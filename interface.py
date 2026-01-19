from llm_client import LLMClient
from players import Player1, Player2
from game import GameState

#creating class for game interface 

class GameInterface:
    def __init__(self):
        self.llm_client = LLMClient()
    
    def show_menu(self):
        # Show game mode options and return user's choice
        print("\n" + "="*50)
        print("TWENTY QUESTIONS GAME")
        print("="*50)
        print("1. Human (Player 1) vs LLM (Player 2)")
        print("2. LLM (Player 1) vs Human (Player 2)")
        print("3. LLM (Player 1) vs LLM (Player 2)")
        print("="*50)

        while True:
            choice = input("Select mode (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                return choice
            print("Invalid choice. Please enter 1, 2, or 3.")

    def run_game(self, player1, player2, game_state):
        
        """Main game loop."""
        print("\n" + "="*50)
        print("GAME START!")
        print("="*50)

        #while game is running
        while not game_state.is_game_over():
            # player 2 asks a question
            question = player2.ask_question(game_state)
            print(f"\nPlayer 2 asks: {question}")
        
            # check if it's a guess:
            words = question.lower().strip().split()
            is_guess = (
                len(words) >= 4 and 
                words[0] == "is" and 
                words[1] == "it" and 
                words[2] in ["a", "an", "the"]
            )
        
            if is_guess:
                # Extract the guessed object
                guess = question.lower().replace("is it", "").replace("?", "").strip()
                guess = guess.replace("a ", "").replace("an ", "").replace("the ", "").strip()
            
                # check if correct
                if game_state.check_correct_guess(guess):
                    # player 2 wins - Record as "yes" answer
                    game_state.add_question_answer(question, "yes")
                    break
                else:
                    # wrong guess - ask player 1 to confirm it's not that object
                    answer = player1.answer_question(question, game_state)

            else:
                # regular question - get answer from Player 1
                answer = player1.answer_question(question, game_state)
        
            print(f"Player 1 answers: {answer}")
        
            # record question and answer pair 
            if not (is_guess and game_state.status == "player2_wins"):
                game_state.add_question_answer(question, answer)
    
        # Game is over 
        self.display_results(game_state)

    def display_results(self, game_state):  
        #Showing final results 
        print("\n" + "="*50)
        print("GAME OVER!")
        print("="*50)

        if game_state.status == "player2_wins":
            print("Player 2 wins! They guessed the object!")
            print(f"The object was: {game_state.secret_object}")
        else:
            print("Player 1 wins! Player 2 ran out of questions.")
            print(f"The secret object was: {game_state.secret_object}")

        print(f"Total questions asked: {game_state.question_count}/{game_state.MAX_QUESTIONS}")

        # Show history
        print("\nGame History:")
        for i, qa in enumerate(game_state.history, 1):
            print(f"  {i}. Q: {qa['question']}")
            print(f"     A: {qa['answer']}")    