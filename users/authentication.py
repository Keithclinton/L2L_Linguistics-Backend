from firebase_admin import auth as firebase_auth
from rest_framework import authentication, exceptions

from .models import Learner


class FirebaseAuthentication(authentication.BaseAuthentication):
    """Authenticates requests carrying a Firebase ID token as a Bearer token."""

    def authenticate(self, request):
        header = authentication.get_authorization_header(request).decode('utf-8')
        if not header or not header.startswith('Bearer '):
            return None

        id_token = header.split(' ', 1)[1]
        try:
            decoded = firebase_auth.verify_id_token(id_token)
        except Exception as exc:
            raise exceptions.AuthenticationFailed('Invalid or expired Firebase token.') from exc

        uid = decoded['uid']
        email = decoded.get('email', '')

        learner = Learner.objects.filter(firebase_uid=uid).first()
        if learner is None:
            learner, created = Learner.objects.get_or_create(
                email=email,
                defaults={
                    'firebase_uid': uid,
                    'first_name': decoded.get('name', '').split(' ')[0],
                    'last_name': ' '.join(decoded.get('name', '').split(' ')[1:]),
                },
            )
            if not created and not learner.firebase_uid:
                learner.firebase_uid = uid
                learner.save(update_fields=['firebase_uid'])
            if created:
                learner.set_unusable_password()
                learner.save(update_fields=['password'])

        return (learner, None)
