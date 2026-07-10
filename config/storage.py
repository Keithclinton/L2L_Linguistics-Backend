import requests
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from decouple import config

BLOB_TOKEN = config('BLOB_READ_WRITE_TOKEN', default='')
BLOB_API_BASE = 'https://blob.vercel-storage.com'


@deconstructible
class VercelBlobStorage(Storage):
    """Stores uploads in Vercel Blob. Field values are the full Blob URL,
    not a relative path, so `url()` just returns it unchanged."""

    def _save(self, name, content):
        content.seek(0)
        resp = requests.put(
            f'{BLOB_API_BASE}/{name}',
            data=content.read(),
            headers={
                'Authorization': f'Bearer {BLOB_TOKEN}',
                'x-content-type': getattr(content, 'content_type', 'application/octet-stream') or 'application/octet-stream',
                'x-add-random-suffix': '1',
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()['url']

    def url(self, name):
        return name

    def exists(self, name):
        # Vercel Blob's x-add-random-suffix avoids collisions server-side,
        # so Django's own get_available_name() dance is unnecessary.
        return False

    def delete(self, name):
        requests.delete(
            f'{BLOB_API_BASE}?url={name}',
            headers={'Authorization': f'Bearer {BLOB_TOKEN}'},
            timeout=30,
        )

    def size(self, name):
        raise NotImplementedError('VercelBlobStorage does not support size().')
