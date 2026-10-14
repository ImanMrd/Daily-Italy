import json
from datetime import datetime
from backend.app.database import engine, Base, SessionLocal
from backend.app.models.curriculum import Stage, Unit, Lesson, Word, Exercise
from backend.app.models.user import User
from backend.app.services.auth_service import hash_password

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if database already has stages
    if db.query(Stage).count() > 0:
        print("Database already populated. Skipping seed.")
        db.close()
        return

    print("Seeding database with Italian curriculum...")

    # Create default demo user / admin for testing
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


    # Demo friend accounts for leaderboard
    friend1 = User(
        username="giulia_roma",
        email="giulia@example.com",
        hashed_password=hash_password("friend123"),
        xp=420,
        streak_days=7,
        last_active_date=datetime.utcnow().strftime("%Y-%m-%d"),
        hearts=4,
        gems=180
    )
    friend2 = User(
        username="marco_milano",
        email="marco@example.com",
        hashed_password=hash_password("friend123"),
        xp=290,
        streak_days=4,
        last_active_date=datetime.utcnow().strftime("%Y-%m-%d"),
        hearts=5,
        gems=90
    )
    friend3 = User(
        username="sofia_firenze",
        email="sofia@example.com",
        hashed_password=hash_password("friend123"),
        xp=180,
        streak_days=2,
        last_active_date=datetime.utcnow().strftime("%Y-%m-%d"),
        hearts=3,
        gems=40
    )
    db.add_all([friend1, friend2, friend3])

    # STAGES DEFINITION
    stage1 = Stage(
        id=1,
        name="Fondamenta Essenziali",
        description="The first 500 core Italian words: foundational vocabulary for daily survival and basic conversation.",
        level="A1",
        order_index=1
    )
    stage2 = Stage(
        id=2,
        name="Vita Quotidiana",
        description="Words 501 to 1000: Express yourself with confidence in shops, travel, work, and social life.",
        level="A2",
        order_index=2
    )
    stage3 = Stage(
        id=3,
        name="Espansione & Famiglie di Parole",
        description="Words 1001 to 2000: Word families, derivations, idioms, and comprehensive grammar exercises.",
        level="B1",
        order_index=3
    )
    stage4 = Stage(
        id=4,
        name="Padronanza & Sfumature",
        description="Words 2001 to 3000: Nuanced expressions, literary vocabulary, and advanced phrase structures.",
        level="B2",
        order_index=4
    )
    db.add_all([stage1, stage2, stage3, stage4])
    db.flush()

    # --- STAGE 1 UNITS ---
    # Unit 1
    unit1 = Unit(
        stage_id=stage1.id,
        title="Primi Passi & La Casa",
        description="Core everyday words: living, home, simple adjectives, and essential actions.",
        grammar_title="Nota Bene: Italian Noun Genders & Articles",
        grammar_tip="In Italian, all nouns are either masculine or feminine. As a rule of thumb: nouns ending in -o are typically masculine (il ragazzo, il libro), while nouns ending in -a are typically feminine (la casa, l'acqua). Nouns ending in -e can be either and must be memorized with their article (il cane, la notte)!",
        order_index=1
    )
    # Unit 2
    unit2 = Unit(
        stage_id=stage1.id,
        title="Emozioni & Il Tempo Libero",
        description="Friendship, love, nature, and the fundamental verb 'Andare'.",
        grammar_title="Nota Bene: The Verb 'Andare' & Prepositions",
        grammar_tip="The verb 'Andare' (to go) is irregular in Italian: io vado, tu vai, lui/lei va, noi andiamo, voi andate, loro vanno. When heading to a city, use 'a' (vado a Roma), but when going to a country or region, use 'in' (vado in Italia)!",
        order_index=2
    )
    # Unit 3
    unit3 = Unit(
        stage_id=stage1.id,
        title="In Giro per la Città",
        description="Transport, navigation, time, and the vital verb 'Avere'.",
        grammar_title="Nota Bene: 'Avere' Idiomatic Expressions",
        grammar_tip="In Italian, many physical and emotional sensations are expressed with 'avere' (to have) instead of 'to be': 'ho fame' (I am hungry, literally I have hunger), 'ho sete' (I am thirsty), 'ho freddo' (I am cold), and 'ho 25 anni' (I am 25 years old).",
        order_index=3
    )
    # Unit 4
    unit4 = Unit(
        stage_id=stage1.id,
        title="Al Bar & Al Ristorante",
        description="Ordering food, drinks, compliments, and Italian dining etiquette.",
        grammar_title="Nota Bene: Ordering Like a Local",
        grammar_tip="When ordering in Italy, 'Un caffè' by default means a single espresso shot. To order politely, use 'Vorrei...' (I would like...) or simply the item followed by 'per favore' (e.g., 'Un bicchiere d'acqua, per favore').",
        order_index=4
    )
    db.add_all([unit1, unit2, unit3, unit4])
    db.flush()

    # --- LESSONS & 15-WORD SETS ---
    # Lesson 1 (Unit 1): 15 Words
    lesson1 = Lesson(unit_id=unit1.id, title="Le Parole di Partenza", order_index=1)
    db.add(lesson1)
    db.flush()

    words_l1 = [
        Word(lesson_id=lesson1.id, italian="abitare", word_type="Va", english="to live, to reside", pronunciation="ah-bee-TAH-reh", example_it="Io abito in centro a Milano.", example_en="I live in downtown Milan.", related_words="abitazione (Nf), abitante (Nm)"),
        Word(lesson_id=lesson1.id, italian="acqua", word_type="Nf", english="water", pronunciation="AHK-wah", example_it="Vorrei un bicchiere d'acqua naturale.", example_en="I would like a glass of still water.", related_words="acquatico (Agg), acquario (Nm)"),
        Word(lesson_id=lesson1.id, italian="adesso", word_type="Avv", english="now, at present", pronunciation="ah-DEHS-soh", example_it="Adesso dobbiamo andare.", example_en="Now we must go.", related_words="ora (Avv)"),
        Word(lesson_id=lesson1.id, italian="aeroplano", word_type="Nm", english="airplane (formal)", pronunciation="ah-eh-roh-PLAH-noh", example_it="L'aeroplano atterra alle cinque.", example_en="The airplane lands at five.", related_words="aereo (Nm), aeroportuale (Agg)"),
        Word(lesson_id=lesson1.id, italian="aereo", word_type="Nm", english="plane, airplane (common)", pronunciation="ah-EH-reh-oh", example_it="Prendo l'aereo per Roma domani.", example_en="I am taking the plane to Rome tomorrow.", related_words="aeroplano (Nm)"),
        Word(lesson_id=lesson1.id, italian="aeroporto", word_type="Nm", english="airport", pronunciation="ah-eh-roh-POR-toh", example_it="Ci vediamo all'aeroporto di Fiumicino.", example_en="See you at Fiumicino airport.", related_words="porto (Nm)"),
        Word(lesson_id=lesson1.id, italian="agosto", word_type="Nm", english="August", pronunciation="ah-GOHS-toh", example_it="In agosto molti italiani vanno in vacanza.", example_en="In August many Italians go on vacation.", related_words="estivo (Agg)"),
        Word(lesson_id=lesson1.id, italian="aiutare", word_type="Va", english="to help, to assist", pronunciation="ah-yoo-TAH-reh", example_it="Mi puoi aiutare con questo esercizio?", example_en="Can you help me with this exercise?", related_words="aiuto (Nm), aiutante (Nm)"),
        Word(lesson_id=lesson1.id, italian="albergo", word_type="Nm", english="hotel", pronunciation="ahl-BEHR-goh", example_it="Abbiamo prenotato una camera in albergo.", example_en="We booked a room in a hotel.", related_words="alberghiero (Agg)"),
        Word(lesson_id=lesson1.id, italian="albero", word_type="Nm", english="tree", pronunciation="AHL-beh-roh", example_it="L'albero nel giardino è pieno di fiori.", example_en="The tree in the garden is full of flowers.", related_words="alberato (Agg)"),
        Word(lesson_id=lesson1.id, italian="alto", word_type="Agg", english="tall, high", pronunciation="AHL-toh", example_it="Marco è un ragazzo molto alto.", example_en="Marco is a very tall boy.", related_words="altezza (Nf), alzare (Va)"),
        Word(lesson_id=lesson1.id, italian="altro", word_type="Agg", english="other, another", pronunciation="AHL-troh", example_it="Vuoi un altro caffè?", example_en="Do you want another coffee?", related_words="altrimenti (Avv)"),
        Word(lesson_id=lesson1.id, italian="alzare", word_type="Va", english="to raise, to lift", pronunciation="ahl-TSAH-reh", example_it="Puoi alzare il volume, per favore?", example_en="Can you raise the volume, please?", related_words="alzarsi (Vr)"),
        Word(lesson_id=lesson1.id, italian="alzarsi", word_type="Vr", english="to get up, to stand up", pronunciation="ahl-TSAHR-see", example_it="Mi alzo presto ogni mattina.", example_en="I get up early every morning.", related_words="alzare (Va)"),
        Word(lesson_id=lesson1.id, italian="amare", word_type="Va", english="to love", pronunciation="ah-MAH-reh", example_it="Amo la lingua e la cultura italiana.", example_en="I love the Italian language and culture.", related_words="amore (Nm), amante (Nm)")
    ]
    db.add_all(words_l1)

    # Exercises for Lesson 1
    ex_l1 = [
        Exercise(
            lesson_id=lesson1.id,
            exercise_type="multiple_choice",
            prompt="What is the Italian word for 'to live / to reside'?",
            options_json=json.dumps(["abitare", "aiutare", "alzare", "amare"]),
            correct_answer="abitare",
            explanation="'Abitare' means to live or reside (e.g. 'Io abito a Roma'). 'Aiutare' means to help."
        ),
        Exercise(
            lesson_id=lesson1.id,
            exercise_type="cloze",
            prompt="Complete the sentence: 'Marco è molto _____ e gioca a basket.' (tall)",
            options_json=json.dumps(["alto", "altro", "amaro", "antico"]),
            correct_answer="alto",
            explanation="'Alto' translates to tall/high. 'Altro' means other/another."
        ),
        Exercise(
            lesson_id=lesson1.id,
            exercise_type="matching",
            prompt="Match each Italian word with its English translation:",
            options_json=json.dumps({
                "acqua": "water",
                "albergo": "hotel",
                "adesso": "now",
                "albero": "tree"
            }),
            correct_answer="matched",
            explanation="Acqua = water, Albergo = hotel, Adesso = now, Albero = tree."
        ),
        Exercise(
            lesson_id=lesson1.id,
            exercise_type="odd_one_out",
            prompt="Which of the following is an ACTION (verb)?",
            options_json=json.dumps(["aiutare", "aeroporto", "agosto", "acqua"]),
            correct_answer="aiutare",
            explanation="'Aiutare' (to help) is a verb ending in -are. The others are nouns."
        )
    ]
    db.add_all(ex_l1)

    # Lesson 2 (Unit 2): 15 Words
    lesson2 = Lesson(unit_id=unit2.id, title="Emozioni & Compagnia", order_index=2)
    db.add(lesson2)
    db.flush()

    words_l2 = [
        Word(lesson_id=lesson2.id, italian="amaro", word_type="Agg", english="bitter", pronunciation="ah-MAH-roh", example_it="Questo caffè è molto amaro.", example_en="This coffee is very bitter.", related_words="amarezza (Nf)"),
        Word(lesson_id=lesson2.id, italian="ambasciata", word_type="Nf", english="embassy", pronunciation="ahm-bah-SHAH-tah", example_it="L'ambasciata si trova vicino al parco.", example_en="The embassy is located near the park.", related_words="ambasciatore (Nm)"),
        Word(lesson_id=lesson2.id, italian="amico", word_type="Nm", english="friend (male)", pronunciation="ah-MEE-koh", example_it="Luca è il mio migliore amico.", example_en="Luca is my best friend.", related_words="amica (Nf), amicizia (Nf)"),
        Word(lesson_id=lesson2.id, italian="amica", word_type="Nf", english="friend (female)", pronunciation="ah-MEE-kah", example_it="Elena è un'amica speciale.", example_en="Elena is a special friend.", related_words="amico (Nm), amichevole (Agg)"),
        Word(lesson_id=lesson2.id, italian="amore", word_type="Nm", english="love", pronunciation="ah-MOH-reh", example_it="L'amore vince sempre.", example_en="Love always wins.", related_words="amare (Va), amoroso (Agg)"),
        Word(lesson_id=lesson2.id, italian="anche", word_type="Cong", english="also, too, as well", pronunciation="AHN-keh", example_it="Anche io voglio imparare l'italiano.", example_en="I also want to learn Italian.", related_words="pure (Cong)"),
        Word(lesson_id=lesson2.id, italian="ancora", word_type="Avv", english="still, yet, again", pronunciation="ahn-KOH-rah", example_it="Sei ancora a casa?", example_en="Are you still at home?", related_words="ancorare (Va)"),
        Word(lesson_id=lesson2.id, italian="andare", word_type="Vr", english="to go", pronunciation="ahn-DAH-reh", example_it="Oggi andiamo al mare.", example_en="Today we are going to the sea.", related_words="andata (Nf)"),
        Word(lesson_id=lesson2.id, italian="animale", word_type="Nm", english="animal", pronunciation="ah-nee-MAH-leh", example_it="Il cane è un animale fedele.", example_en="The dog is a loyal animal.", related_words="animalesco (Agg)"),
        Word(lesson_id=lesson2.id, italian="anno", word_type="Nm", english="year", pronunciation="AHN-noh", example_it="Buon anno nuovo a tutti!", example_en="Happy New Year to everyone!", related_words="annuale (Agg), annata (Nf)"),
        Word(lesson_id=lesson2.id, italian="antico", word_type="Agg", english="ancient, old", pronunciation="ahn-TEE-koh", example_it="Roma ha molti monumenti antichi.", example_en="Rome has many ancient monuments.", related_words="antichità (Nf)"),
        Word(lesson_id=lesson2.id, italian="aperitivo", word_type="Nm", english="aperitif, pre-dinner drink", pronunciation="ah-peh-ree-TEE-voh", example_it="Prendiamo un aperitivo insieme stasera?", example_en="Shall we have an aperitif together this evening?", related_words="aprire (Va)"),
        Word(lesson_id=lesson2.id, italian="appartamento", word_type="Nm", english="apartment, flat", pronunciation="ahp-pahr-tah-MEHN-toh", example_it="L'appartamento è luminoso e spazioso.", example_en="The apartment is bright and spacious.", related_words="appartarsi (Vr)"),
        Word(lesson_id=lesson2.id, italian="aprile", word_type="Nm", english="April", pronunciation="ah-PREE-leh", example_it="In aprile il tempo comincia a scaldarsi.", example_en="In April the weather starts to warm up.", related_words="primavera (Nf)"),
        Word(lesson_id=lesson2.id, italian="aprire", word_type="Va", english="to open", pronunciation="ah-PREE-reh", example_it="Puoi aprire la finestra?", example_en="Can you open the window?", related_words="aperto (Agg), apertura (Nf)")
    ]
    db.add_all(words_l2)

    # Exercises for Lesson 2
    ex_l2 = [
        Exercise(
            lesson_id=lesson2.id,
            exercise_type="multiple_choice",
            prompt="Which Italian word means 'to go'?",
            options_json=json.dumps(["andare", "aprire", "amare", "abitare"]),
            correct_answer="andare",
            explanation="'Andare' means to go. In present tense: io vado, tu vai, noi andiamo."
        ),
        Exercise(
            lesson_id=lesson2.id,
            exercise_type="cloze",
            prompt="Fill in the blank: 'Roma è una città con molti edifici _____.' (ancient)",
            options_json=json.dumps(["antichi", "amari", "alti", "altri"]),
            correct_answer="antichi",
            explanation="'Antichi' is the masculine plural form of 'antico' (ancient/antique)."
        ),
        Exercise(
            lesson_id=lesson2.id,
            exercise_type="matching",
            prompt="Match the Italian social terms with their English meanings:",
            options_json=json.dumps({
                "amico": "friend (m)",
                "amore": "love",
                "aperitivo": "pre-dinner drink",
                "anno": "year"
            }),
            correct_answer="matched",
            explanation="Amico = friend, Amore = love, Aperitivo = pre-dinner drink, Anno = year."
        ),
        Exercise(
            lesson_id=lesson2.id,
            exercise_type="odd_one_out",
            prompt="Select the word that represents a MONTH of the year:",
            options_json=json.dumps(["aprile", "animale", "appartamento", "ancora"]),
            correct_answer="aprile",
            explanation="'Aprile' is April. The others are animal, apartment, and still/yet."
        )
    ]
    db.add_all(ex_l2)

    # Lesson 3 (Unit 3): 15 Words
    lesson3 = Lesson(unit_id=unit3.id, title="In Città & Mezzi", order_index=3)
    db.add(lesson3)
    db.flush()

    words_l3 = [
        Word(lesson_id=lesson3.id, italian="arancia", word_type="Nf", english="orange (fruit)", pronunciation="ah-RAHN-chah", example_it="Bevo una spremuta d'arancia fresca.", example_en="I drink a fresh orange juice.", related_words="arancione (Agg)"),
        Word(lesson_id=lesson3.id, italian="arrivare", word_type="Vr", english="to arrive", pronunciation="ahr-ree-VAH-reh", example_it="Il treno arriva al binario tre.", example_en="The train arrives at platform three.", related_words="arrivo (Nm)"),
        Word(lesson_id=lesson3.id, italian="arrivederci", word_type="Interiez", english="goodbye, see you again", pronunciation="ahr-ree-veh-DEHR-chee", example_it="Grazie mille e arrivederci!", example_en="Thank you very much and goodbye!", related_words="rivederci (Vr)"),
        Word(lesson_id=lesson3.id, italian="aspettare", word_type="Va", english="to wait, to await", pronunciation="ah-speht-TAH-reh", example_it="Aspetto l'autobus da venti minuti.", example_en="I have been waiting for the bus for 20 minutes.", related_words="attesa (Nf)"),
        Word(lesson_id=lesson3.id, italian="attenzione", word_type="Nf", english="attention, caution", pronunciation="aht-tehn-TSYOH-neh", example_it="Attenzione al gradino!", example_en="Watch out for the step! (Caution)", related_words="attento (Agg)"),
        Word(lesson_id=lesson3.id, italian="autobus", word_type="Nm", english="bus", pronunciation="OW-toh-boos", example_it="Prendiamo l'autobus numero 64.", example_en="Let's take bus number 64.", related_words="bus (Nm)"),
        Word(lesson_id=lesson3.id, italian="bus", word_type="Nm", english="bus (short form)", pronunciation="boos", example_it="Il bus è in ritardo.", example_en="The bus is late.", related_words="autobus (Nm)"),
        Word(lesson_id=lesson3.id, italian="automobile", word_type="Nf", english="car, automobile", pronunciation="ow-toh-MOH-bee-leh", example_it="L'automobile è parcheggiata fuori.", example_en="The car is parked outside.", related_words="auto (Nf)"),
        Word(lesson_id=lesson3.id, italian="auto", word_type="Nf", english="car (common)", pronunciation="OW-toh", example_it="Preferisco viaggiare in auto.", example_en="I prefer traveling by car.", related_words="automobile (Nf)"),
        Word(lesson_id=lesson3.id, italian="autunno", word_type="Nm", english="autumn, fall", pronunciation="ow-TOON-noh", example_it="Le foglie cadono in autunno.", example_en="Leaves fall in autumn.", related_words="autunnale (Agg)"),
        Word(lesson_id=lesson3.id, italian="avanti", word_type="Avv", english="forward, ahead, come in!", pronunciation="ah-VAHN-tee", example_it="Avanti, c'è posto!", example_en="Come in, there is room!", related_words="avanzare (Va)"),
        Word(lesson_id=lesson3.id, italian="avere", word_type="Va", english="to have", pronunciation="ah-VEH-reh", example_it="Ho una domanda importante.", example_en="I have an important question.", related_words="avere fame / sete"),
        Word(lesson_id=lesson3.id, italian="azzurro", word_type="Agg", english="light blue, sky blue", pronunciation="ahd-DZOOR-roh", example_it="Il cielo di oggi è completamente azzurro.", example_en="Today's sky is completely azure blue.", related_words="azzurrino (Agg)"),
        Word(lesson_id=lesson3.id, italian="baciare", word_type="Va", english="to kiss", pronunciation="bah-CHAH-reh", example_it="Si baciano per salutarsi.", example_en="They kiss to greet each other.", related_words="bacio (Nm)"),
        Word(lesson_id=lesson3.id, italian="bagno", word_type="Nm", english="bathroom, bath", pronunciation="BAHN-nyoh", example_it="Dov'è il bagno, per favore?", example_en="Where is the bathroom, please?", related_words="bagnare (Va)")
    ]
    db.add_all(words_l3)

    # Exercises for Lesson 3
    ex_l3 = [
        Exercise(
            lesson_id=lesson3.id,
            exercise_type="multiple_choice",
            prompt="How do you ask politely 'Where is the bathroom?' in Italian?",
            options_json=json.dumps(["Dov'è il bagno?", "Dov'è l'autobus?", "Dov'è l'arancia?", "Dov'è l'albergo?"]),
            correct_answer="Dov'è il bagno?",
            explanation="'Bagno' is bathroom. 'Dov'è il bagno, per favore?' is an essential phrase for every traveler."
        ),
        Exercise(
            lesson_id=lesson3.id,
            exercise_type="cloze",
            prompt="Complete: 'Il cielo è limpido e _____.' (sky-blue)",
            options_json=json.dumps(["azzurro", "arancia", "amaro", "antico"]),
            correct_answer="azzurro",
            explanation="'Azzurro' means sky-blue / light blue, the iconic color of the Italian national teams."
        ),
        Exercise(
            lesson_id=lesson3.id,
            exercise_type="matching",
            prompt="Match the vehicles and travel terms:",
            options_json=json.dumps({
                "autobus": "bus",
                "automobile": "car",
                "arrivare": "to arrive",
                "arrivederci": "goodbye"
            }),
            correct_answer="matched",
            explanation="Autobus = bus, Automobile = car, Arrivare = to arrive, Arrivederci = goodbye."
        ),
        Exercise(
            lesson_id=lesson3.id,
            exercise_type="odd_one_out",
            prompt="Find the FRUIT among these words:",
            options_json=json.dumps(["arancia", "autunno", "avanti", "aereo"]),
            correct_answer="arancia",
            explanation="'Arancia' is an orange (fruit). 'Autunno' is autumn, 'avanti' is forward, 'aereo' is airplane."
        )
    ]
    db.add_all(ex_l3)

    # Lesson 4 (Unit 4): 15 Words
    lesson4 = Lesson(unit_id=unit4.id, title="Al Bar & Al Ristorante", order_index=4)
    db.add(lesson4)
    db.flush()

    words_l4 = [
        Word(lesson_id=lesson4.id, italian="ballare", word_type="Va", english="to dance", pronunciation="bahl-LAH-reh", example_it="Mi piace ballare con gli amici.", example_en="I like dancing with friends.", related_words="ballo (Nm), ballerino (Nm)"),
        Word(lesson_id=lesson4.id, italian="bambino", word_type="Nm", english="child, little boy", pronunciation="bahm-BEE-noh", example_it="Il bambino gioca nel parco.", example_en="The child plays in the park.", related_words="bambina (Nf), infanzia (Nf)"),
        Word(lesson_id=lesson4.id, italian="bambina", word_type="Nf", english="child, little girl", pronunciation="bahm-BEE-nah", example_it="La bambina disegna una casa.", example_en="The little girl draws a house.", related_words="bambino (Nm)"),
        Word(lesson_id=lesson4.id, italian="banca", word_type="Nf", english="bank", pronunciation="BAHN-kah", example_it="La banca apre alle otto e mezza.", example_en="The bank opens at eight-thirty.", related_words="banchiere (Nm)"),
        Word(lesson_id=lesson4.id, italian="bar", word_type="Nm", english="cafe, bar", pronunciation="bahr", example_it="Prendiamo un caffè al bar.", example_en="Let's have a coffee at the cafe.", related_words="barista (Nm/f)"),
        Word(lesson_id=lesson4.id, italian="basso", word_type="Agg", english="short, low", pronunciation="BAHS-soh", example_it="Il soffitto della stanza è basso.", example_en="The ceiling of the room is low.", related_words="abbassare (Va)"),
        Word(lesson_id=lesson4.id, italian="bello", word_type="Agg", english="beautiful, handsome, nice", pronunciation="BEHL-loh", example_it="Che bella giornata di sole!", example_en="What a beautiful sunny day!", related_words="bellezza (Nf), abbellire (Va)"),
        Word(lesson_id=lesson4.id, italian="bene", word_type="Avv", english="well, good", pronunciation="BEH-neh", example_it="Sto molto bene, grazie!", example_en="I am doing very well, thank you!", related_words="benessere (Nm)"),
        Word(lesson_id=lesson4.id, italian="benzina", word_type="Nf", english="petrol, gasoline", pronunciation="behn-DZEE-nah", example_it="Dobbiamo fare benzina prima di partire.", example_en="We need to get gas before leaving.", related_words="benzinaio (Nm)"),
        Word(lesson_id=lesson4.id, italian="bere", word_type="Va", english="to drink", pronunciation="BEH-reh", example_it="Bevo un espresso al banco.", example_en="I drink an espresso at the counter.", related_words="bevanda (Nf), bevitore (Nm)"),
        Word(lesson_id=lesson4.id, italian="bianco", word_type="Agg", english="white", pronunciation="BYAHN-koh", example_it="Preferisco il vino bianco.", example_en="I prefer white wine.", related_words="bianchezza (Nf)"),
        Word(lesson_id=lesson4.id, italian="bicchiere", word_type="Nm", english="drinking glass", pronunciation="beek-KYEH-reh", example_it="Un bicchiere d'acqua frizzante, grazie.", example_en="A glass of sparkling water, thanks.", related_words="bottiglia (Nf)"),
        Word(lesson_id=lesson4.id, italian="binario", word_type="Nm", english="train platform, railway track", pronunciation="bee-NAH-ryoh", example_it="Il treno parte dal binario 4.", example_en="The train leaves from platform 4.", related_words="treno (Nm)"),
        Word(lesson_id=lesson4.id, italian="biondo", word_type="Agg", english="blonde, fair-haired", pronunciation="BYOHN-doh", example_it="Ha i capelli biondi e gli occhi chiari.", example_en="She has blonde hair and light eyes.", related_words="biondezza (Nf)"),
        Word(lesson_id=lesson4.id, italian="birra", word_type="Nf", english="beer", pronunciation="BEER-rah", example_it="Una birra alla spina, per favore.", example_en="A draught beer, please.", related_words="birrificio (Nm)")
    ]
    db.add_all(words_l4)

    # Exercises for Lesson 4
    ex_l4 = [
        Exercise(
            lesson_id=lesson4.id,
            exercise_type="multiple_choice",
            prompt="What is the opposite of 'alto' (tall/high)?",
            options_json=json.dumps(["basso", "bello", "bianco", "biondo"]),
            correct_answer="basso",
            explanation="'Basso' means short or low, which is the direct antonym of 'alto'."
        ),
        Exercise(
            lesson_id=lesson4.id,
            exercise_type="cloze",
            prompt="Fill in: 'In Italia si prende il caffè al _____ la mattina.' (cafe)",
            options_json=json.dumps(["bar", "binario", "banco", "bagno"]),
            correct_answer="bar",
            explanation="In Italy, a 'bar' is where locals drink morning espresso and eat cornetti."
        ),
        Exercise(
            lesson_id=lesson4.id,
            exercise_type="matching",
            prompt="Match the beverage & dining vocabulary:",
            options_json=json.dumps({
                "bere": "to drink",
                "bicchiere": "glass",
                "birra": "beer",
                "bello": "beautiful"
            }),
            correct_answer="matched",
            explanation="Bere = to drink, Bicchiere = glass, Birra = beer, Bello = beautiful."
        ),
        Exercise(
            lesson_id=lesson4.id,
            exercise_type="odd_one_out",
            prompt="Which of these words is NOT a color or physical attribute?",
            options_json=json.dumps(["binario", "bianco", "biondo", "basso"]),
            correct_answer="binario",
            explanation="'Binario' is a train track/platform. 'Bianco' (white), 'biondo' (blonde), and 'basso' (short) are adjectives."
        )
    ]
    db.add_all(ex_l4)

    db.commit()
    print("Seeding complete! Stages, units, 15-word lessons, grammar tips, and exercises created.")
    db.close()

    # Seed expanded grammar, reading, and writing modules
    from backend.scripts.seed_expanded_content import seed_expanded_content
    seed_expanded_content()

if __name__ == "__main__":
    seed_database()
