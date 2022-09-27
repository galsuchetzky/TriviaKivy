import random

from utils import fix_string

class Question:
    """
    Represents a question in the game.
    """

    def __init__(self, question_dict):
        """
        Initiates a new question from a python dict of the following format:
        {
            "index": 5,
            "question": "your question here",
            "correct": 0,
            "ans0": "a",
            "ans1": "b",
            "ans2": "c",
            "ans3": "d"
        }
        :param question_dict: the question dict.
        """
        self.index = question_dict["index"]
        self.question = fix_string(question_dict["question"])
        self.correct_answer = int(question_dict["correct"])
        self.answers = []

        for i in range(4):
            tag = 'ans' + str(i)
            self.answers.append(fix_string(question_dict[tag]))

    def shuffle_answers(self):
        """
        Shuffles the answers of the question.
        """

        answers = list(enumerate(self.answers))
        random.shuffle(answers)
        for i in range(4):
            self.answers[i] = answers[i][1]
            if answers[i][0] == self.correct_answer:
                self.correct_answer = i
                return

if __name__ == '__main__':
    q_j ={
        "index": 9,
        "question": "כרישים ניזונים מצבי ים. צבי הים ניזונים מעשב ים. דגים מטילים ביצים בתוך עשב הים ושם הן מוגנות. אם יהיה דיג מוגבר של כרישים, מה צפוי לקרות במערכת אקולוגית זו ?",
        "correct": 0,
        "ans0": "תהיה עלייה בכמות צבי הים וירידה בכמות הדגים",
        "ans1": "תהיה ירידה בכמות צבי הים וירידה בכמות עשב הים.",
        "ans2": "תהיה עלייה בכמות עשב הים ועלייה בכמות הדגים.",
        "ans3": "תהיה עלייה בכמות צבי הים ועלייה בכמות עשב הים."
	}


    q = Question(q_j)
    print()
    q.shuffle_answers()
    print