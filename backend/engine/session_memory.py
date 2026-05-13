class SessionMemory:

    def __init__(self):

        self.questions = []

        self.answers = []

        self.reasoning = []

    def add(self,
            question,
            answer):

        self.questions.append(
            question
        )

        self.answers.append(
            answer
        )

    def get_context(self):

        context = ""

        for q, a in zip(
            self.questions,
            self.answers
        ):

            context += (
                f"Q:{q} A:{a}\n"
            )

        return context