import json
from backend.app.database import engine, Base, SessionLocal
from backend.app.models.curriculum import GrammarLesson, ReadingPassage, WritingPrompt

def seed_expanded_content():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing if re-seeding expanded tables
    db.query(GrammarLesson).delete()
    db.query(ReadingPassage).delete()
    db.query(WritingPrompt).delete()
    db.commit()

    print("Seeding Grammar Lessons...")
    grammar_lessons = [
        GrammarLesson(
            id=1,
            title="Gli Articoli Determinativi e Indeterminativi",
            level="A1",
            category="Articoli & Nomi",
            summary="Definite and indefinite articles in Italian: rules by gender, number, and starting consonant/vowel.",
            rules_markdown="""### Gli Articoli in Italiano

In Italian, nouns have a grammatical gender (**maschile** or **femminile**) and number (**singolare** or **plurale**). The article must agree with the noun in both gender and number.

#### 1. Articoli Determinativi (The)
- **Maschile Singolare:**
  - **il**: before most consonants (*il libro*, *il ragazzo*, *il treno*)
  - **lo**: before *s + consonant*, *z*, *ps*, *gn*, *x*, *y* (*lo studente*, *lo zaino*, *lo psicologo*)
  - **l'**: before vowels (*l'amico*, *l'albero*)
- **Maschile Plurale:**
  - **i**: plural of *il* (*i libri*, *i ragazzi*)
  - **gli**: plural of *lo* and *l'* (*gli studenti*, *gli zaini*, *gli amici*)
- **Femminile Singolare:**
  - **la**: before consonants (*la casa*, *la pizza*, *la strada*)
  - **l'**: before vowels (*l'amica*, *l'isola*)
- **Femminile Plurale:**
  - **le**: plural of *la* and *l'* (*le case*, *le amiche*)

#### 2. Articoli Indeterminativi (A / An)
- **Maschile:** **un** (before vowels and most consonants: *un amico*, *un libro*), **uno** (before *s+cons*, *z*: *uno studente*, *uno zaino*).
- **Femminile:** **una** (before consonants: *una pizza*), **un'** (with apostrophe before vowels: *un'amica*).

> **Attenzione!** Never put an apostrophe on masculine *un*: write *un amico* (not un'amico), but write *un'amica* for feminine!
""",
            tables_json=json.dumps([
                {
                    "title": "Articoli Determinativi",
                    "headers": ["Genere", "Singolare", "Plurale", "Esempio"],
                    "rows": [
                        ["Maschile (Consonante)", "il", "i", "il caffè → i caffè"],
                        ["Maschile (s+cons, z, gn)", "lo", "gli", "lo zaino → gli zaini"],
                        ["Maschile (Vocale)", "l'", "gli", "l'albergo → gli alberghi"],
                        ["Femminile (Consonante)", "la", "le", "la pizza → le pizze"],
                        ["Femminile (Vocale)", "l'", "le", "l'ora → le ore"]
                    ]
                },
                {
                    "title": "Articoli Indeterminativi",
                    "headers": ["Genere", "Articolo", "Uso", "Esempio"],
                    "rows": [
                        ["Maschile", "un", "Davanti a consonanti e vocali", "un libro, un amico"],
                        ["Maschile", "uno", "Davanti a s+cons, z, ps, gn", "uno studente, uno zio"],
                        ["Femminile", "una", "Davanti a consonanti", "una ragazza, una penna"],
                        ["Femminile", "un'", "Davanti a vocali (con apostrofo)", "un'ora, un'idea"]
                    ]
                }
            ]),
            examples_json=json.dumps([
                {"it": "Il caffè espresso è pronto.", "en": "The espresso coffee is ready."},
                {"it": "Lo studente legge un libro interessante.", "en": "The student reads an interesting book."},
                {"it": "Prendo un'aranciata e una focaccia.", "en": "I'll take an orange soda and a focaccia."},
                {"it": "Gli amici arrivano stasera.", "en": "The friends are arriving tonight."}
            ]),
            order_index=1
        ),
        GrammarLesson(
            id=2,
            title="Il Presente Indicativo: Essere e Avere",
            level="A1",
            category="Verbi Ausiliari",
            summary="Master the two most essential irregular auxiliary verbs in Italian and their idiomatic uses.",
            rules_markdown="""### Essere e Avere

*Essere* (to be) and *avere* (to have) are the fundamental building blocks of Italian grammar. They function both as main verbs and as auxiliary verbs to form compound tenses like the *Passato Prossimo*.

#### Usi Speciali di Essere
- Identità e professione: *Io sono Marco, lui è medico.*
- Provenienza: *Siamo di Firenze.*
- Descrizione fisica e carattere: *La città è bellissima.*

#### Usi Speciali di Avere (Espressioni Idiomatiche)
In English you say "I am hungry" or "I am 25 years old", but in Italian you use **avere**:
- **avere fame** = to be hungry (*Ho fame!*)
- **avere sete** = to be thirsty (*Hai sete?*)
- **avere sonno** = to be sleepy (*Hanno sonno.*)
- **avere fretta** = to be in a hurry (*Abbiamo fretta.*)
- **avere ragione / torto** = to be right / wrong (*Ha ragione.*)
- **avere ... anni** = to be ... years old (*Ho trent'anni.*)
""",
            tables_json=json.dumps([
                {
                    "title": "Coniugazione al Presente",
                    "headers": ["Pronome", "Essere (to be)", "Avere (to have)"],
                    "rows": [
                        ["io", "sono", "ho"],
                        ["tu", "sei", "hai"],
                        ["lui / lei", "è", "ha"],
                        ["noi", "siamo", "abbiamo"],
                        ["voi", "siete", "avete"],
                        ["loro", "sono", "hanno"]
                    ]
                }
            ]),
            examples_json=json.dumps([
                {"it": "Io sono italiano e ho venticinque anni.", "en": "I am Italian and I am 25 years old."},
                {"it": "Oggi abbiamo molta fretta perché il treno parte presto.", "en": "Today we are in a big hurry because the train leaves early."},
                {"it": "Se hai fame, andiamo a mangiare qualcosa.", "en": "If you are hungry, let's go eat something."},
                {"it": "Chiara è molto gentile con tutti.", "en": "Chiara is very kind to everyone."}
            ]),
            order_index=2
        ),
        GrammarLesson(
            id=3,
            title="I Verbi Regolari al Presente: -ARE, -ERE, -IRE",
            level="A1",
            category="Verbi Regolari",
            summary="Conjugation patterns for the three regular Italian verb conjugations.",
            rules_markdown="""### Le Tre Coniugazioni Regolari

Italian verbs fall into three groups based on their infinitive ending:
1. **1ª Coniugazione:** **-are** (e.g., *parlare*, *abitare*, *lavorare*)
2. **2ª Coniugazione:** **-ere** (e.g., *prendere*, *scrivere*, *leggere*)
3. **3ª Coniugazione:** **-ire** (e.g., *dormire*, *partire*, *aprire*)

#### Il Gruppo Speciale con -ISC-
Many common *-ire* verbs insert **-isc-** between the stem and the ending for *io, tu, lui/lei, loro*:
- *capire* (to understand): *capisco, capisci, capisce, capiamo, capite, capiscono*
- *preferire* (to prefer): *preferisco, preferisci, preferisce, preferiamo, preferite, preferiscono*
- *pulire* (to clean): *pulisco, pulisci, pulisce, puliamo, pulite, puliscono*
""",
            tables_json=json.dumps([
                {
                    "title": "Desinenze del Presente Indicativo",
                    "headers": ["Pronome", "-ARE (Parlare)", "-ERE (Prendere)", "-IRE (Dormire)", "-IRE con -ISC- (Capire)"],
                    "rows": [
                        ["io", "parl-o", "prend-o", "dorm-o", "cap-isc-o"],
                        ["tu", "parl-i", "prend-i", "dorm-i", "cap-isc-i"],
                        ["lui / lei", "parl-a", "prend-e", "dorm-e", "cap-isc-e"],
                        ["noi", "parl-iamo", "prend-iamo", "dorm-iamo", "cap-iamo"],
                        ["voi", "parl-ate", "prend-ete", "dorm-ite", "cap-ite"],
                        ["loro", "parl-ano", "prend-ono", "dorm-ono", "cap-isc-ono"]
                    ]
                }
            ]),
            examples_json=json.dumps([
                {"it": "Noi parliamo italiano ogni giorno con gli insegnanti.", "en": "We speak Italian every day with the teachers."},
                {"it": "Cosa prendi da bere al bar?", "en": "What are you having to drink at the bar?"},
                {"it": "Capisco perfettamente quello che dici.", "en": "I understand perfectly what you are saying."},
                {"it": "Il treno per Venezia parte dal binario 4.", "en": "The train for Venice departs from platform 4."}
            ]),
            order_index=3
        ),
        GrammarLesson(
            id=4,
            title="I Verbi Riflessivi e la Routine Quotidiana",
            level="A2",
            category="Verbi Riflessivi",
            summary="Express actions that the subject performs on oneself using reflexive pronouns.",
            rules_markdown="""### I Verbi Riflessivi

A verb is reflexive when the subject and direct object are the same person. In Italian, reflexives are very common for daily routines and feelings:
- *alzarsi* (to get up)
- *svegliarsi* (to wake up)
- *lavarsi* (to wash oneself)
- *vestirsi* (to get dressed)
- *chiamarsi* (to be named)
- *riposarsi* (to rest)

#### I Pronomi Riflessivi
The reflexive pronouns precede the conjugated verb:
- io **mi**
- tu **ti**
- lui/lei **si**
- noi **ci**
- voi **vi**
- loro **si**

> **Passato Prossimo Alert:** ALL reflexive verbs always use **essere** as auxiliary in compound tenses! The past participle agrees in gender and number: *Mi sono svegliato/a*, *Ci siamo alzati/e*.
""",
            tables_json=json.dumps([
                {
                    "title": "Coniugazione di Alzarsi",
                    "headers": ["Pronome", "Pronome Riflessivo", "Verbo", "Traduzione"],
                    "rows": [
                        ["io", "mi", "alzo", "I get up"],
                        ["tu", "ti", "alzi", "you get up"],
                        ["lui / lei", "si", "alza", "he / she gets up"],
                        ["noi", "ci", "alziamo", "we get up"],
                        ["voi", "vi", "alzate", "you all get up"],
                        ["loro", "si", "alzano", "they get up"]
                    ]
                }
            ]),
            examples_json=json.dumps([
                {"it": "La mattina mi sveglio alle sette e mi alzo subito.", "en": "In the morning I wake up at seven and get up right away."},
                {"it": "Come ti chiami? Mi chiamo Luca.", "en": "What is your name? My name is Luca."},
                {"it": "Ci prepariamo per uscire con gli amici.", "en": "We get ready to go out with friends."},
                {"it": "Ieri sera si sono riposati a casa.", "en": "Yesterday evening they rested at home."}
            ]),
            order_index=4
        ),
        GrammarLesson(
            id=5,
            title="Il Passato Prossimo: Scelta dell'Ausiliare Essere o Avere",
            level="A2",
            category="Tempi Passati",
            summary="How to construct past actions, select between auxiliary Essere and Avere, and apply participle agreement.",
            rules_markdown="""### Il Passato Prossimo

The *Passato Prossimo* expresses completed past actions. It consists of two parts:
$$\\text{Ausiliare (Presente di Avere o Essere)} + \\text{Participio Passato}$$

#### Participio Passato Regolare:
- **-are** → **-ato** (*parlare → parlato*)
- **-ere** → **-uto** (*credere → creduto*)
- **-ire** → **-ito** (*dormire → dormito*)

#### Quando si usa AVERE?
Used with all **transitive verbs** (verbs that take a direct object: *mangiare una mela*, *leggere un libro*):
- *Ho mangiato una pizza.*
- *Abbiamo ascoltato la musica.*
*(Notice: the participle ends in -o and does NOT change!)*

#### Quando si usa ESSERE?
Used with:
1. **Verbi di movimento** (*andare, venire, partire, arrivare, uscire, entrare*)
2. **Verbi di stato / cambio di stato** (*essere, stare, rimanere, nascere, morire*)
3. **Tutti i verbi riflessivi** (*svegliarsi, vestirsi*)

> **Important Rule of Agreement with ESSERE:**
> When using *essere*, the past participle **must agree in gender and number** with the subject:
> - Marco è andat**o** a Roma.
> - Giulia è andat**a** a Roma.
> - Marco e Luca sono andat**i** a Roma.
> - Giulia e Chiara sono andat**e** a Roma.
""",
            tables_json=json.dumps([
                {
                    "title": "Confronto Ausiliari",
                    "headers": ["Caratteristica", "Con AVERE", "Con ESSERE"],
                    "rows": [
                        ["Tipo di verbi", "Transitivi (con oggetto diretto)", "Movimento, stato, riflessivi"],
                        ["Accordo del participio", "Invariabile (termina in -o)", "Accorda in genere e numero (-o, -a, -i, -e)"],
                        ["Esempio Maschile", "Marco ha mangiato.", "Marco è arrivato."],
                        ["Esempio Femminile", "Chiara ha mangiato.", "Chiara è arrivata."],
                        ["Esempio Plurale M.", "I ragazzi hanno mangiato.", "I ragazzi sono arrivati."],
                        ["Esempio Plurale F.", "Le ragazze hanno mangiato.", "Le ragazze sono arrivate."]
                    ]
                }
            ]),
            examples_json=json.dumps([
                {"it": "Ieri ho comprato un bel libro in libreria.", "en": "Yesterday I bought a nice book in the bookstore."},
                {"it": "Siamo partiti per Napoli alle otto di mattina.", "en": "We left for Naples at eight in the morning."},
                {"it": "Francesca è tornata tardi dall'università.", "en": "Francesca returned late from university."},
                {"it": "Avete visto il nuovo film italiano?", "en": "Did you all see the new Italian film?"}
            ]),
            order_index=5
        ),
        GrammarLesson(
            id=6,
            title="Le Preposizioni Articolate",
            level="A2",
            category="Preposizioni",
            summary="Combining the simple Italian prepositions di, a, da, in, su with definite articles.",
            rules_markdown="""### Le Preposizioni Articolate

When simple prepositions (**di**, **a**, **da**, **in**, **su**) are followed by a definite article, they merge into a single compound word called a *preposizione articolata*.

#### Usi Principali:
- **di** (of, from): specifica o possesso (*Il libro del professore*).
- **a** (to, at): direzione o luogo con città (*Vado al bar*, *allo stadio*).
- **da** (from, by, at someone's place): provenienza o persone (*Vado dal medico*, *dal panettiere*).
- **in** (in, into): dentro a luoghi chiusi, regioni o stati (*Nel cassetto*, *nella piazza*).
- **su** (on, on top of): sopra a una superficie (*Sul tavolo*, *sulla sedia*).
""",
            tables_json=json.dumps([
                {
                    "title": "Tabella delle Preposizioni Articolate",
                    "headers": ["Prep.", "+ il", "+ lo", "+ l'", "+ la", "+ i", "+ gli", "+ le"],
                    "rows": [
                        ["di", "del", "dello", "dell'", "della", "dei", "degli", "delle"],
                        ["a", "al", "allo", "all'", "alla", "ai", "agli", "alle"],
                        ["da", "dal", "dallo", "dall'", "dalla", "dai", "dagli", "dalle"],
                        ["in", "nel", "nello", "nell'", "nella", "nei", "negli", "nelle"],
                        ["su", "sul", "sullo", "sull'", "sulla", "sui", "sugli", "sulle"]
                    ]
                }
            ]),
            examples_json=json.dumps([
                {"it": "Il caffè è sul tavolo della cucina.", "en": "The coffee is on the kitchen table."},
                {"it": "Oggi pomeriggio andiamo dal medico.", "en": "This afternoon we are going to the doctor."},
                {"it": "Ci vediamo alle otto davanti al cinema.", "en": "See you at eight in front of the cinema."},
                {"it": "I documenti sono nella cartella del direttore.", "en": "The documents are in the director's folder."}
            ]),
            order_index=6
        ),
        GrammarLesson(
            id=7,
            title="L'Imperfetto vs Passato Prossimo",
            level="B1",
            category="Tempi Passati",
            summary="Understand how to narrate past stories by balancing background descriptions and completed actions.",
            rules_markdown="""### Imperfetto vs Passato Prossimo

Narrating in Italian requires choosing between two past tenses:

#### 1. L'Imperfetto (The Past Continuative & Descriptive)
Used for:
- Continuous, habitual, or repeated actions in the past ("used to" or "was doing"):
  *Da bambino giocavo sempre a calcio.* (As a child I always played soccer.)
- Descriptions of weather, physical appearance, feelings, and age:
  *Era una bella giornata di sole.* (It was a beautiful sunny day.)
  *Avevo vent'anni ed ero felice.* (I was twenty and happy.)
- Two simultaneous ongoing actions connected by **mentre**:
  *Mentre io cucinavo, lui leggeva.* (While I was cooking, he was reading.)

#### 2. Il Passato Prossimo (The Punctual & Completed Event)
Used for:
- Single, completed events with a clear beginning or end:
  *Ieri ho visto un amico.* (Yesterday I saw a friend.)
  *All'improvviso è suonato il telefono.* (Suddenly the phone rang.)
- An action that interrupts an ongoing action:
  *Mentre dormivo, il telefono ha suonato.* (While I was sleeping, the phone rang.)
""",
            tables_json=json.dumps([
                {
                    "title": "Coniugazione dell'Imperfetto",
                    "headers": ["Pronome", "Parlare (-ARE)", "Prendere (-ERE)", "Dormire (-IRE)", "Essere (Irregolare)"],
                    "rows": [
                        ["io", "parlavo", "prendevo", "dormivo", "ero"],
                        ["tu", "parlavi", "prendevi", "dormivi", "eri"],
                        ["lui / lei", "parlava", "prendeva", "dormiva", "era"],
                        ["noi", "parlavamo", "prendevamo", "dormivamo", "eravamo"],
                        ["voi", "parlavate", "prendevate", "dormivate", "eravate"],
                        ["loro", "parlavano", "prendevano", "dormivano", "erano"]
                    ]
                }
            ]),
            examples_json=json.dumps([
                {"it": "Mentre studiavo per l'esame, è arrivata una notizia inattesa.", "en": "While I was studying for the exam, an unexpected news arrived."},
                {"it": "Da piccolo andavo al mare ogni estate con i miei nonni.", "en": "As a kid I used to go to the sea every summer with my grandparents."},
                {"it": "Faceva molto freddo quando siamo usciti di casa.", "en": "It was very cold when we left the house."}
            ]),
            order_index=7
        ),
        GrammarLesson(
            id=8,
            title="I Pronomi Diretti e Indiretti",
            level="B1",
            category="Pronomi",
            summary="Replace nouns to speak fluidly and avoid repetitions using direct and indirect object pronouns.",
            rules_markdown="""### Pronomi Diretti e Indiretti

#### 1. Pronomi Diretti (Answer: Chi? Che cosa?)
Replace the direct object without a preposition:
- mi (me), ti (you), **lo** (him / it masc.), **la** (her / it fem.)
- ci (us), vi (you all), **li** (them masc.), **le** (them fem.)
*Esempio:* Conosci Marco? Sì, **lo** conosco. Mangi la pasta? Sì, **la** mangio.

#### 2. Pronomi Indiretti (Answer: A chi?)
Replace nouns introduced by preposition **a** (to someone):
- mi (to me), ti (to you), **gli** (to him), **le** (to her)
- ci (to us), vi (to you all), **gli / loro** (to them)
*Esempio:* Telefoni a Chiara? Sì, **le** telefono. Ho parlato a Luca e **gli** ho spiegato tutto.
""",
            tables_json=json.dumps([
                {
                    "title": "Confronto Pronomi Diretti e Indiretti",
                    "headers": ["Persona", "Pronome Diretto (Chi / Cosa)", "Pronome Indiretto (A chi)"],
                    "rows": [
                        ["io", "mi", "mi (a me)"],
                        ["tu", "ti", "ti (a te)"],
                        ["lui", "lo", "gli (a lui)"],
                        ["lei", "la", "le (a lei)"],
                        ["noi", "ci", "ci (a noi)"],
                        ["voi", "vi", "vi (a voi)"],
                        ["loro (m)", "li", "gli / loro (a loro)"],
                        ["loro (f)", "le", "gli / loro (a loro)"]
                    ]
                }
            ]),
            examples_json=json.dumps([
                {"it": "Hai comprato il giornale? Sì, l'ho comprato stamattina.", "en": "Did you buy the newspaper? Yes, I bought it this morning."},
                {"it": "Cosa regali a Maria per il compleanno? Le regalo un libro.", "en": "What are you giving Maria for her birthday? I'm giving her a book."},
                {"it": "Se hai bisogno di aiuto, chiamami e ti aiuto subito.", "en": "If you need help, call me and I'll help you right away."}
            ]),
            order_index=8
        )
    ]
    db.add_all(grammar_lessons)

    print("Seeding Reading Passages & Comprehension...")
    reading_passages = [
        ReadingPassage(
            id=1,
            title="Un Caffè al Bar di Trastevere",
            level="A1",
            category="Vita Quotidiana",
            content_it="""Ogni mattina a Roma inizia con un rito speciale: la colazione al bar. 

Marco entra nel suo bar preferito a Trastevere. Il barista, Roberto, saluta tutti con un sorriso solare: «Buongiorno Marco! Il solito?». 

«Buongiorno Roberto! Sì, grazie: un espresso doppio al banco e un cornetto caldo al pistacchio». 

A Roma, la maggior parte delle persone beve il caffè velocemente in piedi al bancone. Prima di ordinare, Marco passa dalla cassa per fare lo scontrino. Roberto prepara l'espresso con la macchina a vapore: l'aroma del caffè tostato riempie tutto il locale. 

Marco beve il suo espresso in due sorsi, sfoglia il giornale sportivo e chiacchiera con i vicini del quartiere. Dopo dieci minuti saluta con entusiasmo: «Buona giornata Roberto, a domani!». Questo piccolo momento di serenità è il modo migliore per cominciare una giornata dinamica nella Città Eterna.""",
            content_en="""Every morning in Rome begins with a special ritual: breakfast at the bar.

Marco walks into his favorite bar in Trastevere. The barista, Roberto, greets everyone with a bright smile: "Good morning Marco! The usual?"

"Good morning Roberto! Yes, thank you: a double espresso at the counter and a warm pistachio croissant."

In Rome, most people drink coffee quickly standing at the counter. Before ordering, Marco stops by the register to get the receipt. Roberto prepares the espresso with the steam machine: the aroma of roasted coffee fills the entire room.

Marco drinks his espresso in two sips, glances at the sports newspaper, and chats with neighborhood locals. After ten minutes he says goodbye enthusiastically: "Have a great day Roberto, see you tomorrow!". This small moment of serenity is the best way to start a dynamic day in the Eternal City.""",
            vocabulary_hints_json=json.dumps([
                {"term": "il rito", "en": "the ritual"},
                {"term": "al banco / al bancone", "en": "at the bar counter"},
                {"term": "il cornetto", "en": "croissant / Italian pastry"},
                {"term": "la cassa", "en": "the cash register / checkout"},
                {"term": "lo scontrino", "en": "the paper receipt (mandatory first step in Italian bars)"},
                {"term": "in due sorsi", "en": "in two sips / quickly"}
            ]),
            questions_json=json.dumps([
                {
                    "question": "Dove si trova il bar preferito di Marco?",
                    "options": ["A Trastevere, a Roma", "Vicino al Colosseo", "A Firenze", "A Milano"],
                    "correct_answer": "A Trastevere, a Roma",
                    "explanation": "Il testo dice esplicitamente: 'Marco entra nel suo bar preferito a Trastevere' a Roma."
                },
                {
                    "question": "Cosa fa Marco prima di ordinare il caffè?",
                    "options": [
                        "Passa dalla cassa per fare lo scontrino",
                        "Si siede immediatamente al tavolo",
                        "Telefona al suo amico",
                        "Legge tutto il giornale"
                    ],
                    "correct_answer": "Passa dalla cassa per fare lo scontrino",
                    "explanation": "In molti bar italiani tradizionali si paga prima alla cassa e si presenta lo scontrino al barista."
                },
                {
                    "question": "Come beve il caffè la maggior parte delle persone secondo il testo?",
                    "options": [
                        "In piedi al bancone",
                        "Seduti per un'ora",
                        "Da asporto in macchina",
                        "Sempre con il latte"
                    ],
                    "correct_answer": "In piedi al bancone",
                    "explanation": "Il testo precisa: 'la maggior parte delle persone beve il caffè velocemente in piedi al bancone'."
                }
            ]),
            order_index=1
        ),
        ReadingPassage(
            id=2,
            title="Passeggiata a Firenze: Tra Arte e Sapori",
            level="A2",
            category="Cultura & Viaggi",
            content_it="""Firenze è una delle città più affascinanti del mondo, dove ogni vicolo custodisce secoli di arte e tradizione. 

È sabato mattina e Chiara ha deciso di fare una passeggiata nel centro storico. Partendo da Piazza del Duomo, ammira la maestosa Cupola del Brunelleschi, che domina il cielo toscano con le sue tegole rosse di terracotta. 

Camminando lungo Via dei Calzaiuoli, raggiunge Piazza della Signoria con le sue splendide sculture rinascimentali. Poi attraversa il celebre Ponte Vecchio, famoso in tutto il mondo per le antiche botteghe orafe che si affacciano sulle acque placide del fiume Arno.

All'ora di pranzo, Chiara visita il Mercato Centrale di San Lorenzo. L'atmosfera è vibrante e piena di profumi: formaggi toscani, salumi tipici, pane appena sfornato e verdure di stagione. Chiara ordina un piatto tipico toscano con ribollita e cantucci alle mandorle, accompagnati da un bicchiere di Chianti classico. «Vivere a Firenze», pensa Chiara sorridendo, «significa respirare bellezza ogni singolo giorno».""",
            content_en="""Florence is one of the most fascinating cities in the world, where every alley preserves centuries of art and tradition.

It's Saturday morning and Chiara decided to take a stroll in the historic center. Starting from Piazza del Duomo, she admires the majestic Brunelleschi's Dome, which dominates the Tuscan sky with its red terracotta tiles.

Walking along Via dei Calzaiuoli, she reaches Piazza della Signoria with its splendid Renaissance sculptures. Then she crosses the famous Ponte Vecchio, known worldwide for ancient goldsmith workshops overlooking the calm waters of the Arno river.

At lunchtime, Chiara visits the Central Market of San Lorenzo. The atmosphere is vibrant and full of aromas: Tuscan cheeses, cured meats, freshly baked bread, and seasonal vegetables. Chiara orders a typical Tuscan dish with ribollita and almond cantucci, accompanied by a glass of classic Chianti. "Living in Florence," Chiara thinks with a smile, "means breathing beauty every single day.\"""",
            vocabulary_hints_json=json.dumps([
                {"term": "il vicolo", "en": "narrow alley / lane"},
                {"term": "la terracotta", "en": "baked clay / terracotta"},
                {"term": "le botteghe orafe", "en": "goldsmith / jewelry artisan shops"},
                {"term": "la ribollita", "en": "famous Tuscan hearty bread and vegetable soup"},
                {"term": "i cantucci", "en": "crisp Tuscan almond biscotti"},
                {"term": "respirare bellezza", "en": "to breathe in beauty"}
            ]),
            questions_json=json.dumps([
                {
                    "question": "Quale monumento ammira Chiara all'inizio della sua passeggiata?",
                    "options": [
                        "La Cupola del Brunelleschi",
                        "La Torre di Pisa",
                        "Il Colosseo",
                        "Il Duomo di Milano"
                    ],
                    "correct_answer": "La Cupola del Brunelleschi",
                    "explanation": "Il testo racconta che partendo da Piazza del Duomo ammira la maestosa Cupola del Brunelleschi."
                },
                {
                    "question": "Per cosa è celebre il Ponte Vecchio secondo il brano?",
                    "options": [
                        "Per le antiche botteghe orafe",
                        "Per i musei di arte moderna",
                        "Per le automobili d'epoca",
                        "Per le gare di barche"
                    ],
                    "correct_answer": "Per le antiche botteghe orafe",
                    "explanation": "Ponte Vecchio è famoso per le sue storiche botteghe di orafi e gioiellieri sopra il fiume Arno."
                },
                {
                    "question": "Cosa ordina Chiara per pranzo al Mercato Centrale?",
                    "options": [
                        "Ribollita toscana e cantucci alle mandorle",
                        "Pizza napoletana e tiramisù",
                        "Spaghetti alla carbonara",
                        "Risotto ai funghi porcini"
                    ],
                    "correct_answer": "Ribollita toscana e cantucci alle mandorle",
                    "explanation": "Chiara ordina un piatto tipico toscano con ribollita e cantucci alle mandorle."
                }
            ]),
            order_index=2
        ),
        ReadingPassage(
            id=3,
            title="La Tradizione della Dieta Mediterranea e i Mercati Rionali",
            level="B1",
            category="Cultura & Gastronomia",
            content_it="""In Italia il cibo non è semplicemente nutrimento; è cultura, identità regionale e condivisione sociale. La Dieta Mediterranea, riconosciuta dall'UNESCO come patrimonio immateriale dell'umanità, si fonda su ingredienti freschi, stagionalità e rispetto del territorio.

Il cuore pulsante di questa filosofia gastronomica sono i mercati rionali. Ogni quartiere, dal nord al sud della penisola, possiede la propria piazza del mercato. Qui i residenti incontrano direttamente i produttori locali: contadini che vendono pomodori maturati al sole, pescatori con il pescato del giorno e fornai con pagnotte cotte a legna.

A differenza dei grandi supermercati moderni, al mercato si instaura un dialogo autentico. Si chiedono consigli sulle ricette tradizionali, si impara a riconoscere il momento giusto per cogliere un frutto e si scambiano due chiacchiere amichevoli. La cucina italiana celebra la semplicità: con pochi ingredienti di altissima qualità come olio extravergine d'oliva, basilico fresco, aglio e pasta di grano duro, nasce un capolavoro culinario invidiato in tutto il mondo.""",
            content_en="""In Italy food is not merely nourishment; it is culture, regional identity, and social togetherness. The Mediterranean Diet, recognized by UNESCO as intangible cultural heritage of humanity, is based on fresh ingredients, seasonality, and respect for the territory.

The beating heart of this culinary philosophy is the local open-air markets. Every neighborhood, from north to south of the peninsula, possesses its own market square. Here residents directly meet local producers: farmers selling sun-ripened tomatoes, fishermen with the daily catch, and bakers with wood-fired bread.

Unlike large modern supermarkets, an authentic dialogue forms at the market. People ask for tips on traditional recipes, learn to recognize the perfect ripeness of fruit, and exchange friendly chats. Italian cuisine celebrates simplicity: with just a few top-quality ingredients such as extra-virgin olive oil, fresh basil, garlic, and durum wheat pasta, a culinary masterpiece envied worldwide is born.""",
            vocabulary_hints_json=json.dumps([
                {"term": "patrimonio immateriale", "en": "intangible cultural heritage"},
                {"term": "la stagionalità", "en": "seasonality of produce"},
                {"term": "il mercato rionale", "en": "neighborhood open-air market"},
                {"term": "il pescato del giorno", "en": "the catch of the day"},
                {"term": "grano duro", "en": "durum wheat (used for authentic pasta)"}
            ]),
            questions_json=json.dumps([
                {
                    "question": "Quale importante riconoscimento ha ricevuto la Dieta Mediterranea?",
                    "options": [
                        "Patrimonio immateriale dell'umanità dall'UNESCO",
                        "Premio Nobel per la medicina",
                        "Marchio commerciale europeo",
                        "Nessun riconoscimento ufficiale"
                    ],
                    "correct_answer": "Patrimonio immateriale dell'umanità dall'UNESCO",
                    "explanation": "La Dieta Mediterranea è ufficialmente inserita dall'UNESCO tra i patrimoni culturali immateriali."
                },
                {
                    "question": "Cosa caratterizza i mercati rionali rispetto ai supermercati moderni?",
                    "options": [
                        "Il dialogo diretto tra produttori locali e residenti",
                        "I prezzi sempre più alti dei supermercati",
                        "La vendita esclusiva di cibi surgelati",
                        "L'assenza totale di frutta e verdura"
                    ],
                    "correct_answer": "Il dialogo diretto tra produttori locali e residenti",
                    "explanation": "Al mercato rionale si instaura un rapporto diretto e umano con i contadini e artigiani locali."
                }
            ]),
            order_index=3
        )
    ]
    db.add_all(reading_passages)

    print("Seeding Writing & Sentence Building Prompts...")
    writing_prompts = [
        WritingPrompt(
            id=1,
            title="Presentati a un amico italiano",
            level="A1",
            category="Presentazioni & Dialogo",
            task_prompt="Componi una breve presentazione personale in italiano indicando il tuo nome, la tua provenienza e una cosa che ti piace fare nel tempo libero.",
            starter_words_json=json.dumps(["Mi chiamo", "Sono di", "Parlo inglese e", "Nel tempo libero", "Mi piace molto", "Studiare l'italiano"]),
            sample_solution="Ciao! Mi chiamo Marco, sono di Roma e nel tempo libero mi piace molto studiare l'italiano e viaggiare.",
            order_index=1
        ),
        WritingPrompt(
            id=2,
            title="Ordinare la colazione al bar",
            level="A1",
            category="Ordinazioni & Vita Pratica",
            task_prompt="Scrivi una frase educata per ordinare al barista un caffè macchiato e un cornetto, chiedendo infine cortesemente quanto costa.",
            starter_words_json=json.dumps(["Buongiorno", "Vorrei", "Un caffè macchiato", "Un cornetto", "Per favore", "Quanto costa", "Grazie"]),
            sample_solution="Buongiorno, vorrei un caffè macchiato e un cornetto alla crema, per favore. Quanto costa in tutto?",
            order_index=2
        ),
        WritingPrompt(
            id=3,
            title="La mia routine quotidiana",
            level="A2",
            category="Verbi Riflessivi & Routine",
            task_prompt="Descrivi la tua routine mattutina usando almeno due verbi riflessivi (es. svegliarsi, alzarsi, lavarsi, vestirsi).",
            starter_words_json=json.dumps(["La mattina", "Mi sveglio alle", "Mi alzo", "Faccio una doccia", "Mi vesto", "Poi faccio colazione"]),
            sample_solution="Ogni mattina mi sveglio alle sette, mi alzo e mi preparo velocemente prima di uscire per andare al lavoro.",
            order_index=3
        ),
        WritingPrompt(
            id=4,
            title="Il mio ultimo fine settimana",
            level="A2",
            category="Narrazione al Passato Prossimo",
            task_prompt="Scrivi una breve frase al passato prossimo su cosa hai fatto lo scorso sabato, usando verbi con ausiliare essere o avere.",
            starter_words_json=json.dumps(["Sabato scorso", "Sono andato", "Ho incontrato", "Abbiamo mangiato", "È stata una bella giornata"]),
            sample_solution="Sabato scorso sono andato in centro con i miei amici, abbiamo mangiato una pizza e siamo tornati a casa tardi.",
            order_index=4
        ),
        WritingPrompt(
            id=5,
            title="Un consiglio di viaggio in Italia",
            level="B1",
            category="Opinioni & Raccomandazioni",
            task_prompt="Consiglia a un amico una città o regione italiana da visitare, spiegando il motivo principale con parole tue.",
            starter_words_json=json.dumps(["Ti consiglio di visitare", "Secondo me", "Perché", "È una città magnifica", "Non puoi perdere"]),
            sample_solution="Ti consiglio di visitare Firenze perché è una città ricca di arte e storia. Secondo me non puoi perdere la Cupola del Brunelleschi.",
            order_index=5
        )
    ]
    db.add_all(writing_prompts)

    db.commit()
    print("Expanded content successfully seeded!")
    print(f"- {len(grammar_lessons)} Grammar lessons seeded")
    print(f"- {len(reading_passages)} Reading passages seeded")
    print(f"- {len(writing_prompts)} Writing prompts seeded")
    db.close()

if __name__ == "__main__":
    seed_expanded_content()
