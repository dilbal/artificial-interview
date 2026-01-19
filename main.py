from interface import GameInterface
from players import Player1, Player2
from game import GameState
from llm_client import LLMClient

def main():
    interface = GameInterface()
    llm_client = LLMClient()
    
    # show menu and get choice
    choice = interface.show_menu()
    
    # initialize players and game based on choice
    if choice == "1":
        # human is player 1, LLM is player 2
        secret = input("\nYou are Player 1. Think of an object and type it here: ").strip()
        player1 = Player1(secret_object=secret, is_human=True)
        player2 = Player2(is_human=False, llm_client=llm_client)
        game_state = GameState(secret_object=secret)
        
    elif choice == "2":
        # LLM is player 1, human is player 2
        print("\nLLM is thinking of an object...")
        secret = llm_client.get_response("Think of a common object for a game of twenty questions. Respond with ONLY the object name, nothing else. Make it a concrete, specific object.")
        print(f"LLM has chosen an object! (Hidden from you)")
        player1 = Player1(secret_object=secret, is_human=False, llm_client=llm_client)
        player2 = Player2(is_human=True)
        game_state = GameState(secret_object=secret)
        
    else:  # choice == "3"
        # both are LLMs
        print("\nLLM (Player 1) is thinking of an object...")
        secret = llm_client.get_response("Think of a common object for a game of twenty questions. Respond with ONLY the object name, nothing else. Make it a concrete, specific object.")
        player1 = Player1(secret_object=secret, is_human=False, llm_client=llm_client)
        player2 = Player2(is_human=False, llm_client=llm_client)
        game_state = GameState(secret_object=secret)
    
    # run game
    interface.run_game(player1, player2, game_state)

if __name__ == "__main__":
    main()