class Question:
    '''
    Holds data concerning a question

    Properties:
        q_string (str): The actual question
        q_class (str): The class of question (WH word or binary)
        q_answer (str): The answer to the question 
    '''
    
    def __init__(self, question, klass, answer):
        self.q_string = question
        self.q_class = klass
        self.q_answer = answer
        