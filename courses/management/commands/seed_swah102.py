"""
Management command: seed_swah102

Creates the Intermediate Kiswahili (Level II) course with all 16 weekly
lessons based on the SWAH 102 syllabus. Safe to run multiple times —
it skips existing records rather than duplicating them.

Usage:
    python manage.py seed_swah102
    python manage.py seed_swah102 --price 1500   # set a paid price in KES
    python manage.py seed_swah102 --publish       # mark the course published immediately
"""

from django.core.management.base import BaseCommand
from courses.models import Category, Course, Lesson

LESSONS = [
    {
        "order": 1,
        "title": "Week 1 — Review of Kiswahili Basics",
        "duration_minutes": 90,
        "is_preview": True,
        "content": (
            "Topic: Review of foundational Kiswahili\n"
            "Key Grammar: Noun classes and their agreement patterns\n"
            "Skills Focus: Speaking\n\n"
            "Activities:\n"
            "• Introductions and greetings review\n"
            "• Vocabulary games covering core Level I vocabulary\n\n"
            "Assignment:\n"
            "Write a self-introduction (150 words) covering your name, where you are from, "
            "what you do, and why you are learning Kiswahili.\n\n"
            "Digital Tool: Duolingo — complete the review module before next class."
        ),
    },
    {
        "order": 2,
        "title": "Week 2 — Present Tense (Wakati wa Sasa)",
        "duration_minutes": 90,
        "is_preview": True,
        "content": (
            "Topic: Present tense verbs in Kiswahili\n"
            "Key Grammar: Affirmative and negative present tense constructions\n"
            "Skills Focus: Conversation\n\n"
            "Structure:\n"
            "• Affirmative: Subject prefix + NA + verb root  →  Ninasoma (I am reading)\n"
            "• Negative: Subject prefix + SI + verb root  →  Sisomi (I am not reading)\n\n"
            "Activities:\n"
            "• Dialogue practice: daily routines (asubuhi, mchana, jioni)\n"
            "• Pair work: asking and answering 'Unafanya nini sasa?'\n\n"
            "Assignment:\n"
            "Record a 2-minute conversation with a partner discussing your daily routine. "
            "Use at least 10 different verbs in the present tense.\n\n"
            "Digital Tool: Quizlet — verb drills flashcard set."
        ),
    },
    {
        "order": 3,
        "title": "Week 3 — Past Tense (Wakati Uliopita)",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Narrating past events in Kiswahili\n"
            "Key Grammar: Past tense verb forms using -LI- tense marker\n"
            "Skills Focus: Writing\n\n"
            "Structure:\n"
            "• Recent past: Subject + LI + verb root  →  Nilisoma (I read / I was reading)\n"
            "• Negative past: Subject + KU + verb root  →  Sikuenda (I did not go)\n\n"
            "Activities:\n"
            "• Storytelling: narrate what you did last weekend\n"
            "• Gap-fill exercises with -LI- and -KU- forms\n\n"
            "Assignment:\n"
            "Write a paragraph (200 words) describing a past experience or memorable event. "
            "Include at least 8 past tense verbs.\n\n"
            "Digital Tool: Grammarly — paste your paragraph to check sentence structure."
        ),
    },
    {
        "order": 4,
        "title": "Week 4 — Future Tense (Wakati Ujao)",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Expressing future plans and intentions\n"
            "Key Grammar: Future tense using -TA- tense marker\n"
            "Skills Focus: Speaking\n\n"
            "Structure:\n"
            "• Future: Subject + TA + verb root  →  Nitasoma (I will read)\n"
            "• Negative future: Subject + HATA + verb root  →  Sitasoma (I will not read)\n\n"
            "Activities:\n"
            "• Planning scenarios: holiday plans, career goals, weekend activities\n"
            "• Group discussion: 'Utafanya nini baadaye?'\n\n"
            "Assignment:\n"
            "Write a short paragraph about your future goals — what you will study, where "
            "you will travel, and what you hope to achieve. Use at least 6 future tense verbs."
        ),
    },
    {
        "order": 5,
        "title": "Week 5 — Object Markers",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Object markers in Kiswahili verbs\n"
            "Key Grammar: Sentence structure with object infixes\n"
            "Skills Focus: Listening\n\n"
            "Concept:\n"
            "Object markers are prefixes inserted into the verb to indicate the object, "
            "allowing the object noun to be omitted.\n\n"
            "Examples:\n"
            "• Ninamwona (I see him/her) — -m- is the object marker\n"
            "• Ninakipenda (I like it) — -ki- refers to a ki-class noun\n"
            "• Wanawaona (They see them) — -wa- refers to people\n\n"
            "Activities:\n"
            "• Sentence-building drills substituting object markers\n"
            "• Listening exercise: identify the object marker used in each sentence\n\n"
            "Assignment:\n"
            "Complete the grammar worksheet: rewrite 20 sentences replacing full object "
            "nouns with the correct object markers."
        ),
    },
    {
        "order": 6,
        "title": "Week 6 — Imperatives (Amri)",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Commands and requests in Kiswahili\n"
            "Key Grammar: Imperative verb forms (singular and plural)\n"
            "Skills Focus: Role-play\n\n"
            "Structure:\n"
            "• Singular command: verb root alone  →  Soma! (Read!)\n"
            "• Plural command: verb root + -ni  →  Someni! (Read! — to a group)\n"
            "• Polite request: Tafadhali + verb  →  Tafadhali kaa. (Please sit.)\n"
            "• Negative imperative: Usisome / Msisome (Don't read)\n\n"
            "Activities:\n"
            "• Role-play scenarios: market, classroom, bus station\n"
            "• Giving and following instructions in pairs\n\n"
            "Assignment:\n"
            "Write a dialogue script (15–20 lines) set in a market (soko). "
            "Include at least 6 imperative forms, both singular and plural."
        ),
    },
    {
        "order": 7,
        "title": "Week 7 — Adjectives and Agreement",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Descriptive adjectives and noun class agreement\n"
            "Key Grammar: Adjective agreement with noun classes\n"
            "Skills Focus: Writing\n\n"
            "Concept:\n"
            "In Kiswahili, adjectives must agree with the noun class of the noun they describe.\n\n"
            "Examples:\n"
            "• Mtoto mzuri (good child — M/WA class)\n"
            "• Watoto wazuri (good children)\n"
            "• Kitabu kizuri (good book — KI/VI class)\n"
            "• Nyumba nzuri (good house — N class)\n\n"
            "Common adjectives: -zuri (good), -baya (bad), -kubwa (big), -dogo (small), "
            "-refu (tall/long), -fupi (short), -zito (heavy), -pya (new), -zee (old)\n\n"
            "Activities:\n"
            "• Descriptive exercises with pictures\n"
            "• Matching adjectives to correct noun class prefixes\n\n"
            "Assignment:\n"
            "Write a descriptive paragraph (150 words) about a person or place you know. "
            "Use at least 8 different adjectives with correct agreement."
        ),
    },
    {
        "order": 8,
        "title": "Week 8 — Midterm Exam",
        "duration_minutes": 120,
        "is_preview": False,
        "content": (
            "Midterm Assessment — Weeks 1–7\n\n"
            "The midterm covers all content from Weeks 1–7:\n"
            "• Noun classes and agreement (Week 1)\n"
            "• Present tense — affirmative and negative (Week 2)\n"
            "• Past tense with -LI- and -KU- (Week 3)\n"
            "• Future tense with -TA- (Week 4)\n"
            "• Object markers (Week 5)\n"
            "• Imperatives — singular, plural, negative (Week 6)\n"
            "• Adjective agreement (Week 7)\n\n"
            "Format:\n"
            "• Section A: Multiple choice (grammar, 20 questions)\n"
            "• Section B: Fill in the blank (verb conjugation, 15 questions)\n"
            "• Section C: Short writing (one paragraph, 100 words)\n"
            "• Section D: Oral component — 3-minute conversation with instructor\n\n"
            "Weight: 20% of final grade"
        ),
    },
    {
        "order": 9,
        "title": "Week 9 — Possessives (Umiliki)",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Expressing ownership and possession\n"
            "Key Grammar: Possessive concords agreeing with noun classes\n"
            "Skills Focus: Reading\n\n"
            "Concept:\n"
            "Possessives in Kiswahili use a possessive marker that agrees with the noun possessed, "
            "not the possessor.\n\n"
            "Examples:\n"
            "• Kitabu changu (my book) — KI class possessive 'ch-'\n"
            "• Watoto wangu (my children) — WA class possessive 'w-'\n"
            "• Nyumba yangu (my house) — N class possessive 'y-'\n\n"
            "Possessive pronouns: -angu (my), -ako (your), -ake (his/her), "
            "-etu (our), -enu (your plural), -ao (their)\n\n"
            "Activities:\n"
            "• Reading passage: A Kiswahili family description using possessives\n"
            "• Comprehension questions on the passage\n\n"
            "Assignment:\n"
            "Reading comprehension exercise: answer 10 questions about a provided text, "
            "focusing on identifying possessive constructions and their referents."
        ),
    },
    {
        "order": 10,
        "title": "Week 10 — Prepositions and Location",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Describing location and giving directions\n"
            "Key Grammar: Locative suffixes (-ni) and place words\n"
            "Skills Focus: Dialogue\n\n"
            "Key Vocabulary:\n"
            "• -ni suffix: adds locative meaning  →  nyumbani (at home), darasa → darasani (in class)\n"
            "• Mahali (place), karibu na (near), mbali na (far from)\n"
            "• Directional words: kushoto (left), kulia (right), moja kwa moja (straight ahead)\n"
            "• Prepositions: ndani ya (inside), nje ya (outside), juu ya (on top of), "
            "chini ya (under), kati ya (between)\n\n"
            "Activities:\n"
            "• Map exercises: describe the location of buildings on a town map\n"
            "• Pair dialogue: giving and following directions around a city\n\n"
            "Assignment:\n"
            "Write a set of directions (8–10 sentences) from one landmark to another in your "
            "town or city. Use at least 5 different locative expressions."
        ),
    },
    {
        "order": 11,
        "title": "Week 11 — Complex Sentences and Conjunctions",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Linking ideas using conjunctions\n"
            "Key Grammar: Subordinating and coordinating conjunctions\n"
            "Skills Focus: Writing\n\n"
            "Key Conjunctions:\n"
            "• na (and), lakini (but), kwa sababu (because), kwa hivyo (therefore)\n"
            "• ingawa / ijapokuwa (although), ili (so that / in order to)\n"
            "• wakati (when), kabla ya (before), baada ya (after)\n"
            "• ikiwa / kama (if)\n\n"
            "Examples:\n"
            "• Ninasoma kwa sababu napenda Kiswahili. (I study because I love Kiswahili.)\n"
            "• Nitakwenda dukani baada ya kula chakula. (I will go to the shop after eating.)\n\n"
            "Activities:\n"
            "• Writing workshop: combine simple sentences into complex ones\n"
            "• Peer editing: swap and correct each other's sentences\n\n"
            "Assignment:\n"
            "Write a short essay (200 words) on the topic 'Why I am learning Kiswahili.' "
            "Use at least 6 different conjunctions."
        ),
    },
    {
        "order": 12,
        "title": "Week 12 — Conditionals (Masharti)",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Expressing conditions and hypotheticals\n"
            "Key Grammar: If-clauses using -KI- (real condition) and -NGE-/-NGELI- (unreal)\n"
            "Skills Focus: Speaking\n\n"
            "Structure:\n"
            "• Real/possible condition (-KI-): Ukisoma, utafaulu. "
            "(If you study, you will succeed.)\n"
            "• Hypothetical (-NGE-): Ningeenda Kenya, ningejifunza Kiswahili zaidi. "
            "(If I went to Kenya, I would learn more Kiswahili.)\n"
            "• Past unreal (-NGELI-): Ningelisoma, ningelifaulu. "
            "(If I had studied, I would have passed.)\n\n"
            "Activities:\n"
            "• Debate scenario: 'Ikiwa serikali ingefanya X, nini kingetokea?'\n"
            "• Pair challenge: respond to 'if' prompts using the correct conditional form\n\n"
            "Assignment:\n"
            "Write 10 original 'If…' conditional sentences — 4 using -KI-, 4 using -NGE-, "
            "and 2 using -NGELI-."
        ),
    },
    {
        "order": 13,
        "title": "Week 13 — Culture and East African Context",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: East African cultural practices and communication norms\n"
            "Key Grammar: Reading and text analysis\n"
            "Skills Focus: Reading and Cultural Competence\n\n"
            "Topics Covered:\n"
            "• The role of Kiswahili as a lingua franca in East Africa\n"
            "• Greetings and respect in Kiswahili culture (heshima kwa wazee)\n"
            "• Food, family, and social customs across Kenya, Tanzania, Uganda\n"
            "• African proverbs (methali) and their meanings\n"
            "  – Haba na haba hujaza kibaba (Little by little fills the measure)\n"
            "  – Haraka haraka haina baraka (Hurry hurry has no blessing)\n"
            "  – Umoja ni nguvu, utengano ni udhaifu (Unity is strength, division is weakness)\n\n"
            "Activities:\n"
            "• Group cultural discussion\n"
            "• Text analysis of a short East African story or newspaper excerpt\n\n"
            "Assignment:\n"
            "Write a reflection paper (250 words): How does learning about East African culture "
            "change or deepen your understanding of the Kiswahili language?"
        ),
    },
    {
        "order": 14,
        "title": "Week 14 — Fluency Practice and Listening",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Building listening fluency with authentic Kiswahili audio\n"
            "Key Grammar: Review of all tenses and structures\n"
            "Skills Focus: Listening\n\n"
            "Goals:\n"
            "• Identify main ideas in spoken Kiswahili\n"
            "• Understand naturally paced conversation\n"
            "• Pick out familiar vocabulary from authentic speech\n\n"
            "Activities:\n"
            "• Listening exercises from authentic Kiswahili radio or video clips\n"
            "• Note-taking: summarise what you heard in 3–5 sentences\n"
            "• Dictation exercise: listen and write\n\n"
            "Digital Tool:\n"
            "YouTube — search 'Kiswahili news Kenya' or 'Kiswahili lessons Kenya' for "
            "authentic listening material. Recommended channels: KBC Channel 1, Citizen TV Kenya.\n\n"
            "No formal assignment — focus on listening for at least 20 minutes outside class "
            "and jot down 10 new words you heard."
        ),
    },
    {
        "order": 15,
        "title": "Week 15 — Oral Presentations",
        "duration_minutes": 90,
        "is_preview": False,
        "content": (
            "Topic: Formal oral presentation in Kiswahili\n"
            "Key Grammar: Application of all grammar structures covered in the course\n"
            "Skills Focus: Speaking\n\n"
            "Presentation Requirements:\n"
            "• Length: 4–5 minutes per learner\n"
            "• Language: Kiswahili only\n"
            "• Topic: Choose ONE of the following:\n"
            "  1. Describe your hometown or home country in Kiswahili\n"
            "  2. Present a traditional East African story (hadithi)\n"
            "  3. Teach the class one cultural practice from East Africa\n"
            "  4. Summarise a Kiswahili news story from the past week\n\n"
            "Grading Rubric:\n"
            "• Pronunciation and fluency (30%)\n"
            "• Grammar accuracy (30%)\n"
            "• Content and organisation (25%)\n"
            "• Confidence and delivery (15%)\n\n"
            "Weight: 10% of final grade"
        ),
    },
    {
        "order": 16,
        "title": "Week 16 — Final Exam",
        "duration_minutes": 120,
        "is_preview": False,
        "content": (
            "Final Examination — Comprehensive Review\n\n"
            "The final exam covers all course content (Weeks 1–15).\n\n"
            "Format:\n"
            "• Section A: Multiple choice — grammar and vocabulary (25 questions)\n"
            "• Section B: Verb conjugation table — complete tense forms (10 questions)\n"
            "• Section C: Reading comprehension — passage with 10 questions\n"
            "• Section D: Writing — one structured essay (250 words)\n"
            "• Section E: Oral — 5-minute conversation with examiners\n\n"
            "Topics:\n"
            "Noun classes, present/past/future tense, object markers, imperatives, "
            "adjectives, possessives, prepositions, complex sentences, conditionals, "
            "cultural knowledge\n\n"
            "Weight: 20% of final grade\n\n"
            "Grading Scale:\n"
            "A (70–100%): Distinction  |  B (60–69%): Credit  |  "
            "C (50–59%): Pass  |  D (<50%): Fail"
        ),
    },
]


class Command(BaseCommand):
    help = "Seed the SWAH 102 Intermediate Kiswahili course with all 16 weekly lessons"

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

        # Category
        category, cat_created = Category.objects.get_or_create(
            name="Intermediate Kiswahili",
            defaults={"description": "Structured Kiswahili courses for learners at CEFR A2–B1 level."},
        )
        if cat_created:
            self.stdout.write(self.style.SUCCESS(f"  Created category: {category.name}"))
        else:
            self.stdout.write(f"  Category already exists: {category.name}")

        # Course
        course, course_created = Course.objects.get_or_create(
            title="Intermediate Kiswahili (Level II)",
            defaults={
                "description": (
                    "Develop intermediate proficiency in Kiswahili at CEFR A2–B1 level. "
                    "This 16-week course (SWAH 102) covers present, past, and future tenses, "
                    "object markers, imperatives, adjectives, possessives, prepositions, "
                    "complex sentences, and conditionals — integrated with East African cultural "
                    "knowledge. Includes weekly assignments, a midterm, oral presentations, and a "
                    "final exam. Prerequisite: Introductory Kiswahili (Level I) or equivalent."
                ),
                "category": category,
                "level": "intermediate",
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

        # Lessons
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
