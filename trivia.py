import json, random, argparse, requests
from pydantic import BaseModel

class QuestionModel(BaseModel):
    question: str; options: list[str]; correct: str; category: str; difficulty: str

class TriviaGame:
    def __init__(self, json_file, num_players):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.local_questions = [QuestionModel(**q) for q in json.load(f)]
        

        diff_choice = input("Select difficulty (easy, medium, hard): ").strip().lower()
        self.web_questions = []

        try:
            url = f"https://opentdb.com/api.php?amount=20&category=18&difficulty={diff_choice}&type=multiple"
            resp = requests.get(url).json()
            for item in resp.get('results', []):
                opts = item['incorrect_answers'] + [item['correct_answer']]
                self.web_questions.append(QuestionModel(
                    question=item['question'], options=opts, correct=item['correct_answer'], 
                    category="Computers", difficulty=item['difficulty']))
        except: pass

        
        if len(self.web_questions) < 20:
            extra = [q for q in self.local_questions if q not in self.web_questions]
            random.shuffle(extra)
            self.web_questions += extra[:20 - len(self.web_questions)]
        
        random.shuffle(self.web_questions)
        self.players = [{"name": f"Player {i+1}", "score": 0} for i in range(num_players)]

    def run(self):
        p_idx, current_q = 0, None
        while self.web_questions or current_q:
            player = self.players[p_idx]

            if not current_q:
                current_q = self.web_questions.pop(0)
                random.shuffle(current_q.options)

            print(f"\n{player['name']}'s Turn | {current_q.category} ({current_q.difficulty})")
            print(f"Question: {current_q.question}")
            for i, opt in enumerate(current_q.options, 1): print(f"{i}. {opt}")
 
            try:
                ans = int(input("Answer #: "))
                if current_q.options[ans-1] == current_q.correct:
                    print("Correct!"); player['score'] += 1
                    current_q = None 
                else:
                    print("Wrong! Same question for next player.")

            except (ValueError, IndexError):
                print("Invalid input! Use numbers only.")
                continue 
            
            p_idx = (p_idx + 1) % len(self.players)
        self.end_game()

    def end_game(self):
        print("\n--- Final Scores ---")
        for p in self.players: print(f"{p['name']}: {p['score']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file"); parser.add_argument("players", type=int)
    args = parser.parse_args()
    TriviaGame(args.file, args.players).run()