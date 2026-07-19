"""
Management command: seed_swah101

Creates the Mastering Kiswahili for Beginners (Level I) course with 6 weekly
lessons based on the SWAH 101 syllabus. Safe to run multiple times — it skips
existing records rather than duplicating them.

Usage:
    python manage.py seed_swah101
    python manage.py seed_swah101 --price 1000
    python manage.py seed_swah101 --publish
"""

from django.core.management.base import BaseCommand
from courses.models import Category, Course, Lesson

LESSONS = [
    {
        "order": 1,
        "title": "Chapter 1 — Introduction to the Swahili Language",
        "duration_minutes": 45,
        "is_preview": True,
        "content": (
            "Welcome to Mastering Kiswahili for Beginners.\n\n"
            "1.1 What is Swahili?\n"
            "Swahili, known natively as Kiswahili, is one of Africa's most widely spoken languages. "
            "It belongs to the Bantu family and has over 100 million speakers. It serves as a bridge "
            "language across East and Central Africa, used in homes, schools, businesses, and government.\n\n"
            "1.2 Where is Swahili Spoken?\n"
            "Swahili is spoken in: Kenya, Tanzania, Uganda, Rwanda, Burundi, DR Congo, Mozambique, "
            "Comoros, and Zambia (border areas). Many universities worldwide also teach Swahili.\n\n"
            "1.3 Why Learn Swahili?\n"
            "• Education — important in African studies\n"
            "• Travel — communicate with local people\n"
            "• Business — East Africa is a fast-growing economic region\n"
            "• Employment — valued by international organisations\n"
            "• Culture — opens doors to African literature, music, and history\n\n"
            "1.4 Characteristics of Swahili\n"
            "• Words are pronounced almost exactly as written\n"
            "• Only five vowel sounds\n"
            "• Spelling is highly consistent\n"
            "• Many recognisable English loanwords: Kompyuta, Redio, Hospitali, Televisheni\n\n"
            "1.5 Your First Ten Swahili Words\n"
            "Jambo — Hello\n"
            "Asante — Thank you\n"
            "Karibu — Welcome\n"
            "Kwaheri — Goodbye\n"
            "Ndiyo — Yes\n"
            "Hapana — No\n"
            "Tafadhali — Please\n"
            "Samahani — Sorry\n"
            "Rafiki — Friend\n"
            "Shule — School\n\n"
            "Cultural Note: In many East African communities, greeting someone before asking a "
            "question is a sign of respect. Take time to say Jambo before starting a conversation."
        ),
    },
    {
        "order": 2,
        "title": "Chapter 2 — Greetings and Polite Expressions",
        "duration_minutes": 45,
        "is_preview": True,
        "content": (
            "2.1 Why Greetings Matter\n"
            "In Swahili-speaking communities, greeting someone is a sign of respect and social "
            "awareness. Even brief interactions begin with a greeting.\n\n"
            "2.2 Common Greetings\n"
            "Jambo — Hello\n"
            "Hamjambo? — Hello (plural/formal)\n"
            "Hujambo? — How are you?\n"
            "Sijambo — I am fine\n"
            "Habari ya asubuhi — Good morning\n"
            "Habari ya mchana — Good afternoon\n"
            "Habari ya jioni — Good evening\n"
            "Kwaheri — Goodbye\n"
            "Tutaonana — See you later\n\n"
            "2.3 Asking About Someone's Well-Being\n"
            "Habari? — How are things?\n"
            "Habari za leo? — How are you today?\n"
            "Habari za kazi? — How is work?\n"
            "Habari za nyumbani? — How is your family/home?\n\n"
            "Common responses:\n"
            "Nzuri — Fine\n"
            "Nzuri sana — Very well\n"
            "Salama — Peaceful / I'm well\n"
            "Poa — Cool / I'm good (informal)\n\n"
            "Polite Expressions Vocabulary:\n"
            "Asante — Thank you\n"
            "Asante sana — Thank you very much\n"
            "Karibu — Welcome\n"
            "Tafadhali — Please\n"
            "Samahani — Excuse me / Sorry\n"
            "Ndiyo — Yes\n"
            "Hapana — No\n\n"
            "Sample Dialogue:\n"
            "Amina: Jambo!\n"
            "John: Jambo!\n"
            "Amina: Habari?\n"
            "John: Nzuri sana. Asante. Wewe je?\n"
            "Amina: Mimi pia ni mzuri.\n\n"
            "Cultural Tip: When greeting an elder or someone you do not know well, use more "
            "respectful forms and show genuine interest in their well-being."
        ),
    },
    {
        "order": 3,
        "title": "Chapter 3 — The Swahili Alphabet and Pronunciation",
        "duration_minutes": 45,
        "is_preview": False,
        "content": (
            "3.1 The Swahili Alphabet\n"
            "Swahili uses the Latin alphabet: A B C D E F G H I J K L M N O P R S T U V W Y Z\n"
            "Q and X appear mainly in borrowed words.\n\n"
            "3.2 The Five Vowels\n"
            "A — 'Ah' as in father — baba\n"
            "E — 'Eh' as in bed — embe\n"
            "I — 'Ee' as in machine — pili\n"
            "O — 'Oh' as in obey — moto\n"
            "U — 'Oo' as in rule — kuku\n\n"
            "Unlike English, these sounds never change. 'Asante' is always A-SA-NTE, never AY-SAYN-TEE.\n\n"
            "3.3 Consonants\n"
            "Most consonants sound like English. Examples:\n"
            "B — baba (father)\n"
            "D — dada (sister)\n"
            "K — kitabu (book)\n"
            "M — mama (mother)\n"
            "P — pesa (money)\n"
            "S — safari (journey)\n\n"
            "3.4 Special Letter Combinations\n"
            "CH — like 'ch' in chair: chakula, chai, chumba\n"
            "SH — like 'sh' in ship: shule, shati, shamba\n"
            "NY — like 'ny' in canyon: nyumba, nyama, nyota\n"
            "NG' — single nasal sound: ng'ombe, ngoma, ngazi\n"
            "DH — like 'th' in this: dhahabu, dhambi\n\n"
            "3.5 Syllables\n"
            "Each syllable usually ends in a vowel:\n"
            "Ma-ma | Ba-ba | Ki-ta-bu | Ra-fi-ki | Nyu-mba\n\n"
            "3.6 Word Stress\n"
            "Most words are stressed on the second-last syllable:\n"
            "ki-TA-bu | ra-FI-ki | cha-KU-la | ku-SO-ma\n\n"
            "Key Vocabulary:\n"
            "baba — father | mama — mother | mtoto — child | shule — school\n"
            "kitabu — book | kalamu — pen | chakula — food | maji — water\n"
            "nyumba — house | rafiki — friend"
        ),
    },
    {
        "order": 4,
        "title": "Chapter 4 — Introducing Yourself",
        "duration_minutes": 45,
        "is_preview": False,
        "content": (
            "4.1 Key Vocabulary\n"
            "Jina — Name | Jina langu — My name | Mimi — I/Me | Wewe — You\n"
            "Nchi — Country | Mji — Town/City | Kijiji — Village\n"
            "Mwanafunzi — Student | Mwalimu — Teacher | Daktari — Doctor\n"
            "Mfanyabiashara — Businessperson | Mhandisi — Engineer | Muuguzi — Nurse\n\n"
            "4.2 Saying Your Name\n"
            "Jina langu ni... — My name is...\n"
            "Mimi ninaitwa... — I am called...\n"
            "Examples: Jina langu ni John. | Mimi ninaitwa Maria.\n\n"
            "4.3 Asking Someone's Name\n"
            "Jina lako ni nani? — What is your name?\n"
            "Response: Jina langu ni Grace.\n\n"
            "Useful Expression:\n"
            "Nimefurahi kukutana nawe — I am pleased to meet you.\n"
            "Nimefurahi pia — I am pleased too.\n\n"
            "4.4 Saying Where You Come From\n"
            "Ninatoka... — I come from...\n"
            "Unatoka wapi? — Where do you come from?\n"
            "Examples: Ninatoka Kenya. | Ninatoka Tanzania. | Ninatoka Uganda.\n\n"
            "4.5 Saying Where You Live\n"
            "Ninaishi... — I live in...\n"
            "Unaishi wapi? — Where do you live?\n"
            "Examples: Ninaishi Nairobi. | Ninaishi Mombasa. | Ninaishi Arusha.\n\n"
            "4.6 Talking About Your Occupation\n"
            "Mimi ni mwanafunzi — I am a student\n"
            "Mimi ni mwalimu — I am a teacher\n"
            "Mimi ni daktari — I am a doctor\n"
            "Wewe ni nani? — What do you do?\n\n"
            "4.7 Talking About Your Age\n"
            "Una miaka mingapi? — How old are you?\n"
            "Nina miaka ishirini — I am twenty years old.\n"
            "Examples: Nina miaka kumi. | Nina miaka kumi na tano. | Nina miaka thelathini.\n\n"
            "Sample Dialogue:\n"
            "Amina: Jina lako ni nani?\n"
            "James: Jina langu ni James.\n"
            "Amina: Unatoka wapi?\n"
            "James: Ninatoka Kenya. Wewe je?\n"
            "Amina: Ninatoka Tanzania. Nimefurahi kukutana nawe.\n"
            "James: Mimi pia."
        ),
    },
    {
        "order": 5,
        "title": "Chapter 5 — Numbers, Time, and Dates",
        "duration_minutes": 60,
        "is_preview": False,
        "content": (
            "5.1 Counting 0–20\n"
            "0 Sifuri | 1 Moja | 2 Mbili | 3 Tatu | 4 Nne | 5 Tano\n"
            "6 Sita | 7 Saba | 8 Nane | 9 Tisa | 10 Kumi\n"
            "11 Kumi na moja | 12 Kumi na mbili | 13 Kumi na tatu\n"
            "14 Kumi na nne | 15 Kumi na tano | 16 Kumi na sita\n"
            "17 Kumi na saba | 18 Kumi na nane | 19 Kumi na tisa | 20 Ishirini\n\n"
            "5.2 Counting 21–100\n"
            "21 Ishirini na moja | 22 Ishirini na mbili | 30 Thelathini\n"
            "40 Arobaini | 50 Hamsini | 60 Sitini | 70 Sabini\n"
            "80 Themanini | 90 Tisini | 100 Mia moja\n\n"
            "Money Vocabulary:\n"
            "Nambari — Number | Pesa — Money | Bei — Price\n"
            "Nafuu — Cheap | Ghali — Expensive | Chenji — Change\n\n"
            "5.3 Age\n"
            "Una miaka mingapi? — How old are you?\n"
            "Nina miaka ishirini — I am twenty years old.\n\n"
            "5.4 Telling Time\n"
            "Saa ngapi? — What time is it?\n"
            "Saa moja — 1 o'clock | Saa tatu — 3 o'clock | Saa sita — 6 o'clock\n"
            "Cultural Note: Traditional Swahili time starts at sunrise (~6:00 a.m.). "
            "Saa moja asubuhi = approximately 7:00 a.m.\n\n"
            "Time Words: Asubuhi — Morning | Mchana — Afternoon | Jioni — Evening\n"
            "Usiku — Night | Leo — Today | Kesho — Tomorrow | Jana — Yesterday\n\n"
            "5.5 Days of the Week\n"
            "Jumatatu — Monday | Jumanne — Tuesday | Jumatano — Wednesday\n"
            "Alhamisi — Thursday | Ijumaa — Friday | Jumamosi — Saturday | Jumapili — Sunday\n\n"
            "5.6 Months of the Year\n"
            "Januari | Februari | Machi | Aprili | Mei | Juni\n"
            "Julai | Agosti | Septemba | Oktoba | Novemba | Desemba\n\n"
            "5.7 Saying the Date\n"
            "Leo ni tarehe + number + month\n"
            "Leo ni tarehe tano Julai — Today is the fifth of July.\n"
            "Leo ni tarehe ngapi? — What is today's date?\n\n"
            "Market Dialogue:\n"
            "Customer: Ndizi ni bei gani? — How much are the bananas?\n"
            "Shopkeeper: Ni shilingi mia moja — They are one hundred shillings.\n"
            "Customer: Asante. | Shopkeeper: Karibu tena."
        ),
    },
    {
        "order": 6,
        "title": "Chapter 6 — Family and Relationships",
        "duration_minutes": 60,
        "is_preview": False,
        "content": (
            "6.1 Family Vocabulary\n"
            "Familia — Family | Baba — Father | Mama — Mother | Wazazi — Parents\n"
            "Mwana — Son | Binti — Daughter | Kaka — Brother | Dada — Sister\n"
            "Mume — Husband | Mke — Wife | Mtoto — Child | Watoto — Children\n"
            "Babu — Grandfather | Bibi — Grandmother | Mjomba — Uncle (mother's brother)\n"
            "Shangazi — Aunt (father's sister) | Binamu — Cousin | Jamaa — Relative\n\n"
            "6.2 Talking About Your Family\n"
            "Hii ni familia yangu — This is my family.\n"
            "Nina kaka mmoja — I have one brother.\n"
            "Nina dada wawili — I have two sisters.\n"
            "Baba yangu anaitwa Musa — My father's name is Musa.\n"
            "Mama yangu ni mwalimu — My mother is a teacher.\n\n"
            "6.3 Possessive Expressions\n"
            "Baba yangu — My father | Mama yangu — My mother\n"
            "Kaka yangu — My brother | Dada yangu — My sister\n"
            "Familia yangu — My family | Familia yako — Your family\n"
            "Familia yetu — Our family | Familia yake — His/Her family\n\n"
            "Possessive suffixes: -angu (my) | -ako (your) | -ake (his/her) "
            "| -etu (our) | -enu (your plural) | -ao (their)\n\n"
            "6.4 Asking About Family\n"
            "Una kaka? — Do you have a brother?\n"
            "Una dada? — Do you have a sister?\n"
            "Una watoto? — Do you have children?\n"
            "Baba yako anafanya kazi gani? — What does your father do?\n"
            "Mama yako anaitwa nani? — What is your mother's name?\n\n"
            "Describing Your Family:\n"
            "Familia yangu ni kubwa — My family is big.\n"
            "Familia yangu ni ndogo — My family is small.\n"
            "Ninaishi na wazazi wangu — I live with my parents.\n"
            "Tunaishi Nairobi — We live in Nairobi.\n\n"
            "Sample Dialogue:\n"
            "Asha: Una kaka?\n"
            "Daniel: Ndiyo, nina kaka mmoja.\n"
            "Asha: Baba yako ni nani?\n"
            "Daniel: Baba yangu ni daktari.\n"
            "Asha: Mama yako je?\n"
            "Daniel: Mama yangu ni mwalimu.\n\n"
            "Cultural Note: In Swahili-speaking communities, respect for elders is a core value. "
            "Children greet parents, grandparents, and teachers before starting conversations. "
            "Family gatherings play a significant role in strengthening relationships."
        ),
    },
]


class Command(BaseCommand):
    help = "Seed the Mastering Kiswahili for Beginners (Level I) course with 6 chapters"

    def add_arguments(self, parser):
        parser.add_argument(
            "--price",
            type=float,
            default=0.00,
            help="Course price in KES (default: 0 = free)",
        )
        parser.add_argument(
            "--publish",
            action="store_true",
            help="Mark the course as published immediately",
        )

    def handle(self, *args, **options):
        price = options["price"]
        publish = options["publish"]

        category, cat_created = Category.objects.get_or_create(
            name="Beginner Kiswahili",
            defaults={"description": "Kiswahili courses for complete beginners at CEFR A1 level."},
        )
        if cat_created:
            self.stdout.write(self.style.SUCCESS(f"  Created category: {category.name}"))
        else:
            self.stdout.write(f"  Category already exists: {category.name}")

        course, course_created = Course.objects.get_or_create(
            title="Mastering Kiswahili for Beginners (Level I)",
            defaults={
                "description": (
                    "A Cambridge-style beginner course in Kiswahili at CEFR A1 level. "
                    "This course (SWAH 101) covers the Swahili alphabet, pronunciation, greetings, "
                    "introductions, numbers, time, dates, and family vocabulary — with dialogues, "
                    "reading passages, grammar notes, and practical activities in every chapter. "
                    "No previous knowledge of Swahili is required."
                ),
                "category": category,
                "level": "beginner",
                "price": price,
                "is_published": publish,
            },
        )

        if course_created:
            self.stdout.write(self.style.SUCCESS(f"  Created course: {course.title}"))
        else:
            self.stdout.write(f"  Course already exists: {course.title}")
            if publish and not course.is_published:
                course.is_published = True
                course.save(update_fields=["is_published"])
                self.stdout.write(self.style.SUCCESS("  Marked course as published."))

        created_count = 0
        skipped_count = 0
        for data in LESSONS:
            lesson, lesson_created = Lesson.objects.get_or_create(
                course=course,
                order=data["order"],
                defaults={
                    "title": data["title"],
                    "content": data["content"],
                    "duration_minutes": data["duration_minutes"],
                    "is_preview": data["is_preview"],
                },
            )
            if lesson_created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n  Done! {created_count} lessons created, {skipped_count} already existed."
            )
        )
        self.stdout.write(
            f"\n  Course URL in admin:\n"
            f"  /admin/courses/course/{course.pk}/change/\n"
        )
        if not course.is_published:
            self.stdout.write(
                self.style.WARNING(
                    "  The course is currently UNPUBLISHED. "
                    "Run with --publish to make it live, or set it in the admin panel."
                )
            )
