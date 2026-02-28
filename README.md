Trivia Programming Game
A joyful trivia game where players can choose their level of difficulty and answer questions about software.

Project Description
This project is a terminal-based trivia game developed as part of the Algorithms and Programming course.
The system manages multiple players, tracks scores, and handles questions dynamically using Object-Oriented Programming (OOP) principles.

Features
OOP Architecture: Uses classes to model questions and game logic.

Data Persistence: Loads questions from a JSON file.

Error Handling: Implements try-except blocks to manage invalid user inputs.

Dynamic Content: Supports fetching additional questions via API (Requests).

How to Run
The game is executed via the command line using argparse. Use the following command format:
python trivia.py questions.json 1
Note: The first argument is the JSON file, and the second is the number of players. The more players in the game, the higher the number you should write.
