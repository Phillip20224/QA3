import sqlite3

class Question:
    def __init__(self, course, question_text, choices, correct_index):
        if len(choices) != 4:
            raise ValueError("Exactly 4 choices are required.")
        if not 0 <= correct_index < 4:
            raise ValueError("Correct index must be between 0 and 3.")
        self.course = course
        self.question_text = question_text
        self.choices = choices
        self.correct_index = correct_index

    def to_tuple(self):
        return (
            self.question_text,
            self.choices[0],
            self.choices[1],
            self.choices[2],
            self.choices[3],
            self.correct_index
        )


    @staticmethod
    def get_all_questions_for_course(course):
        conn = sqlite3.connect("questionsdb.db")
        cursor = conn.cursor()
        questions = []
        try:
            cursor.execute(f"SELECT * FROM {course}")
            rows = cursor.fetchall()
            for row in rows:
                question_text = row[1]  # matches your __init__
                choices = list(row[2:6])
                correct_index = row[6]
                questions.append(Question(course, question_text, choices, correct_index))
        except Exception as e:
            print(f"Error fetching questions for course {course}: {e}")
        finally:
            conn.close()
        return questions


def save_many_questions(questions, db_file="questionsdb.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    for question in questions:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {question.course} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                choice_a TEXT,
                choice_b TEXT,
                choice_c TEXT,
                choice_d TEXT,
                correct_index INTEGER
            )
        """)
        cursor.execute(f"""
            INSERT INTO {question.course} (
                question, choice_a, choice_b, choice_c, choice_d, correct_index
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, question.to_tuple())

    conn.commit()
    conn.close()


questions = [
    Question("DS3850", "What is str", ["integer", "key", "string", "boolean"], 2),
    Question("DS3850", "What is used for a dictionary?", ["()", "[]", "{}", "0"], 2),
    Question("DS3850", "What do loops do?", ["combine data types", "repeat an action", "error", "make the text spin"], 1),
    Question("DS3850", "What does == mean?", ["is equal to", "takes the value", "does not mean", "error"], 0),
    Question("DS3850", "What is one way to get stuck in a loop?", ["while test with nothing further to test", "allowing user to input new values", "just avoid loops", "error"], 0),
    Question("DS3850", "What does blank space in lines of code do?", ["nothing will show up", "a whole bunch of space will appear in the terminal", "error", "it won't affect the output; vs code reads to the next line of code"], 3),
    Question("DS3850", "Which is (would be if it weren't text) an integer?", ["3.12", "5", "seven", "steve"], 1),
    Question("DS3850", "How do you write comments?", ["#", "begin with the word comment", "$", "()"], 0),
    Question("DS3850", "What does GUI stand for?", ["good under illusion", "don't know", "graphical user interface", "given understood interests"], 2),
    Question("DS3850", "Should AI be used?", ["NO!", "all the time", "not at first(except maybe to check), but more as we progress", "maybe"], 2),

    Question("FIN3210", "What is often considered above the CEO in an organization?", ["no superiors", "stock holders", "the gov.", "board of directors"], 3),
    Question("FIN3210", "What is a disadvantage of a corporation?", ["unlimited life", "double taxation", "limited liability", "none"], 1),
    Question("FIN3210", "What should a stock price be?", ["equal its intrinsic value", "$500", "unlimited money", "nothing"], 0),
    Question("FIN3210", "What is a market by definition?", ["the internet", "McDonalds", "a venue where goods and services are exchanged", "Facebook"], 2),
    Question("FIN3210", "Types of financial institutions include:", ["investment banks", "commerical banks", "pension funds", "all of the above"], 3),
    Question("FIN3210", "What is an IPO?", ["I Ponder Often", "Incredible Penguin Org.", "Interest Paid Off", "Inital Public Offering"], 3),
    Question("FIN3210", "Which of these is one of the four main financial statements?", ["p/e ratio", "balance sheet", "verbal section", "lease"], 1),
    Question("FIN3210", "What is the difference between an annuity and annuity due?", ["they are the same", "they are paid at different times within each period", "only one needs paid", "I'm not sure"], 1),
    Question("FIN3210", "How many buttons on the financial calc. is usually required to solve TVM problems?", ["5", "3", "4", "1"], 0),
    Question("FIN3210", "Why do companies usually sell bonds?", ["stocks are better", "they don't", "stocks are worse", "they tend to be less restrictive than bank covenants on loans"], 3),

    Question("DS3620", "What is business analytics (simplified)?", ["data", "combination of qualitative reasoning and quantitative methods", "exactly how companies work", "a class"], 1),
    Question("DS3620", "What is population data?", ["all items of interest", "subset", "small group", "sample"], 0),
    Question("DS3620", "What is a time series for?", ["measuring time", "recording info. in equal time periods", "change in y", "change in x"], 1),
    Question("DS3620", "What is a variable?", ["a word", "a number", "something that stores info. that can be recorded", "something that remains unchanging at all times"], 2),
    Question("DS3620", "What is a dummy variable", ["a variable that isn't bright", "72", "an extremely complex variable", "a numeric representation of a categorical variable"], 3),
    Question("DS3620", "What is the simplest measure of dispersion?", ["mean", "range", "mode", "standard deviation"], 1),
    Question("DS3620", "The mean absolute deviation is a measure of dispersion?", ["no", "yes", "maybe", "not sure"], 1),
    Question("DS3620", "Pie charts and bubble charts are great?", ["63", "yes", "sometimes", "no, they should be avoided"], 3),
    Question("DS3620", "What does a contingency table do?", ["nothing", "lists numeric variables in order", "shows the frequencies for two categorical variables", "splits tables so info. can be read easier"], 2),
    Question("DS3620", "What is y called in linear regression?", ["simply the output", "no name", "target or response variable", "whatever you want"], 2),

    Question("BMGT3510", "What are personal values?", ["stable over time and motivational", "constantly changing", "don't vary across generations and culture", "not motivational"], 0),
    Question("BMGT3510", "What is cognitive dissonance?", ["simultaneous conflicting cognitions", "comfort", "anger", "sadness"], 0),
    Question("BMGT3510", "What are some of the benefits of orginizational citizenship behavior?", ["all of the choices", "higher productivity", "improved job satisfaction", "lower turnover"], 0),
    Question("BMGT3510", "What is discretionary effort", ["working because you identify with the work and it means a lot to you", "working for a paycheck", "working for fun", "working when you want to"], 0),
    Question("BMGT3510", "What is the strongest importance of a competitive edge among these?", ["increasing efficiency and positivity", "it makes your company look better", "means more work", "means more profit"], 0),
    Question("BMGT3510", "Why are stereotypes most often harmful?", ["may or may not be accurate", "take a lot of thought", "are focused on postive qualities", "are not widespread"], 0),
    Question("BMGT3510", "What are causual attributions?", ["suspected or inferred causes of behavior", "what is seen", "what is explained", "I don't know"], 0),
    Question("BMGT3510", "According to Kelley's Model of Attribution what is one of the three dimensions of behavior", ["concensus", "1st", "space", "mind"], 0),
    Question("BMGT3510", "According to the OB book how many layers of diversity are there?", ["4", "3", "1", "5"], 0),
    Question("BMGT3510", "What are the two main types of goals?", ["small and large", "short-term and long-term", "performance and learning", "whatever you want"], 2),

    Question("DS3860", "What is a relational database?", ["a database", "a self describing collection of integrated data and relationships", "multiple databases", "I don't know"], 1),
    Question("DS3860", "How many main types of data are there?", ["1", "2", "3", "4"],3),
    Question("DS3860", "What is a primary key?", ["any attribute", "any attribute or collection that can uniquely identify a row", "a field", "the first row in a table"], 1),
    Question("DS3860", "What is a foreign key?", ["42", "a key from a different country", "any attribute", "an attribute in one table that contains the primary key in another"], 0),
    Question("DS3860", "How many types of databases are there?", ["1", "2", "3", "quite a few but we only focus on a couple such as relational databases"], 3),
    Question("DS3860", "NOSQL means?", ["no SQL", "numbered SQL", "not only SQL", "I'm unsure"], 2),
    Question("DS3860", "Is ACID Compliance important", ["yes very (but they aren't always e.g. may favor BASE)", "sometimes", "maybe", "not sure"], 0),
    Question("DS3860", "Can you create a union of tables with different data types?", ["not sure", "sometimes", "yes", "no"], 3),
    Question("DS3860", "What is an entity?", ["distinct, identifiable object or concept that can be stored and managed", "only names", "only places", "only verbs"], 0),
    Question("DS3860", "Is a many to many relationship OK?", ["yes", "not really, an intersection should be used", "not sure", "maybe"], 1)
    ]

save_many_questions(questions)

    
