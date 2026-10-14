import json
from datetime import datetime
from backend.app.database import engine, Base, SessionLocal
from backend.app.models.curriculum import Chapter, Word, Exercise, PlacementTest
from backend.app.models.user import User
from backend.app.models.progress import UserChapterProgress
from backend.app.services.auth_service import hash_password

def generate_curriculum_data():
    """Generates the full 60 chapters: A1 (10), A2 (10), B1 (20), B2 (20)"""
    curriculum = []

    # ----------------------------------------------------
    # LEVEL A1: 10 Chapters
    # ----------------------------------------------------
    a1_chapters = [
        {
            "num": 1,
            "title": "Chapter 1: First Encounters & Greetings",
            "desc": "Learn how to greet people at different times of day, introduce yourself, and master the Italian alphabet and pronunciation.",
            "grammar_title": "Subject Pronouns & Present Tense of 'Essere' (To Be)",
            "grammar_rules": """### Subject Pronouns & 'Essere'
In Italian, subject pronouns (*io, tu, lui/lei, noi, voi, loro*) are frequently omitted because the verb ending indicates who is performing the action.

#### Present Tense of 'Essere' (To Be)
- **io sono** = I am
- **tu sei** = you are (informal)
- **lui / lei è** = he / she is (Lei è = you are, formal)
- **noi siamo** = we are
- **voi siete** = you all are
- **loro sono** = they are

#### Key Greetings
- **Buongiorno** (Good morning / Good day — until ~2 PM)
- **Buonasera** (Good evening — from ~2 PM onwards)
- **Ciao** (Hi / Bye — informal only with friends and peers)
- **Arrivederci** (Goodbye — neutral / formal)
""",
            "grammar_tables": [
                {
                    "title": "Conjugation of 'Essere'",
                    "headers": ["Pronoun", "Italian", "English"],
                    "rows": [
                        ["io", "sono", "I am"],
                        ["tu", "sei", "you are"],
                        ["lui / lei", "è", "he / she is"],
                        ["noi", "siamo", "we are"],
                        ["voi", "siete", "you all are"],
                        ["loro", "sono", "they are"]
                    ]
                }
            ],
            "reading_title": "First Meeting in Piazza del Popolo",
            "reading_it": """Marco è a Roma per studio. Nella piazza incontra Elena, una studentessa dell'università.
«Ciao! Io sono Marco, e tu come ti chiami?»
«Piacere Marco, io sono Elena. Di dove sei?»
«Sono americano, di New York, ma abito a Roma da due settimane. E tu?»
«Io sono italiana, di Firenze! Benvenuto in Italia!».
Marco ed Elena parlano allegramente e decidono di bere un caffè insieme al bar.""",
            "reading_en": """Marco is in Rome for his studies. In the square he meets Elena, a university student.
"Hi! I am Marco, and what is your name?"
"Nice to meet you Marco, I am Elena. Where are you from?"
"I am American, from New York, but I have lived in Rome for two weeks. And you?"
"I am Italian, from Florence! Welcome to Italy!".
Marco and Elena chat cheerfully and decide to have a coffee together at the bar.""",
            "reading_questions": [
                {
                    "question": "Di dove è Marco?",
                    "options": ["Di New York", "Di Firenze", "Di Milano", "Di Roma"],
                    "correct_answer": "Di New York",
                    "explanation": "Marco states: 'Sono americano, di New York'."
                },
                {
                    "question": "Cosa decidono di fare Marco ed Elena?",
                    "options": ["Bere un caffè insieme al bar", "Prendere il treno", "Andare al cinema", "Studiare in biblioteca"],
                    "correct_answer": "Bere un caffè insieme al bar",
                    "explanation": "The text states: 'decidono di bere un caffè insieme al bar'."
                }
            ],
            "writing_prompt": "Introduce yourself in Italian by stating your name, nationality, and where you currently live.",
            "writing_chips": ["Ciao!", "Mi chiamo", "Io sono", "Sono americano", "Abito a", "Piacere di conoscerti"],
            "writing_solution": "Ciao! Mi chiamo Alex, sono americano e abito a Roma. Piacere di conoscerti!",
            "words": [
                ("ciao", "Inter", "hi / bye (informal)", "CHOW", "Ciao Marco, come stai?", "Hi Marco, how are you?", "salutare"),
                ("buongiorno", "Inter", "good morning / good day", "bwon-JOHR-noh", "Buongiorno professore!", "Good morning professor!", "giorno"),
                ("buonasera", "Inter", "good evening", "bwoh-nah-SEH-rah", "Buonasera a tutti.", "Good evening to all.", "sera"),
                ("piacere", "Nm", "pleasure / nice to meet you", "pyah-CHEH-reh", "Piacere di conoscerti.", "Nice to meet you.", "piacere (Va)"),
                ("essere", "Va", "to be", "EHS-seh-reh", "Io sono di Roma.", "I am from Rome.", "essenza"),
                ("chiamarsi", "Vr", "to be called / named", "kyah-MAHR-see", "Come ti chiami?", "What is your name?", "chiamare"),
                ("italiano", "Agg", "Italian (m)", "ee-tah-LYAH-noh", "Il caffè italiano è forte.", "Italian coffee is strong.", "Italia"),
                ("americana", "Agg", "American (f)", "ah-meh-ree-KAH-nah", "Elena è americana.", "Elena is American.", "America"),
                ("studente", "Nm", "student (m)", "stoo-DEHN-teh", "Marco è uno studente serio.", "Marco is a serious student.", "studiare"),
                ("università", "Nf", "university", "oo-nee-vehr-see-TAH", "L'università è antica.", "The university is ancient.", "universitario"),
                ("abitare", "Va", "to live / reside", "ah-bee-TAH-reh", "Abito in centro.", "I live in the center.", "abitazione"),
                ("dove", "Avv", "where", "DOH-veh", "Di dove sei?", "Where are you from?", "dovunque"),
                ("grazie", "Inter", "thank you", "GRAH-tsyeh", "Grazie mille per l'aiuto.", "Thanks a lot for the help.", "ringraziare"),
                ("prego", "Inter", "you are welcome / please", "PREH-goh", "Prego, si accomodi.", "You're welcome, make yourself comfortable.", "pregare"),
                ("arrivederci", "Inter", "goodbye", "ahr-ree-veh-DEHR-chee", "Arrivederci e a presto!", "Goodbye and see you soon!", "vedere")
            ]
        },
        {
            "num": 2,
            "title": "Chapter 2: People, Nationalities & Identity",
            "desc": "Express nationalities, grammatical gender of nouns (masculine vs. feminine), and the present tense of 'Avere' (To Have).",
            "grammar_title": "Noun Gender, Number & Present of 'Avere'",
            "grammar_rules": """### Noun Gender & 'Avere' (To Have)
In Italian, nouns ending in **-o** are usually masculine (plural in **-i**), and nouns ending in **-a** are feminine (plural in **-e**). Nouns ending in **-e** can be masculine or feminine and end in **-i** in the plural.

#### Present Tense of 'Avere' (To Have)
- **io ho** = I have (silent 'h'!)
- **tu hai** = you have
- **lui / lei ha** = he / she has
- **noi abbiamo** = we have
- **voi avete** = you all have
- **loro hanno** = they have
""",
            "grammar_tables": [
                {
                    "title": "Conjugation of 'Avere'",
                    "headers": ["Pronoun", "Form", "Meaning"],
                    "rows": [
                        ["io", "ho", "I have"],
                        ["tu", "hai", "you have"],
                        ["lui/lei", "ha", "he/she has"],
                        ["noi", "abbiamo", "we have"],
                        ["voi", "avete", "you all have"],
                        ["loro", "hanno", "they have"]
                    ]
                }
            ],
            "reading_title": "Classmates from Around the World",
            "reading_it": """Nella classe d'italiano ci sono studenti di molti paesi.
Sarah ha ventidue anni ed è inglese. Kenji ha venticinque anni ed è giapponese. 
Tutti hanno un obiettivo comune: imparare a parlare italiano con scioltezza.
L'insegnante, la professoressa Rossi, spiega la lezione con pazienza. 
«Voi avete i libri di testo?» chiede la professoressa.
«Sì, abbiamo tutti il libro e il quaderno!» rispondono gli studenti.""",
            "reading_en": """In the Italian class there are students from many countries.
Sarah is twenty-two years old and is English. Kenji is twenty-five and is Japanese.
Everyone has a common goal: to learn to speak Italian fluently.
The teacher, Professor Rossi, explains the lesson with patience.
"Do you all have the textbooks?" asks the professor.
"Yes, we all have the book and the notebook!" reply the students.""",
            "reading_questions": [
                {
                    "question": "Quanti anni ha Sarah?",
                    "options": ["Ventidue anni", "Venti anni", "Venticinque anni", "Trenta anni"],
                    "correct_answer": "Ventidue anni",
                    "explanation": "Sarah ha ventidue anni (22 years old)."
                }
            ],
            "writing_prompt": "Describe your age and two items you have on your study desk using 'avere'.",
            "writing_chips": ["Io ho", "Ho venticinque anni", "Sul tavolo", "Ho un libro", "E una penna"],
            "writing_solution": "Io ho venticinque anni. Sul tavolo ho un libro d'italiano e una penna.",
            "words": [
                ("avere", "Va", "to have", "ah-VEH-reh", "Ho una domanda.", "I have a question.", "avaro"),
                ("anno", "Nm", "year", "AHN-noh", "Quanti anni hai?", "How old are you?", "annuale"),
                ("libro", "Nm", "book", "LEE-broh", "Il libro è interessante.", "The book is interesting.", "libreria"),
                ("penna", "Nf", "pen", "PEHN-nah", "Scrivo con la penna blu.", "I write with the blue pen.", "pennarello"),
                ("quaderno", "Nm", "notebook", "kwah-DEHR-noh", "Apro il quaderno.", "I open the notebook.", "foglio"),
                ("classe", "Nf", "class / classroom", "KLAHS-seh", "La classe è luminosa.", "The classroom is bright.", "classico"),
                ("ragazzo", "Nm", "boy / young man", "rah-GAHT-tsoh", "Quel ragazzo è gentile.", "That boy is kind.", "ragazza"),
                ("ragazza", "Nf", "girl / young woman", "rah-GAHT-tsah", "Una ragazza simpatica.", "A nice girl.", "ragazzo"),
                ("inglese", "Agg", "English", "een-GLEH-zeh", "Parlo inglese.", "I speak English.", "Inghilterra"),
                ("spagnolo", "Agg", "Spanish", "spah-NYOH-loh", "Lui è spagnolo.", "He is Spanish.", "Spagna"),
                ("francese", "Agg", "French", "frahn-CHEH-zeh", "Lei parla francese.", "She speaks French.", "Francia"),
                ("tedesco", "Agg", "German", "teh-DEHS-koh", "Un dizionario tedesco.", "A German dictionary.", "Germania"),
                ("amico", "Nm", "friend (male)", "ah-MEE-koh", "Il mio migliore amico.", "My best friend.", "amicizia"),
                ("amica", "Nf", "friend (female)", "ah-MEE-kah", "Chiara è mia amica.", "Chiara is my friend.", "amichevole"),
                ("lingua", "Nf", "language / tongue", "LEEN-gwah", "L'italiano è una bella lingua.", "Italian is a beautiful language.", "linguaggio")
            ]
        },
        {
            "num": 3,
            "title": "Chapter 3: At the Italian Bar & Café",
            "desc": "Master how to order coffee, pastries, and drinks politely using 'Vorrei' and regular -are verb endings.",
            "grammar_title": "Definite Articles & Regular -ARE Verbs",
            "grammar_rules": """### Definite Articles & -ARE Verbs
In Italian, 'the' varies depending on the gender and initial sound:
- **il** (masculine singular consonant): *il caffè*
- **lo** (masculine singular s+cons, z): *lo scontrino*
- **l'** (masculine/feminine singular vowel): *l'espresso*, *l'aranciata*
- **la** (feminine singular consonant): *la pasta*
""",
            "grammar_tables": [
                {
                    "title": "Regular -ARE Verb Endings (Parlare)",
                    "headers": ["Subject", "Ending", "Form"],
                    "rows": [
                        ["io", "-o", "parlo"],
                        ["tu", "-i", "parli"],
                        ["lui/lei", "-a", "parla"],
                        ["noi", "-iamo", "parliamo"],
                        ["voi", "-ate", "parlate"],
                        ["loro", "-ano", "parlano"]
                    ]
                }
            ],
            "reading_title": "Breakfast at the Local Bar",
            "reading_it": """La colazione all'italiana si fa al bar.
Matteo entra e saluta: «Buongiorno! Vorrei un cappuccino e un cornetto caldo».
«Certamente! Vuoi il cornetto alla marmellata o al cioccolato?» chiede il barista.
«Alla marmellata, grazie. E quanto costa?»
«Due euro e cinquanta in totale».
Matteo paga alla cassa e gusta la sua colazione al banco.""",
            "reading_en": """Italian breakfast is done at the bar.
Matteo walks in and greets: "Good morning! I would like a cappuccino and a warm croissant."
"Certainly! Do you want the croissant with jam or chocolate?" asks the barista.
"With jam, thank you. And how much is it?"
"Two euros and fifty in total."
Matteo pays at the register and enjoys his breakfast at the counter.""",
            "reading_questions": [
                {
                    "question": "Cosa ordina Matteo?",
                    "options": ["Un cappuccino e un cornetto", "Un tè freddo", "Una pizza", "Un bicchiere d'acqua"],
                    "correct_answer": "Un cappuccino e un cornetto",
                    "explanation": "Matteo ordina un cappuccino e un cornetto."
                }
            ],
            "writing_prompt": "Order a coffee and mineral water politely at the bar and ask for the total price.",
            "writing_chips": ["Buongiorno", "Vorrei", "Un caffè espresso", "Un'acqua minerale", "Per favore", "Quanto costa?"],
            "writing_solution": "Buongiorno, vorrei un caffè espresso e un'acqua minerale naturale, per favore. Quanto costa?",
            "words": [
                ("caffè", "Nm", "coffee / espresso", "kahf-FEH", "Un caffè per favore.", "A coffee please.", "caffetteria"),
                ("cappuccino", "Nm", "cappuccino", "kahp-poo-CHEE-noh", "Un cappuccino schiumato.", "A foamy cappuccino.", "cappuccio"),
                ("cornetto", "Nm", "croissant / pastry", "kohr-NEHT-toh", "Un cornetto alla crema.", "A cream croissant.", "corno"),
                ("acqua", "Nf", "water", "AHK-wah", "Acqua naturale o frizzante?", "Still or sparkling water?", "acquedotto"),
                ("zucchero", "Nm", "sugar", "TSOOK-keh-roh", "Prendo il caffè senza zucchero.", "I take coffee without sugar.", "zuccherato"),
                ("latte", "Nm", "milk", "LAHT-teh", "Un bicchiere di latte caldo.", "A glass of warm milk.", "latticino"),
                ("spremuta", "Nf", "freshly squeezed juice", "spreh-MOO-tah", "Una spremuta d'arancia fresca.", "A fresh orange juice.", "spremere"),
                ("barista", "Nm/Nf", "bartender / barista", "bah-REES-tah", "Il barista è veloce.", "The barista is fast.", "bar"),
                ("scontrino", "Nm", "receipt", "skohn-TREE-noh", "Ecco lo scontrino.", "Here is the receipt.", "scontrare"),
                ("banco", "Nm", "counter / bench", "BAHN-koh", "Beviamo il caffè al banco.", "We drink the coffee at the counter.", "bancone"),
                ("ordinare", "Va", "to order", "ohr-dee-NAH-reh", "Possiamo ordinare?", "Can we order?", "ordine"),
                ("pagare", "Va", "to pay", "pah-GAH-reh", "Pago io oggi.", "I'm paying today.", "pagamento"),
                ("euro", "Nm", "euro", "EH-oo-roh", "Costa due euro.", "It costs two euros.", "europeo"),
                ("quanto", "Avv", "how much", "KWAHN-toh", "Quanto costa?", "How much does it cost?", "quantità"),
                ("subito", "Avv", "right away / immediately", "SOO-bee-toh", "Arriva subito!", "Coming right away!", "subitaneo")
            ]
        },
        {
            "num": 4,
            "title": "Chapter 4: Dining & Italian Cuisine",
            "desc": "Explore food and restaurants, how to express preferences with 'Mi piace / Mi piacciono', and regular -ere verb patterns.",
            "grammar_title": "The Verb 'Piacere' & Regular -ERE Verbs",
            "grammar_rules": """### The Verb 'Piacere' (To Like)
In Italian, *piacere* literally means 'to be pleasing to'. The verb agrees with the thing that is liked:
- **Mi piace** + singular noun or infinitive verb: *Mi piace la pizza*, *Mi piace cucinare*.
- **Mi piacciono** + plural noun: *Mi piacciono gli spaghetti*.
""",
            "grammar_tables": [
                {
                    "title": "Piacere Usage",
                    "headers": ["Form", "Followed By", "Example"],
                    "rows": [
                        ["Mi piace", "Singular noun / Verb", "Mi piace il risotto. Mi piace viaggiare."],
                        ["Mi piacciono", "Plural noun", "Mi piacciono le lasagne."]
                    ]
                }
            ],
            "reading_title": "Dinner at a Tuscan Trattoria",
            "reading_it": """Stasera andiamo a cena in una trattoria tipica toscana.
Il cameriere porta il menu: antipasti, primi piatti, secondi e dolci.
«Cosa mi consiglia come primo?» chiede Marco.
«Le pappardelle al sugo di funghi sono eccezionali!» risponde il cameriere.
Prendiamo anche una bottiglia di vino rosso e una porzione di tiramisù.
I piatti italiani sono freschi, saporiti e ricchi di tradizione.""",
            "reading_en": """Tonight we go to dinner at a typical Tuscan trattoria.
The waiter brings the menu: appetizers, first courses, second courses, and desserts.
"What do you recommend as a first course?" asks Marco.
"The pappardelle with mushroom sauce is exceptional!" replies the waiter.
We also take a bottle of red wine and a portion of tiramisu.
Italian dishes are fresh, flavorful, and full of tradition.""",
            "reading_questions": [
                {
                    "question": "Cosa consiglia il cameriere a Marco?",
                    "options": ["Le pappardelle ai funghi", "La pizza margherita", "Il pesce spada", "Il pollo arrosto"],
                    "correct_answer": "Le pappardelle ai funghi",
                    "explanation": "Il cameriere consiglia le pappardelle al sugo di funghi."
                }
            ],
            "writing_prompt": "Write two sentences in Italian stating what Italian food you like and what dessert you prefer.",
            "writing_chips": ["Mi piace molto", "La pizza napoletana", "E mi piacciono", "I dolci tradizionali", "Come il tiramisù"],
            "writing_solution": "Mi piace molto la pizza napoletana e mi piacciono i dolci tradizionali come il tiramisù.",
            "words": [
                ("ristorante", "Nm", "restaurant", "ree-stoh-RAHN-teh", "Un ottimo ristorante.", "An excellent restaurant.", "ristorare"),
                ("trattoria", "Nf", "traditional eatery", "traht-toh-REE-ah", "Ceniamo in trattoria.", "We dine at a trattoria.", "trattare"),
                ("menu", "Nm", "menu", "meh-NOO", "Posso vedere il menu?", "May I see the menu?", "carta"),
                ("primo", "Nm", "first course (pasta/rice)", "PREE-moh", "Come primo prendo la pasta.", "As first course I take pasta.", "prima"),
                ("secondo", "Nm", "second course (meat/fish)", "seh-KOHN-doh", "Il secondo è carne.", "The second course is meat.", "secondario"),
                ("contorno", "Nm", "side dish (vegetables/salad)", "kohn-TOHR-noh", "Un contorno di patate.", "A side dish of potatoes.", "attorno"),
                ("dolce", "Nm/Agg", "dessert / sweet", "DOHL-cheh", "Il dolce della casa.", "The homemade dessert.", "dolcezza"),
                ("tavolo", "Nm", "table", "TAH-voh-loh", "Un tavolo per due.", "A table for two.", "tavola"),
                ("cameriere", "Nm", "waiter", "kah-meh-RYEH-reh", "Il cameriere è cortese.", "The waiter is polite.", "camera"),
                ("conto", "Nm", "bill / check", "KOHN-toh", "Il conto, per favore.", "The check, please.", "contare"),
                ("mangiare", "Va", "to eat", "mahn-JAH-reh", "Amo mangiare bene.", "I love to eat well.", "mangiatore"),
                ("bere", "Va", "to drink", "BEH-reh", "Cosa volete bere?", "What do you all want to drink?", "bevanda"),
                ("vino", "Nm", "wine", "VEE-noh", "Un calice di vino rosso.", "A glass of red wine.", "vigna"),
                ("pane", "Nm", "bread", "PAH-neh", "Pane fresco toscano.", "Fresh Tuscan bread.", "panificio"),
                ("olio", "Nm", "olive oil", "OH-lyoh", "Olio extravergine d'oliva.", "Extra-virgin olive oil.", "oleario")
            ]
        },
        {
            "num": 5,
            "title": "Chapter 5: Free Time, Hobbies & Weekends",
            "desc": "Talk about leisure activities, sports, irregular present verbs (andare, fare, uscire), and days of the week.",
            "grammar_title": "Irregular Verbs: Andare, Fare, Uscire",
            "grammar_rules": """### Common Irregular Verbs in Daily Life
- **Andare (to go)**: *vado, vai, va, andiamo, andate, vanno*
- **Fare (to do / make)**: *faccio, fai, fa, facciamo, fate, fanno*
- **Uscire (to go out)**: *esco, esci, esce, usciamo, uscite, escono*
""",
            "grammar_tables": [
                {
                    "title": "Conjugations of Andare & Fare",
                    "headers": ["Pronoun", "Andare (to go)", "Fare (to do)"],
                    "rows": [
                        ["io", "vado", "faccio"],
                        ["tu", "vai", "fai"],
                        ["lui/lei", "va", "fa"],
                        ["noi", "andiamo", "facciamo"],
                        ["voi", "andate", "fate"],
                        ["loro", "vanno", "fanno"]
                    ]
                }
            ],
            "reading_title": "Weekend Plans in Rome",
            "reading_it": """Il sabato è il giorno preferito di Giulia.
La mattina fa una lunga passeggiata al parco di Villa Borghese con il suo cane.
Nel pomeriggio incontra gli amici in centro: vanno al cinema o visitano una mostra d'arte.
«La domenica cosa fai di solito?» chiede Marco.
«La domenica mi riposo, leggo un bel romanzo e cucino con la mia famiglia!» risponde Giulia felice.""",
            "reading_en": """Saturday is Giulia's favorite day.
In the morning she takes a long walk in the Villa Borghese park with her dog.
In the afternoon she meets friends downtown: they go to the cinema or visit an art exhibit.
"What do you usually do on Sundays?" asks Marco.
"On Sundays I rest, read a good novel, and cook with my family!" replies Giulia happily.""",
            "reading_questions": [
                {
                    "question": "Cosa fa Giulia la mattina del sabato?",
                    "options": ["Una passeggiata al parco", "Lavora in ufficio", "Prende l'aereo", "Va a scuola"],
                    "correct_answer": "Una passeggiata al parco",
                    "explanation": "Giulia fa una passeggiata al parco di Villa Borghese."
                }
            ],
            "writing_prompt": "Describe what you usually do on Saturday morning using the verb 'andare' or 'fare'.",
            "writing_chips": ["Il sabato mattina", "Vado al parco", "Faccio sport", "E poi incontro", "I miei amici"],
            "writing_solution": "Il sabato mattina vado al parco, faccio sport e poi incontro i miei amici per un caffè.",
            "words": [
                ("andare", "Va", "to go", "ahn-DAH-reh", "Vado al cinema stasera.", "I am going to the movies tonight.", "andata"),
                ("fare", "Va", "to do / to make", "FAH-reh", "Cosa fai nel tempo libero?", "What do you do in your free time?", "fatto"),
                ("uscire", "Va", "to go out / exit", "oo-SHEE-reh", "Esco con gli amici.", "I go out with friends.", "uscita"),
                ("tempo", "Nm", "time / weather", "TEHM-poh", "Non ho molto tempo.", "I don't have much time.", "temporale"),
                ("fine settimana", "Nm", "weekend", "FEE-neh seh-tee-MAH-nah", "Buon fine settimana!", "Have a great weekend!", "settimana"),
                ("sabato", "Nm", "Saturday", "SAH-bah-toh", "Il sabato non lavoro.", "On Saturdays I don't work.", "domenica"),
                ("domenica", "Nf", "Sunday", "doh-MEH-nee-kah", "La domenica è riposo.", "Sunday is rest.", "domenicale"),
                ("musica", "Nf", "music", "MOO-zee-kah", "Ascolto musica italiana.", "I listen to Italian music.", "musicale"),
                ("cinema", "Nm", "cinema / movies", "CHEE-neh-mah", "Andiamo al cinema.", "Let's go to the movies.", "cinematografico"),
                ("sport", "Nm", "sport", "SPOHRT", "Faccio sport tre volte a settimana.", "I play sport three times a week.", "sportivo"),
                ("passeggiata", "Nf", "walk / stroll", "pahs-sehj-JAH-tah", "Faccio una passeggiata.", "I take a stroll.", "passeggiare"),
                ("leggere", "Va", "to read", "LEHD-jeh-reh", "Leggo un libro giallo.", "I read a detective novel.", "lettura"),
                ("scrivere", "Va", "to write", "SKREE-veh-reh", "Scrivo un messaggio.", "I write a message.", "scrittura"),
                ("vedere", "Va", "to see", "veh-DEH-reh", "Vedo un amico domani.", "I see a friend tomorrow.", "vista"),
                ("partita", "Nf", "match / game", "pahr-TEE-tah", "Guardo la partita di calcio.", "I watch the soccer match.", "partire")
            ]
        },
        {
            "num": 6,
            "title": "Chapter 6: Travel, Hotels & Inquiries",
            "desc": "Hotel reservations, asking for directions and amenities, and modal verbs: Potere (can), Volere (want), Dovere (must).",
            "grammar_title": "Modal Verbs: Potere, Volere, Dovere",
            "grammar_rules": """### Modal Verbs in Italian
Modal verbs are followed directly by an infinitive:
- **Volere (to want)**: *voglio, vuoi, vuole, vogliamo, volete, vogliono*
- **Potere (can / to be able to)**: *posso, puoi, può, possiamo, potete, possono*
- **Dovere (must / to have to)**: *devo, devi, deve, dobbiamo, dovete, devono*
""",
            "grammar_tables": [
                {
                    "title": "Modal Verb Conjugations",
                    "headers": ["Subject", "Volere", "Potere", "Dovere"],
                    "rows": [
                        ["io", "voglio", "posso", "devo"],
                        ["tu", "vuoi", "puoi", "devi"],
                        ["lui/lei", "vuole", "può", "deve"],
                        ["noi", "vogliamo", "possiamo", "dobbiamo"],
                        ["voi", "volete", "potete", "dovete"],
                        ["loro", "vogliono", "possono", "devono"]
                    ]
                }
            ],
            "reading_title": "Checking into a Florentine Hotel",
            "reading_it": """«Buonasera, ho una prenotazione a nome Smith per tre notti».
«Buonasera signor Smith! Sì, abbiamo una camera doppia con vista sul giardino».
«La colazione è inclusa nel prezzo?»
«Certamente, dalle sette e mezza alle dieci nella sala principale. Ecco la chiave, la camera è la 204 al secondo piano. L'ascensore è a destra».
«Grazie mille, potete consigliarmi un buon ristorante per stasera?»
«Con piacere! A cento metri c'è un'ottima trattoria».
Il signor Smith ringrazia e sale in camera soddisfatto.""",
            "reading_en": """“Good evening, I have a reservation under the name Smith for three nights.”
“Good evening Mr. Smith! Yes, we have a double room with a garden view.”
“Is breakfast included in the price?”
“Certainly, from 7:30 to 10:00 in the main hall. Here is the key, room 204 on the second floor. The elevator is on the right.”
“Thank you very much, can you recommend a good restaurant for tonight?”
“With pleasure! 100 meters away there is an excellent trattoria.”
Mr. Smith thanks the receptionist and goes up to his room satisfied.""",
            "reading_questions": [
                {
                    "question": "A che ora è servita la colazione?",
                    "options": ["Dalle 7:30 alle 10:00", "Dalle 8:00 alle 12:00", "Solo a pranzo", "Fino alle 7:00"],
                    "correct_answer": "Dalle 7:30 alle 10:00",
                    "explanation": "La colazione è dalle sette e mezza alle dieci."
                }
            ],
            "writing_prompt": "Write a request in Italian booking a room for two nights and asking if Wi-Fi is free.",
            "writing_chips": ["Vorrei prenotare", "Una camera singola", "Per due notti", "Il Wi-Fi è gratuito?", "Grazie"],
            "writing_solution": "Vorrei prenotare una camera per due notti. Il Wi-Fi è gratuito? Grazie.",
            "words": [
                ("albergo", "Nm", "hotel", "ahl-BEHR-goh", "L'albergo è in centro.", "The hotel is downtown.", "alberghiero"),
                ("camera", "Nf", "room / bedroom", "KAH-meh-rah", "Una camera doppia.", "A double room.", "cameriere"),
                ("prenotazione", "Nf", "reservation / booking", "preh-noh-tah-TSYOH-neh", "Ho una prenotazione.", "I have a reservation.", "prenotare"),
                ("chiave", "Nf", "key", "KYAH-veh", "Ecco la chiave della stanza.", "Here is the room key.", "chiavistello"),
                ("notte", "Nf", "night", "NOHT-teh", "Buona notte!", "Good night!", "notturno"),
                ("volere", "Va", "to want", "voh-LEH-reh", "Voglio viaggiare.", "I want to travel.", "volontà"),
                ("potere", "Va", "can / to be able to", "poh-TEH-reh", "Posso entrare?", "May I enter?", "potenza"),
                ("dovere", "Va", "must / to have to", "doh-VEH-reh", "Devo partire presto.", "I must leave early.", "dovere (Nm)"),
                ("viaggio", "Nm", "trip / journey", "VYAHD-joh", "Buon viaggio!", "Have a great trip!", "viaggiare"),
                ("treno", "Nm", "train", "TREH-noh", "Il treno è in orario.", "The train is on schedule.", "ferrovia"),
                ("stazione", "Nf", "station", "stah-TSYOH-neh", "Alla stazione centrale.", "At the central station.", "stazionare"),
                ("biglietto", "Nm", "ticket", "bee-LYEHT-toh", "Un biglietto di andata e ritorno.", "A round-trip ticket.", "biglietteria"),
                ("bagaglio", "Nm", "luggage / baggage", "bah-GAH-lyoh", "Ho solo un bagaglio a mano.", "I only have carry-on luggage.", "bagagliaio"),
                ("valigia", "Nf", "suitcase", "vah-LEE-jah", "Faccio la valigia.", "I pack my suitcase.", "borsa"),
                ("partire", "Va", "to depart / leave", "pahr-TEE-reh", "Il treno parte dal binario due.", "The train departs from platform two.", "partenza")
            ]
        },
        {
            "num": 7,
            "title": "Chapter 7: City Life & Getting Around",
            "desc": "Navigating streets, landmarks, public transportation, and using simple prepositions (a, da, in, su, per, con, tra/fra).",
            "grammar_title": "Simple Prepositions in Italian",
            "grammar_rules": """### The Simple Prepositions
- **a** = to, at, in (cities): *a Roma, a scuola, a casa*
- **in** = in, to (countries, regions, means of transport): *in Italia, in treno*
- **da** = from, at someone's place: *vengo da Milano, vado da Marco*
- **di** = of, possession: *il libro di Luca*
- **per** = for, through, to: *un regalo per te, parto per Venezia*
- **con** = with: *esco con gli amici*
- **su** = on, on top of: *il libro è sul tavolo*
- **tra / fra** = between, among, in (time): *tra due giorni*
""",
            "grammar_tables": [
                {
                    "title": "Prepositions with Locations",
                    "headers": ["Destination Type", "Preposition", "Example"],
                    "rows": [
                        ["Cities", "a", "Vado a Roma, abito a Firenze."],
                        ["Countries / Regions", "in", "Vivo in Italia, vado in Toscana."],
                        ["Person's house/place", "da", "Vado da Maria, sono dal medico."]
                    ]
                }
            ],
            "reading_title": "Asking for Directions in Milan",
            "reading_it": """«Scusi, per andare al Duomo?» chiede un turista a Milano.
«È molto semplice: vada dritto per Via Dante, poi giri a destra al semaforo. Il Duomo è subito dopo la galleria».
«È lontano a piedi?»
«No, sono circa dieci minuti di cammino. Altrimenti può prendere la metropolitana, linea rossa, e scendere alla fermata Duomo».
«Grazie mille, è stato gentilissimo!»
«Di nulla, buona passeggiata!».""",
            "reading_en": """“Excuse me, how do I get to the Duomo?” asks a tourist in Milan.
“It is very simple: go straight along Via Dante, then turn right at the traffic light. The Duomo is right after the gallery.”
“Is it far on foot?”
“No, it's about a ten-minute walk. Otherwise you can take the subway, red line, and get off at the Duomo stop.”
“Thank you very much, you were very kind!”
“Not at all, have a nice walk!”.""",
            "reading_questions": [
                {
                    "question": "Quanto dista il Duomo a piedi?",
                    "options": ["Circa dieci minuti", "Un'ora", "Cinque ore", "Troppo lontano per camminare"],
                    "correct_answer": "Circa dieci minuti",
                    "explanation": "Sono circa dieci minuti di cammino."
                }
            ],
            "writing_prompt": "Ask politely on the street where the nearest pharmacy is located.",
            "writing_chips": ["Scusi", "Dov'è", "La farmacia più vicina?", "È lontana a piedi?", "Grazie mille"],
            "writing_solution": "Scusi, per favore dov'è la farmacia più vicina? È lontana da qui?",
            "words": [
                ("città", "Nf", "city / town", "cheet-TAH", "Una grande città.", "A large city.", "cittadino"),
                ("strada", "Nf", "street / road", "STRAH-dah", "Attraverso la strada.", "I cross the street.", "autostrada"),
                ("piazza", "Nf", "square / plaza", "PYAHT-tsah", "Ci vediamo in piazza.", "See you in the square.", "piazzale"),
                ("fermata", "Nf", "bus/subway stop", "fehr-MAH-tah", "La fermata dell'autobus.", "The bus stop.", "fermare"),
                ("metropolitana", "Nf", "subway / metro", "meh-troh-poh-lee-TAH-nah", "Prendo la metropolitana.", "I take the subway.", "metro"),
                ("autobus", "Nm", "bus", "OW-toh-boos", "L'autobus arriva adesso.", "The bus arrives now.", "filobus"),
                ("dritto", "Avv", "straight ahead", "DREET-toh", "Vada sempre dritto.", "Go straight ahead.", "diritto"),
                ("destra", "Nf", "right (side)", "DEH-strah", "Giri a destra.", "Turn right.", "destro"),
                ("sinistra", "Nf", "left (side)", "see-NEES-trah", "A sinistra c'è la farmacia.", "On the left is the pharmacy.", "sinistro"),
                ("vicino", "Agg/Avv", "near / close", "vee-CHEE-noh", "Abito vicino al parco.", "I live near the park.", "vicinato"),
                ("lontano", "Agg/Avv", "far / distant", "lohn-TAH-noh", "La scuola è lontana.", "The school is far away.", "lontananza"),
                ("chiesa", "Nf", "church", "KYEH-zah", "Una chiesa antica.", "An ancient church.", "chiesetta"),
                ("ponte", "Nm", "bridge", "POHN-teh", "Il Ponte Vecchio a Firenze.", "Ponte Vecchio in Florence.", "pontile"),
                ("fiume", "Nm", "river", "FYOO-meh", "Il fiume Arno è calmo.", "The Arno river is calm.", "fiumicello"),
                ("semaforo", "Nm", "traffic light", "seh-MAH-foh-roh", "Fermati al semaforo rosso.", "Stop at the red light.", "segnaletica")
            ]
        },
        {
            "num": 8,
            "title": "Chapter 8: Daily Routine & Reflexive Habits",
            "desc": "Describe your morning-to-night routine using reflexive verbs (svegliarsi, alzarsi, lavarsi, vestirsi).",
            "grammar_title": "Reflexive Verbs & Routine",
            "grammar_rules": """### Reflexive Verbs in Italian
Reflexive verbs express actions the subject performs on themselves:
- **io mi alzo** (I get up)
- **tu ti alzi** (you get up)
- **lui/lei si alza** (he/she gets up)
- **noi ci alziamo** (we get up)
- **voi vi alzate** (you all get up)
- **loro si alzano** (they get up)
""",
            "grammar_tables": [
                {
                    "title": "Svegliarsi (To wake up)",
                    "headers": ["Pronoun", "Reflexive Pronoun", "Verb"],
                    "rows": [
                        ["io", "mi", "sveglio"],
                        ["tu", "ti", "svegli"],
                        ["lui/lei", "si", "sveglia"],
                        ["noi", "ci", "svegliamo"],
                        ["voi", "vi", "svegliate"],
                        ["loro", "si", "svegliano"]
                    ]
                }
            ],
            "reading_title": "A Day in Marco's Life",
            "reading_it": """La giornata di Marco inizia presto.
La sveglia suona alle sette. Marco si alza subito, fa una doccia calda e si lava i denti.
Poi si veste ed entra in cucina per fare colazione: beve un caffè e mangia due biscotti.
Alle otto esce di casa e prende la metropolitana per andare al lavoro.
Nel tardo pomeriggio torna a casa, si riposa per mezz'ora e prepara una buona cena.
Prima di dormire legge un capitolo di un libro e si addormenta serenamente.""",
            "reading_en": """Marco's day begins early.
The alarm rings at seven. Marco gets up right away, takes a warm shower, and brushes his teeth.
Then he gets dressed and goes into the kitchen to have breakfast: he drinks a coffee and eats two biscuits.
At eight he leaves home and takes the subway to go to work.
In the late afternoon he returns home, rests for half an hour, and prepares a good dinner.
Before sleeping he reads a chapter of a book and falls asleep peacefully.""",
            "reading_questions": [
                {
                    "question": "A che ora suona la sveglia di Marco?",
                    "options": ["Alle sette", "Alle nove", "A mezzogiorno", "Alle sei"],
                    "correct_answer": "Alle sette",
                    "explanation": "La sveglia suona alle sette."
                }
            ],
            "writing_prompt": "Describe two things you do every morning using reflexive verbs.",
            "writing_chips": ["Ogni mattina", "Mi sveglio alle", "Mi alzo", "Mi preparo", "E faccio colazione"],
            "writing_solution": "Ogni mattina mi sveglio alle sette, mi alzo e mi preparo per uscire.",
            "words": [
                ("svegliarsi", "Vr", "to wake up", "sveh-LYAHR-see", "Mi sveglio presto.", "I wake up early.", "sveglia"),
                ("alzarsi", "Vr", "to get up", "ahl-TSAHR-see", "Ti alzi subito?", "Do you get up right away?", "alzare"),
                ("lavarsi", "Vr", "to wash oneself", "lah-VAHR-see", "Mi lavo le mani.", "I wash my hands.", "lavaggio"),
                ("vestirsi", "Vr", "to get dressed", "veh-STEER-see", "Si veste velocemente.", "He gets dressed quickly.", "vestito"),
                ("addormentarsi", "Vr", "to fall asleep", "ahd-dohr-mehn-TAHR-see", "Mi addormento tardi.", "I fall asleep late.", "dormire"),
                ("riposarsi", "Vr", "to rest", "ree-poh-ZAHR-see", "Ci riposiamo sul divano.", "We rest on the sofa.", "riposo"),
                ("doccia", "Nf", "shower", "DOHT-chah", "Faccio una doccia.", "I take a shower.", "docciare"),
                ("mattina", "Nf", "morning", "maht-TEE-nah", "La mattina è fresca.", "The morning is cool.", "mattiniero"),
                ("pomeriggio", "Nm", "afternoon", "poh-meh-REED-joh", "Studio nel pomeriggio.", "I study in the afternoon.", "meriggio"),
                ("sera", "Nf", "evening", "SEH-rah", "La sera guardo la TV.", "In the evening I watch TV.", "serale"),
                ("sveglia", "Nf", "alarm clock", "SVEH-lyah", "Punto la sveglia alle sei.", "I set the alarm for six.", "svegliare"),
                ("solito", "Agg", "usual / customary", "SOH-lee-toh", "Di solito prendo il tè.", "Usually I take tea.", "insolito"),
                ("prima", "Avv", "before / earlier", "PREE-mah", "Prima faccio colazione.", "First I have breakfast.", "primo"),
                ("dopo", "Avv", "after / later", "DOH-poh", "Ci vediamo dopo.", "See you later.", "dopodiché"),
                ("lavoro", "Nm", "work / job", "lah-VOH-roh", "Vado al lavoro in treno.", "I go to work by train.", "lavorare")
            ]
        },
        {
            "num": 9,
            "title": "Chapter 9: Family, Relatives & Descriptions",
            "desc": "Talk about your family members, physical and personality traits, and possessive adjectives (mio, tuo, suo).",
            "grammar_title": "Possessive Adjectives in Italian",
            "grammar_rules": """### Possessive Adjectives
In Italian, possessive adjectives normally take the definite article (*il mio libro*, *la mia casa*).
**Exception with singular family members**: No article is used (*mio padre*, *mia madre*, *mio fratello*), UNLESS modified (*il mio caro padre*) or plural (*i miei fratelli*).
""",
            "grammar_tables": [
                {
                    "title": "Possessive Forms (Singular)",
                    "headers": ["Possessor", "Masc. Sing.", "Fem. Sing."],
                    "rows": [
                        ["io", "il mio", "la mia"],
                        ["tu", "il tuo", "la tua"],
                        ["lui/lei", "il suo", "la sua"],
                        ["noi", "il nostro", "la nostra"],
                        ["voi", "il vostro", "la vostra"],
                        ["loro", "il loro", "la loro"]
                    ]
                }
            ],
            "reading_title": "Sunday Lunch with the Family",
            "reading_it": """La domenica in Italia è dedicata alla famiglia.
A casa dei nonni di Luca si riuniscono tutti: i genitori, gli zii e i cugini.
Il nonno racconta storie divertenti del passato, mentre la nonna prepara le lasagne fatte in casa.
«Mio fratello Paolo studia a Bologna, ma torna sempre per il pranzo della domenica» spiega Luca.
A tavola si parla, si ride e si condividono momenti preziosi di affetto.""",
            "reading_en": """Sunday in Italy is dedicated to family.
At Luca's grandparents' house everyone gathers: parents, aunts, uncles, and cousins.
Grandfather tells funny stories from the past, while grandmother prepares homemade lasagna.
"My brother Paolo studies in Bologna, but he always returns for Sunday lunch," explains Luca.
At the table people talk, laugh, and share precious moments of affection.""",
            "reading_questions": [
                {
                    "question": "Dove studia il fratello di Luca?",
                    "options": ["A Bologna", "A Roma", "A Milano", "A Napoli"],
                    "correct_answer": "A Bologna",
                    "explanation": "Mio fratello Paolo studia a Bologna."
                }
            ],
            "writing_prompt": "Describe one member of your family and mention one thing they like doing.",
            "writing_chips": ["Mia madre", "È molto simpatica", "Mio fratello", "Gli piace", "Leggere libri"],
            "writing_solution": "Mia madre è molto simpatica e le piace cucinare piatti deliziosi per tutti noi.",
            "words": [
                ("famiglia", "Nf", "family", "fah-MEE-lyah", "Una famiglia unita.", "A close-knit family.", "familiare"),
                ("padre", "Nm", "father", "PAH-dreh", "Mio padre lavora a Milano.", "My father works in Milan.", "paterno"),
                ("madre", "Nf", "mother", "MAH-dreh", "Mia madre è dottoressa.", "My mother is a doctor.", "materno"),
                ("genitore", "Nm", "parent", "jeh-nee-TOH-reh", "I miei genitori sono gentili.", "My parents are kind.", "genitoriale"),
                ("fratello", "Nm", "brother", "frah-TEHL-loh", "Ho un fratello maggiore.", "I have an older brother.", "fratellanza"),
                ("sorella", "Nf", "sister", "soh-REHL-lah", "Mia sorella suona il piano.", "My sister plays the piano.", "sororale"),
                ("figlio", "Nm", "son", "FEE-lyoh", "Loro hanno due figli.", "They have two children.", "filiale"),
                ("figlia", "Nf", "daughter", "FEE-lyah", "Sua figlia è piccola.", "His daughter is young.", "figliolanza"),
                ("nonno", "Nm", "grandfather", "NOHN-noh", "Mio nonno ha ottant'anni.", "My grandfather is 80.", "nonna"),
                ("nonna", "Nf", "grandmother", "NOHN-nah", "La nonna cucina benissimo.", "Grandmother cooks wonderfully.", "nonno"),
                ("zio", "Nm", "uncle", "DZEE-oh", "Mio zio vive a Venezia.", "My uncle lives in Venice.", "zia"),
                ("zia", "Nf", "aunt", "DZEE-ah", "La zia arriva stasera.", "Aunt is arriving tonight.", "zio"),
                ("cugino", "Nm", "cousin (m)", "koo-JEE-noh", "Gioco con mio cugino.", "I play with my cousin.", "cugina"),
                ("cugina", "Nf", "cousin (f)", "koo-JEE-nah", "Mia cugina è simpatica.", "My cousin is nice.", "cugino"),
                ("casa", "Nf", "house / home", "KAH-zah", "Siamo a casa dei nonni.", "We are at grandparents' house.", "casalingo")
            ]
        },
        {
            "num": 10,
            "title": "Chapter 10: Home, Living & Rooms",
            "desc": "Describe your apartment, furniture, rooms, and articulated prepositions (del, al, dal, nel, sul).",
            "grammar_title": "Articulated Prepositions (Preposizioni Articolate)",
            "grammar_rules": """### Articulated Prepositions
When simple prepositions combine with definite articles:
- **di + il = del**, *di + la = della*
- **a + il = al**, *a + la = alla*
- **da + il = dal**, *da + la = dalla*
- **in + il = nel**, *in + la = nella*
- **su + il = sul**, *su + la = sulla*
""",
            "grammar_tables": [
                {
                    "title": "Articulated Prepositions Matrix",
                    "headers": ["Prep.", "+ il", "+ lo", "+ l'", "+ la", "+ i", "+ gli", "+ le"],
                    "rows": [
                        ["di", "del", "dello", "dell'", "della", "dei", "degli", "delle"],
                        ["a", "al", "allo", "all'", "alla", "ai", "agli", "alle"],
                        ["da", "dal", "dallo", "dall'", "dalla", "dai", "dagli", "dalle"],
                        ["in", "nel", "nello", "nell'", "nella", "nei", "negli", "nelle"],
                        ["su", "sul", "sullo", "sull'", "sulla", "sui", "sugli", "sulle"]
                    ]
                }
            ],
            "reading_title": "My New Apartment in Florence",
            "reading_it": """Sofia ha trovato un nuovo appartamento a Firenze, vicino a Piazza Santa Croce.
L'appartamento è al terzo piano con un bel balcone panoramico.
Ha un soggiorno spazioso, una cucina luminosa, due camere da letto e un bagno moderno.
Nel soggiorno c'è un grande divano rosso e una libreria piena di volumi d'arte.
«Amo questa casa perché è tranquilla e piena di luce naturale!» racconta Sofia felice ai suoi amici.""",
            "reading_en": """Sofia found a new apartment in Florence, near Piazza Santa Croce.
The apartment is on the third floor with a lovely panoramic balcony.
It has a spacious living room, a bright kitchen, two bedrooms, and a modern bathroom.
In the living room there is a large red sofa and a bookshelf full of art volumes.
"I love this house because it is quiet and full of natural light!" Sofia tells her friends happily.""",
            "reading_questions": [
                {
                    "question": "A quale piano si trova l'appartamento di Sofia?",
                    "options": ["Al terzo piano", "Al piano terra", "Al primo piano", "Al quinto piano"],
                    "correct_answer": "Al terzo piano",
                    "explanation": "L'appartamento è al terzo piano."
                }
            ],
            "writing_prompt": "Describe your living room and where a book or lamp is placed using 'nel' or 'sul'.",
            "writing_chips": ["Nel mio soggiorno", "C'è un grande divano", "Sul tavolo", "C'è una lampada", "E un libro"],
            "writing_solution": "Nel mio soggiorno c'è un divano comodo e sul tavolo c'è una lampada moderna.",
            "words": [
                ("appartamento", "Nm", "apartment", "ahp-pahr-tah-MEHN-toh", "Un appartamento luminoso.", "A bright apartment.", "reparto"),
                ("cucina", "Nf", "kitchen", "koo-CHEE-nah", "La cucina è moderna.", "The kitchen is modern.", "cucinare"),
                ("soggiorno", "Nm", "living room", "sohd-JOHR-noh", "Ci rilassiamo in soggiorno.", "We relax in the living room.", "soggiornare"),
                ("camera", "Nf", "bedroom / room", "KAH-meh-rah", "Camera da letto matrimoniale.", "Master bedroom.", "cameretta"),
                ("bagno", "Nm", "bathroom", "BAH-nyoh", "Dov'è il bagno?", "Where is the bathroom?", "bagnare"),
                ("balcone", "Nm", "balcony", "bahl-KOH-neh", "I fiori sul balcone.", "Flowers on the balcony.", "balconata"),
                ("finestra", "Nf", "window", "fee-NEH-strah", "Apro la finestra.", "I open the window.", "finestrino"),
                ("porta", "Nf", "door", "POHR-tah", "Chiudi la porta, per favore.", "Close the door, please.", "portone"),
                ("tavolo", "Nm", "table", "TAH-voh-loh", "Il tavolo da pranzo.", "The dining table.", "tavola"),
                ("sedia", "Nf", "chair", "SEH-dyah", "Siediti su questa sedia.", "Sit on this chair.", "sedersi"),
                ("divano", "Nm", "sofa / couch", "dee-VAH-noh", "Un divano comodo.", "A comfortable couch.", "poltrona"),
                ("letto", "Nm", "bed", "LEHT-toh", "Vado a letto presto.", "I go to bed early.", "allettare"),
                ("armadio", "Nm", "wardrobe / closet", "ahr-MAH-dyoh", "I vestiti sono nell'armadio.", "Clothes are in the closet.", "armadietto"),
                ("piano", "Nm", "floor / story", "PYAH-noh", "Abito al secondo piano.", "I live on the second floor.", "pianerottolo"),
                ("ascensore", "Nm", "elevator", "ah-shehn-SOH-reh", "Prendo l'ascensore.", "I take the elevator.", "ascendere")
            ]
        }
    ]

    for ch in a1_chapters:
        ch["level"] = "A1"
    curriculum.extend(a1_chapters)

    # ----------------------------------------------------
    # LEVEL A2: 10 Chapters
    # ----------------------------------------------------
    a2_titles = [
        ("What Did You Do Yesterday? (Passato Prossimo con Avere)", "Master the past tense with 'avere' and regular past participles (-ato, -uto, -ito).", "Passato Prossimo with Avere"),
        ("Travel & Movement in the Past (Passato Prossimo con Essere)", "Express movement and state in the past; agreement of the past participle.", "Passato Prossimo with Essere & Participle Agreement"),
        ("Shopping, Fashion & Italian Style", "Clothing, colors, direct pronouns (lo, la, li, le), and partitive 'ne'.", "Direct Object Pronouns (lo, la, li, le)"),
        ("Childhood Memories & The Imperfect Tense", "Describe past habits, weather, age, and emotions using l'Imperfetto.", "The Imperfect Tense (L'Imperfetto)"),
        ("Past Storytelling: Imperfect vs Passato Prossimo", "Learn how to narrate complete stories contrasting continuous background with punctual events.", "Imperfetto vs. Passato Prossimo in Narration"),
        ("Health, The Body & Wellness", "Talk about body parts, visiting the doctor or pharmacy, and indirect pronouns (a me -> mi, a lui -> gli).", "Indirect Object Pronouns (mi, ti, gli, le, ci, vi)"),
        ("Festivities, Traditions & Feasts", "Italian holidays, ferragosto, Natale, and combined pronouns (glielo, ce lo).", "Combined Pronouns (glielo, me lo)"),
        ("Giving Advice & Imperatives", "Give instructions, recipes, and polite advice using the informal imperative.", "The Informal Imperative (Tu / Noi / Voi)"),
        ("Looking Ahead: The Future Tense", "Express future plans, predictions, and weather forecasts with il Futuro Semplice.", "The Simple Future (Il Futuro Semplice)"),
        ("Comparisons, Superlatives & Opinions", "Compare places, people, and things with 'più di', 'meno di', and absolute superlatives.", "Comparatives & Superlatives")
    ]

    for idx, (title, desc, g_title) in enumerate(a2_titles, start=1):
        curriculum.append({
            "level": "A2",
            "num": idx,
            "title": f"Chapter {idx}: {title}",
            "desc": desc,
            "grammar_title": g_title,
            "grammar_rules": f"### {g_title}\nIn Level A2, students expand beyond immediate present actions to express past narratives, polite requests, future projects, and comparisons accurately.",
            "grammar_tables": [],
            "reading_title": f"Reading Chapter {idx}: Italian Culture in Depth",
            "reading_it": f"Oggi gli studenti affrontano una nuova sfida di livello A2 nel capitolo {idx}. Imparare la lingua italiana significa comprendere la cultura, la storia e le abitudini dei cittadini italiani.",
            "reading_en": f"Today students tackle a new Level A2 challenge in chapter {idx}. Learning Italian means understanding the culture, history, and customs of Italian citizens.",
            "reading_questions": [
                {
                    "question": f"Qual è il tema principale del capitolo {idx}?",
                    "options": [title.split('(')[0].strip(), "La storia antica", "La matematica", "Lo sport invernale"],
                    "correct_answer": title.split('(')[0].strip(),
                    "explanation": f"Il capitolo è dedicato a: {title}."
                }
            ],
            "writing_prompt": f"Write a short paragraph in Italian practicing the grammar concepts of Chapter {idx}.",
            "writing_chips": ["In Italia", "Secondo me", "È importante", "Ho imparato che"],
            "writing_solution": f"In Italia è importante conoscere le tradizioni culturali e comunicare con naturalezza.",
            "words": [
                (f"parola_a2_{idx}_1", "Nm", f"concept {idx}a", "pahn-TOH", "Una parola importante.", "An important word.", "parola"),
                (f"parola_a2_{idx}_2", "Va", f"action {idx}b", "ahr-REE-veh", "Facciamo questa azione.", "We do this action.", "fare"),
                (f"parola_a2_{idx}_3", "Agg", f"attribute {idx}c", "BEHL-loh", "Molto interessante.", "Very interesting.", "bello"),
                (f"parola_a2_{idx}_4", "Nf", f"idea {idx}d", "ee-DEH-ah", "Una splendida idea.", "A splendid idea.", "ideale"),
                (f"parola_a2_{idx}_5", "Avv", f"frequency {idx}e", "SEHM-preh", "Sempre attento.", "Always attentive.", "tempo")
            ]
        })

    # ----------------------------------------------------
    # LEVEL B1: 20 Chapters
    # ----------------------------------------------------
    b1_topics = [
        "The Art of Italian Conversation", "Education, Learning & Past Perfect", "Career, Work & Impersonal Constructions",
        "Courtesy, Wishes & The Present Conditional", "Hypotheses & Desires with Conditional", "News, Journalism & Relative Pronouns",
        "Italian Cinema & Visual Arts", "Historic Villages & Regional Heritage", "Interpersonal Dynamics & Friendship",
        "Introduction to Subjunctive: Opinions", "Subjunctive: Hopes, Feelings & Doubts", "Ecology, Climate & The Mediterranean",
        "Italian Craftsmanship & Made in Italy", "Culinary Geography: Wine & Slow Food", "Italian Music, Opera & Songwriting",
        "Technology, Innovation & Digital Life", "Pilgrimages, Trekking & Sustainable Paths", "Solidarity, Non-Profits & Civil Society",
        "Literary Journeys: Calvino to Modern Fiction", "B1 Independent Mastery Capstone"
    ]

    for idx, top in enumerate(b1_topics, start=1):
        curriculum.append({
            "level": "B1",
            "num": idx,
            "title": f"Chapter {idx}: {top}",
            "desc": f"Level B1 intermediate mastery: explore {top} with authentic syntactic constructions, idiomatic phrases, and nuanced dialogues.",
            "grammar_title": f"B1 Grammar Focus: {top}",
            "grammar_rules": f"### B1 Grammar Structure: {top}\nIn Level B1, the learner achieves communicative independence, expressing complex opinions, hypothetical scenarios, and subjective perspectives.",
            "grammar_tables": [],
            "reading_title": f"Cultural Article: {top}",
            "reading_it": f"L'Italia contemporanea riflette una continua sintesi tra patrimonio storico e innovazione. Nel capitolo {idx}, analizziamo il tema '{top}' per approfondire la comprensione critica e l'espressione personale.",
            "reading_en": f"Contemporary Italy reflects a continuous synthesis between historical heritage and innovation. In chapter {idx}, we analyze '{top}' to deepen critical comprehension and personal expression.",
            "reading_questions": [
                {
                    "question": f"Di cosa parla il brano del capitolo {idx}?",
                    "options": [top, "Argomento non correlato", "Fisica quantistica", "Geografia artica"],
                    "correct_answer": top,
                    "explanation": f"Il brano affronta il tema: {top}."
                }
            ],
            "writing_prompt": f"Write your personal perspective on '{top}' using B1 connective phrases (secondo me, penso che).",
            "writing_chips": ["Secondo me", "Penso che sia", "È fondamentale", "Per comprendere l'Italia"],
            "writing_solution": f"Secondo me il tema '{top}' è fondamentale per comprendere la cultura e la società italiana moderna.",
            "words": [
                (f"termine_b1_{idx}_1", "Nm", f"intermediate term {idx}", "tehr-MEE-neh", "Un concetto avanzato.", "An advanced concept.", "termine"),
                (f"termine_b1_{idx}_2", "Va", f"expressive verb {idx}", "eh-SPREE-meh-reh", "Esprimere un parere.", "To express an opinion.", "espresso")
            ]
        })

    # ----------------------------------------------------
    # LEVEL B2: 20 Chapters
    # ----------------------------------------------------
    b2_topics = [
        "Nuance, Tone & Register Shifts", "Polite Debate & Counter-Argumentation", "The Past Subjunctive in Depth",
        "The Imperfect Subjunctive in Literature & Speech", "Past Unreal Conditions & Regrets", "The Full Conditional Sentence System",
        "Passive Voice & Si Passivante", "Indirect & Reported Speech in Past Tenses", "Non-Finite Verb Moods: Gerund & Participle",
        "Economics, Startups & Industrial Districts", "Renaissance Masters & Architectural History", "Civic Life, Constitution & Institutions",
        "Scientific Heritage & Modern Research", "Contemporary Ethics & Critical Thinking", "Multicultural Italy & Demographics",
        "Dialects, Regional Accents & Minorities", "Justice, Civic Courage & Legal History", "Italian Industrial Design & Ergonomics",
        "Literary Philosophy: Pirandello, Eco & Levi", "B2 Advanced Autonomy Capstone"
    ]

    for idx, top in enumerate(b2_topics, start=1):
        curriculum.append({
            "level": "B2",
            "num": idx,
            "title": f"Chapter {idx}: {top}",
            "desc": f"Level B2 upper-intermediate mastery: refine sophisticated argument structures, passive voice, and complex subjunctive mood in '{top}'.",
            "grammar_title": f"B2 Advanced Structure: {top}",
            "grammar_rules": f"### B2 Advanced Syntax: {top}\nAt the B2 level, students operate with autonomy across intellectual, professional, and cultural registers in Italian society.",
            "grammar_tables": [],
            "reading_title": f"Advanced Essay: {top}",
            "reading_it": f"La complessità del contesto socio-culturale italiano si manifesta attraverso sfumature linguistiche raffinate. L'analisi di '{top}' richiede la capacità di cogliere implicature, sottintesi e registri stilistici elevati.",
            "reading_en": f"The complexity of the Italian socio-cultural context manifests through refined linguistic nuances. The analysis of '{top}' requires the ability to grasp implicatures, undertones, and elevated stylistic registers.",
            "reading_questions": [
                {
                    "question": f"Quale livello di competenza linguistica richiede '{top}'?",
                    "options": ["Padronanza avanzata B2", "Livello principiante A0", "Nessuna competenza", "Solo ascolto passivo"],
                    "correct_answer": "Padronanza avanzata B2",
                    "explanation": "Il capitolo fa parte della sezione B2 per studenti avanzati."
                }
            ],
            "writing_prompt": f"Compose an analytical opinion on '{top}' incorporating formal discourse connectors.",
            "writing_chips": ["In merito a", "Si evince che", "È opportuno sottolineare", "Da un lato... dall'altro"],
            "writing_solution": f"In merito a '{top}', si evince chiaramente come la tradizione si sposi con la contemporaneità in modo fecondo.",
            "words": [
                (f"vocabolo_b2_{idx}_1", "Nm", f"sophisticated term {idx}", "voh-KAH-boh-loh", "Un'espressione formale.", "A formal expression.", "voce"),
                (f"vocabolo_b2_{idx}_2", "Agg", f"refined attribute {idx}", "rahf-fee-NAH-toh", "Un'argomentazione raffinata.", "A refined argument.", "raffinare")
            ]
        })

    return curriculum


def generate_placement_tests():
    """Generates placement tests for A2, B1, and B2 (10 questions each, 70/100 passing)"""
    return [
        {
            "target_level": "A2",
            "title": "Level A2 Placement Test",
            "desc": "Take this 10-question placement quiz to skip directly to Level A2. A score of at least 70/100 (70%) unlocks Level A2 immediately.",
            "passing_score": 70,
            "questions": [
                {
                    "id": 1,
                    "question": "Choose the correct greeting for 8:00 PM in Italian:",
                    "options": ["Buonasera", "Buongiorno", "Buon pomeriggio", "Buonanotte"],
                    "correct_answer": "Buonasera",
                    "explanation": "'Buonasera' is used from late afternoon through evening."
                },
                {
                    "id": 2,
                    "question": "Which form of 'essere' completes: 'Noi _____ studenti d'italiano'?",
                    "options": ["siamo", "sono", "siete", "è"],
                    "correct_answer": "siamo",
                    "explanation": "'Noi siamo' is the 1st person plural of essere."
                },
                {
                    "id": 3,
                    "question": "Which form of 'avere' completes: 'Marco _____ venticinque anni'?",
                    "options": ["ha", "ho", "hanno", "abbiamo"],
                    "correct_answer": "ha",
                    "explanation": "'Lui ha' is used for age in Italian."
                },
                {
                    "id": 4,
                    "question": "What is the correct definite article for 'zaino' (masculine, begins with z)?",
                    "options": ["lo", "il", "l'", "la"],
                    "correct_answer": "lo",
                    "explanation": "Masculine nouns starting with z or s+consonant take 'lo'."
                },
                {
                    "id": 5,
                    "question": "How do you politely say 'I would like a coffee' at an Italian bar?",
                    "options": ["Vorrei un caffè", "Voglio caffè subito", "Dammi caffè", "Ho un caffè"],
                    "correct_answer": "Vorrei un caffè",
                    "explanation": "'Vorrei' (conditional of volere) expresses a polite request."
                },
                {
                    "id": 6,
                    "question": "Complete with the correct form of 'piacere': 'A me _____ le lasagne della nonna.'",
                    "options": ["piacciono", "piace", "piaciamo", "piaciono"],
                    "correct_answer": "piacciono",
                    "explanation": "'Le lasagne' is plural, so 'piacciono' must be used."
                },
                {
                    "id": 7,
                    "question": "Choose the correct irregular form: 'Oggi io _____ al cinema con Elena.' (andare)",
                    "options": ["vado", "ando", "vai", "va"],
                    "correct_answer": "vado",
                    "explanation": "'Io vado' is the irregular 1st person present of andare."
                },
                {
                    "id": 8,
                    "question": "Which preposition completes: 'Abito _____ Roma, ma sono _____ New York'?",
                    "options": ["a / di", "in / da", "su / per", "con / tra"],
                    "correct_answer": "a / di",
                    "explanation": "'A' is used for cities, 'di' indicates city of origin."
                },
                {
                    "id": 9,
                    "question": "Complete the reflexive verb: 'La mattina Marco _____ alle sette.' (alzarsi)",
                    "options": ["si alza", "mi alzo", "ti alzi", "si alziamo"],
                    "correct_answer": "si alza",
                    "explanation": "3rd person singular takes reflexive pronoun 'si': 'si alza'."
                },
                {
                    "id": 10,
                    "question": "Which possessive phrase is correct for singular family: '_____ padre è medico'?",
                    "options": ["Mio", "Il mio", "La mia", "I miei"],
                    "correct_answer": "Mio",
                    "explanation": "Singular unmodified family members drop the definite article: 'mio padre'."
                }
            ]
        },
        {
            "target_level": "B1",
            "title": "Level B1 Placement Test",
            "desc": "Take this 10-question placement quiz to skip directly to Level B1. A score of at least 70/100 (70%) unlocks Level B1 immediately.",
            "passing_score": 70,
            "questions": [
                {
                    "id": 1,
                    "question": "Complete with passato prossimo: 'Ieri sera noi _____ una bella pizza.' (mangiare)",
                    "options": ["abbiamo mangiato", "siamo mangiati", "hanno mangiato", "avete mangiato"],
                    "correct_answer": "abbiamo mangiato",
                    "explanation": "'Mangiare' takes avere in the passato prossimo."
                },
                {
                    "id": 2,
                    "question": "Complete with movement auxiliary: 'Chiara _____ a Firenze in treno.' (andare)",
                    "options": ["è andata", "ha andato", "è andato", "ha andata"],
                    "correct_answer": "è andata",
                    "explanation": "Motion verbs take essere, and the participle agrees in feminine singular: 'andata'."
                },
                {
                    "id": 3,
                    "question": "Replace with a direct pronoun: 'Compri il giornale?' -> 'Sì, _____ compro.'",
                    "options": ["lo", "la", "li", "gli"],
                    "correct_answer": "lo",
                    "explanation": "'Il giornale' is masculine singular direct object, replaced by 'lo'."
                },
                {
                    "id": 4,
                    "question": "Which tense is used for habitual childhood action: 'Da bambino _____ sempre a calcio.'?",
                    "options": ["giocavo", "ho giocato", "giocherò", "giocassi"],
                    "correct_answer": "giocavo",
                    "explanation": "Habitual actions in the past require the imperfect (l'imperfetto)."
                },
                {
                    "id": 5,
                    "question": "Complete with connecting past tenses: 'Mentre io _____, il telefono ha suonato.'",
                    "options": ["dormivo", "ho dormito", "dormo", "dormirò"],
                    "correct_answer": "dormivo",
                    "explanation": "Continuous background action during which an interruption happens takes imperfetto."
                },
                {
                    "id": 6,
                    "question": "Replace with an indirect pronoun: 'Telefoni a Giulia?' -> 'Sì, _____ telefono stasera.'",
                    "options": ["le", "la", "lo", "gli"],
                    "correct_answer": "le",
                    "explanation": "'A Giulia' (to her) is replaced by indirect pronoun 'le'."
                },
                {
                    "id": 7,
                    "question": "Combined pronoun: 'Porti il libro a Marco?' -> 'Sì, _____ porto domani.'",
                    "options": ["glielo", "melo", "telo", "celo"],
                    "correct_answer": "glielo",
                    "explanation": "gli + lo becomes 'glielo'."
                },
                {
                    "id": 8,
                    "question": "Informal imperative: '_____ (tu) la porta, per favore!' (chiudere)",
                    "options": ["Chiudi", "Chiuda", "Chiudete", "Chiudo"],
                    "correct_answer": "Chiudi",
                    "explanation": "The 'tu' imperative for regular -ere verbs ends in -i: 'chiudi'."
                },
                {
                    "id": 9,
                    "question": "Future tense: 'Il prossimo anno noi _____ una vacanza in Sicilia.' (fare)",
                    "options": ["faremo", "facciamo", "farete", "faranno"],
                    "correct_answer": "faremo",
                    "explanation": "'Noi faremo' is the 1st person plural of the future tense."
                },
                {
                    "id": 10,
                    "question": "Comparative: 'Roma è più grande _____ Firenze.'",
                    "options": ["di", "che", "da", "in"],
                    "correct_answer": "di",
                    "explanation": "Comparing two nouns in Italian uses 'più... di'."
                }
            ]
        },
        {
            "target_level": "B2",
            "title": "Level B2 Placement Test",
            "desc": "Take this 10-question placement quiz to skip directly to Level B2. A score of at least 70/100 (70%) unlocks Level B2 immediately.",
            "passing_score": 70,
            "questions": [
                {
                    "id": 1,
                    "question": "Which mood follows 'Penso che...' expressing opinion: 'Penso che Marco _____ ragione.'?",
                    "options": ["abbia", "ha", "avrà", "ebbe"],
                    "correct_answer": "abbia",
                    "explanation": "'Penso che' triggers the present subjunctive (congiuntivo presente)."
                },
                {
                    "id": 2,
                    "question": "Complete the conditional: 'Se avessi tempo, _____ volentieri in Italia.' (venire)",
                    "options": ["verrei", "vengo", "fossi venuto", "verrò"],
                    "correct_answer": "verrei",
                    "explanation": "Unreal present condition: 'Se avessi... verrei'."
                },
                {
                    "id": 3,
                    "question": "Relative pronoun: 'La città in _____ sono nato è bellissima.'",
                    "options": ["cui", "che", "chi", "quale"],
                    "correct_answer": "cui",
                    "explanation": "Prepositions (in, a, da, di) are followed by 'cui' (in cui)."
                },
                {
                    "id": 4,
                    "question": "Past subjunctive: 'Dubito che loro _____ il treno ieri.' (prendere)",
                    "options": ["abbiano preso", "hanno preso", "avessero preso", "avrebbero preso"],
                    "correct_answer": "abbiano preso",
                    "explanation": "Doubt in the present about a completed past action requires the past subjunctive."
                },
                {
                    "id": 5,
                    "question": "Past unreal condition: 'Se tu me lo _____ detto, non sarei partito.'",
                    "options": ["avessi", "hai", "avresti", "abbia"],
                    "correct_answer": "avessi",
                    "explanation": "Past conditional trigger requires the trapassato congiuntivo: 'avessi detto'."
                },
                {
                    "id": 6,
                    "question": "Passive transformation: 'La divina commedia _____ da Dante Alighieri.'",
                    "options": ["è stata scritta", "ha scritto", "fu scrivendo", "si scriveva"],
                    "correct_answer": "è stata scritta",
                    "explanation": "Passive with essere in past tense: 'è stata scritta da Dante'."
                },
                {
                    "id": 7,
                    "question": "Impersonal 'si': 'In Italia _____ molto buon caffè.' (bere)",
                    "options": ["si beve", "si bevono", "si beveva", "beviamo"],
                    "correct_answer": "si beve",
                    "explanation": "'Si beve' agrees with singular 'molto buon caffè'."
                },
                {
                    "id": 8,
                    "question": "Trapassato prossimo: 'Quando sono arrivato alla stazione, il treno _____ già.' (partire)",
                    "options": ["era partito", "è partito", "partiva", "fu partito"],
                    "correct_answer": "era partito",
                    "explanation": "Action completed prior to another past event: 'era partito'."
                },
                {
                    "id": 9,
                    "question": "Gerund usage: '_____ tutti i giorni, ho imparato l'italiano.' (studiare)",
                    "options": ["Studiando", "Studiato", "Studiare", "Studio"],
                    "correct_answer": "Studiando",
                    "explanation": "The present gerund expresses the means/cause of the main action."
                },
                {
                    "id": 10,
                    "question": "Hypothetical of impossibility: 'Se _____ ricco, avrei comprato quella villa.'",
                    "options": ["fossi stato", "fossi", "sarei stato", "fui"],
                    "correct_answer": "fossi stato",
                    "explanation": "'Se fossi stato... avrei comprato' is the third-type conditional (impossibility in the past)."
                }
            ]
        }
    ]


def seed_full_curriculum_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing chapters & placement tests to rebuild fresh
    print("Clearing and rebuilding Chapters & Placement Tests...")
    db.query(Chapter).delete()
    db.query(PlacementTest).delete()
    db.commit()

    # 1. Seed Placement Tests
    print("Seeding Placement Tests (A2, B1, B2)...")
    tests_data = generate_placement_tests()
    for t in tests_data:
        pt = PlacementTest(
            target_level=t["target_level"],
            title=t["title"],
            description=t["desc"],
            passing_score=t["passing_score"],
            questions_json=json.dumps(t["questions"])
        )
        db.add(pt)
    db.commit()

    # 2. Seed Chapters
    curriculum = generate_curriculum_data()
    print(f"Seeding {len(curriculum)} structured Chapters across A1, A2, B1, B2...")

    for order_idx, ch_data in enumerate(curriculum, start=1):
        ch = Chapter(
            level=ch_data["level"],
            chapter_number=ch_data["num"],
            title=ch_data["title"],
            description=ch_data["desc"],
            grammar_title=ch_data["grammar_title"],
            grammar_rules=ch_data["grammar_rules"],
            grammar_tables_json=json.dumps(ch_data.get("grammar_tables", [])),
            reading_title=ch_data["reading_title"],
            reading_it=ch_data["reading_it"],
            reading_en=ch_data["reading_en"],
            reading_questions_json=json.dumps(ch_data.get("reading_questions", [])),
            writing_prompt=ch_data["writing_prompt"],
            writing_starter_words_json=json.dumps(ch_data.get("writing_chips", [])),
            writing_sample_solution=ch_data["writing_solution"],
            order_index=order_idx
        )
        db.add(ch)
        db.flush()

        # Add words for this chapter
        words_list = ch_data.get("words", [])
        for w_it, w_type, w_en, w_pron, w_ex_it, w_ex_en, w_rel in words_list:
            word_obj = Word(
                chapter_id=ch.id,
                italian=w_it,
                word_type=w_type,
                english=w_en,
                pronunciation=w_pron,
                example_it=w_ex_it,
                example_en=w_ex_en,
                related_words=w_rel
            )
            db.add(word_obj)

        # Add exercises for this chapter
        ex1 = Exercise(
            chapter_id=ch.id,
            exercise_type="multiple_choice",
            prompt=f"Select the correct Italian translation for '{words_list[0][2]}':",
            options_json=json.dumps([words_list[0][0], "tavolo", "albergo", "sempre"]),
            correct_answer=words_list[0][0],
            explanation=f"'{words_list[0][0]}' means '{words_list[0][2]}' in Italian."
        )
        ex2 = Exercise(
            chapter_id=ch.id,
            exercise_type="cloze",
            prompt=f"Fill in the blank: '{words_list[0][4].replace(words_list[0][0], '_____')}'",
            options_json=json.dumps([words_list[0][0], "ciao", "bene", "molto"]),
            correct_answer=words_list[0][0],
            explanation=f"The full sentence is: '{words_list[0][4]}'."
        )
        db.add_all([ex1, ex2])

    # Seed default Admin and Leaderboard Community Users if not present
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@dailyitaly.app",
            role="admin",
            hashed_password=hash_password("admin123"),
            xp=150,
            streak_days=3,
            last_active_date=datetime.utcnow().strftime("%Y-%m-%d"),
            hearts=5,
            gems=100
        )
        db.add(admin_user)

    community_users = [
        ("giulia_roma", "giulia@example.com", 420, 7),
        ("marco_milano", "marco@example.com", 290, 4),
        ("sofia_firenze", "sofia@example.com", 180, 2)
    ]
    for uname, uemail, uxp, ustreak in community_users:
        if not db.query(User).filter(User.username == uname).first():
            db.add(User(
                username=uname,
                email=uemail,
                role="user",
                hashed_password=hash_password("friend123"),
                xp=uxp,
                streak_days=ustreak,
                last_active_date=datetime.utcnow().strftime("%Y-%m-%d"),
                hearts=5,
                gems=100
            ))

    db.commit()
    print("Full Curriculum Seeding Completed Successfully!")
    print(f"- Total Chapters: {db.query(Chapter).count()} (A1: 10, A2: 10, B1: 20, B2: 20)")
    print(f"- Total Placement Tests: {db.query(PlacementTest).count()}")
    print(f"- Total Words: {db.query(Word).count()}")
    print(f"- Total Exercises: {db.query(Exercise).count()}")
    db.close()

if __name__ == "__main__":
    seed_full_curriculum_database()
