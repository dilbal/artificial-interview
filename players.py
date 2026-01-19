#implementing classes for the 2 players separately
from game import GameState

#class for player 1 (thinks of secret object and answers)
class Player1:
    def __init__(self, secret_object, is_human=True, llm_client=None):
        self.secret_object = secret_object
        self.is_human = is_human
        self.llm_client = llm_client

    def answer_question(self, question, game_state):
        
        if self.is_human:
            return self._human_answer(question)
        else:
            return self._llm_answer(question, game_state)
        
    def _human_answer(self, question):
        """Get yes/no answer from human player."""
        print(f"\nQuestion: {question}")
        print(f"Secret object: {self.secret_object}")                

        while True:
            answer = input("Your answer (yes/no): ").lower().strip()

            if answer in ["yes", "no"]:
                return answer
            else:
                print("Invalid input. Please answer 'yes' or 'no'.")
        
    def _llm_answer(self, question, game_state):
        #get yes/no ans from LLM

        history_context = ""    
        if game_state.history:
            history_context = "\n\nPrevious questions and answers:\n"
            for qa in game_state.history:
                history_context += f"Q: {qa['question']} - A: {qa['answer']}\n"

        prompt = f"""You are Player 1 in a game of Twenty Questions.
    Your secret object is: {self.secret_object}

    {history_context}

    Current question: {question}

    Answer ONLY with 'yes' or 'no' based on whether the question applies to {self.secret_object}.
    Do not include any explanation, just answer 'yes' or 'no'."""
    
        max_retries = 3
        for attempt in range(max_retries):
            response = self.llm_client.get_response(prompt)
            answer = response.lower().strip()

            if answer in ["yes", "no"]:
                return answer
            
            prompt += f"\n\nYour previous response '{response}' was invalid. Please respond with ONLY 'yes' or 'no'."

        #Fallback if all retries fail
        print(f"Warning: LLM failed to give valid answer after {max_retries} attempts. Defaulting to 'no'.")
        return "no"
    
#class for player 2 - the one who's trying to guess
class Player2:

    def __init__(self, is_human=True, llm_client=None):
        self.is_human = is_human
        self.llm_client = llm_client
    
    def ask_question(self, game_state):
        """
        Formulate and return the next question.
        Returns: a string question
        """
        if self.is_human:
            return self._human_ask(game_state)
        else:
            return self._llm_ask(game_state)
    
    def _human_ask(self, game_state):
        #get question from human player
        questions_remaining = game_state.MAX_QUESTIONS - game_state.question_count

        #count of number of qns
        print(f"\n{'='*50}")
        print(f"Question{game_state.question_count +1}/{game_state.MAX_QUESTIONS}")
        print(f"Questions remaining: {questions_remaining}")
        print(f"{'='*50}")

        #show history of qns previously asked
        if game_state.history:
            print("\nPrevious Q&A:")
            for qa in game_state.history[-5:]:
                print(f" Q: {qa['question']}")
                print(f" A: {qa['answer']}")

        #get question
        user_question = input("What is your question?  ").strip()
        return user_question
    
    def _llm_ask(self, game_state):
        #get question from llm player
        questions_remaining = game_state.MAX_QUESTIONS - game_state.question_count
        
        #build history context
        history_context = "" 
        if game_state.history:
            history_context = "Previous questions and answers:\n"
            for qa in game_state.history:
                history_context += f"Q: {qa['question']} - A: {qa['answer']}\n"
        
        prompt = f"""You are Player 2 in a game of Twenty Questions. Your goal is to guess the secret object.

        {history_context}
        You have {questions_remaining} questions remaining.

        Based on the information above, ask one strategic yes/no question to narrow down what the object is.
        If you're confident you know the answer, you can make a guess by asking "Is it [object]?"

        Respond with only your question, nothing else.
        """

        max_retries = 3
        for attempt in range(max_retries):
            response = self.llm_client.get_response(prompt)
            question = response.strip()

            #check if it looks like a question
            if question and len(question) > 0:
                return question
            
            #if invalid, try again with stronger prompt
            prompt += f"\n\nYour previous response was empty or invalid. Please provide a question."

        #Fallback if all retries fail - ask a generic question
        print(f"Warning: LLM failed to give valid answer after {max_retries} attempts. Using default fallback.")
        return "Is it a common household object?"

        