# artificial-interview
AI Engineer Intern Technical Task - Dilip Balakrishnan

Part 1 (user playing with LLM) and 2 (LLM playing with LLM) have been implemented in the various files through a CLI. 

Some techniques used to ensure that the program doesn't have any unexpected behaviour include:

1. Input validation - in interface.py, users are forced to select a specific mode and only 1, 2, or 3 is acepted. 

2. Retry logic with fallbacks in LLM API calls - in players.py, Player1._llm_answer() and Player2._llm_ask() both allow up to 3 retries before defaulting to a fallback. This would prevent LLMs from continually returning unexpected formats and ensures that the program never crashes from bad LLM response.

3. Enforcing 20 question limit: in game.py, GameState.add_question_answer() ensures that the game continues until 20 questions have been used.

Part 3: 

Implementing a scheme to automatically evaluate performance of LLM as player 1 and player 2.

As player 1 and 2 answer and ask questions respectively, the considerations for evaluation are different for each of them. 

For player 1, key performance metrics could include: accuracy of answers, consistency and object selection quality. 

Accuracy of answers would involve the use of a judge LLM to verify whether answers are factually correct given the secret object. For each question-answer pair, the judge evaluates whether it is correct, incorrect or ambiguous. Accuracy score could be determined by using (correct answers / total questions) * 100. 

Consistency would involve checking for logical contradictions across answers in the same game using semantic similarity and logical reasoning. Consistency rate could be penalised. 

Object selection quality would involve evaluating whether the chosen secret object is appropriate for the game. This would mean checking if the object that has been selected is well-defined and concrete (e.g.: bicycle, laptop) instead of something that is too vague. 

To evaluate player 1 using the aforementioned metrics, a separate LLM instance could be started to review all Q&A pairs with the prompt: "Given the secret object is 'object', evaluate if answering 'answer' to the question 'question' is factually correct. Rate as: correct/incorrect/ambiguous. Use the following formula to calculate player 1 score: player1_score = (accuracy + consistency + object_quality) / 3. Accuracy should be evaluated using (correct answers / total questions) * 100, consistency should be evaluated using semantic similarity between related questions and logical inference rules. Object selection quality should be rated by checking if the object is well-defined and concrete instead of something that is too vague"

For player 2, key performance metrics would involve: win rate, efficiency and information gain. 

Win rate would involve the percentage of games won on a standardised test set. Efficiency would involve number of questions required to win. Efficiency should be measured on won games. Information gain would involve assessing how much each question narrows down possibilities. In addition to the performance metrics, imposing penalties for wrong guesses and question quality would also help. 

These metrics can be captured using a reward function that adds win rate, efficiency and information gain per question and subtracts points for wrong guesses and unclear questions. 

Some possible emergent behaviours would include the following:

1. Strategic guessing: Only making specific types of guesses (e.g.: "Is it X?") when confidence is high. (e.g.: in situations when LLM is guessing after narrowing to 2-3 likely options.). To encourage this, heavy penalty could be given for incorrect guesses. 

2. Guess spamming: Making many rapid low-confidence guesses hoping to get lucky (e.g: "Is it an apple", "Is it a chair" etc for more than 10 questions). To discourage such behaviour, heavy pentalty could be given for incorrect guesses. 

