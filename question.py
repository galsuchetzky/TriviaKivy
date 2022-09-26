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
