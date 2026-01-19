
#creating GameState class to track everything in the game

class GameState:

    #imposing max questions
    MAX_QUESTIONS = 20

    def __init__(self, secret_object):
        self.secret_object = str(secret_object)
        self.question_count = 0  
        self.history = []  
        self.status = "in_progress" 
    
    def add_question_answer(self, question, answer):
        #add Q&A pair and increase count
        self.history.append({"question": question, "answer": answer})
        self.question_count += 1

        #checking if player 2 has run out of questions
        if self.question_count >= self.MAX_QUESTIONS and self.status == "in_progress":
            self.status = "player1_wins"

    def is_game_over(self):
        #checking if game is over
        return self.status != "in_progress"

    def check_correct_guess(self,guess):
        #checking if player 2's guess is correct 
        if guess.lower() == self.secret_object.lower():
            self.status = "player2_wins"
            return True
        return False
    
    