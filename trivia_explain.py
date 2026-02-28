
#json -בשביל שהקובץ ידע לקרוא קבצים מסוג JSON 
#random-בשביל לבחור בצורה רנדומלית את השאלה מהספריה
#argparse-נותן יכולת להשפיע על התוכנית דרך הטרמינל
#requests-מעביר את המידע מהספריה אל קובץ בפורמט של JSON
#pydantic-מוודא שהמידע שבא מהאינטרנט עומד בסטנדרטים שקבענו 
import json, random, argparse, requests
from pydantic import BaseModel

#יצירת קלאס הbaseModel עושה מאחורי הקלעים את התבנית המוכרת של יצירת עצם עם self .
#העצם קובע את התבנית של מה שאנחנו מקבלים מAPI מתי רשימה מתי סטרינג וכו'
class QuestionModel(BaseModel):
    question: str; options: list[str]; correct: str; category: str; difficulty: str

#יצירת קלאס חדש , self מייצג מופע ספציפי של האובייקט שנוצר כרגע
#json_file הוא המסמך של השאלות שלי ,num_players הוא משתנה שמייצג את מספר המשתתפים
#משתמשים ב with כדי לפתוח את הקובץ אבל גם לסגור אותו 
#הקובץ שפותחים הוא json_file ,משתמשים באות r' שזה קריאה ולא עריכה מחיקה וכו' 
#אנו ממירים את השפה הבוליאנית שמתקבלת על ידי encoding utf8 הינו לשפה של בני אדם 
#מגדירים את הקובץ כמשתנה בשם f 

#הוספנו מאפיין חדש לעצם שנקרא self.local_questions
#אנחנו יוצרים עצמים של QuestionModel על ידי הזנה של נתונים לאובייקטים החדשים מהמסמך שלנו 
#עושים לולאה שטוענת את המסמך שהגדרנו כf
class TriviaGame:
    def __init__(self, json_file, num_players):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.local_questions = [QuestionModel(**q) for q in json.load(f)]
        
#בחירת רמת קושי + הורדה של רווחים מהקצוות ובמקרה של אותיות גדולות להפוך לקטנות 
#הוספה של מאפיין חדש לעצם שהוא רשימה
        diff_choice = input("Select difficulty (easy, medium, hard): ").strip().lower()
        self.web_questions = []
#למקרה והשרת קורס משתמשים בtry 
# משיכת שאלות מחשבים (18) ברמה שנבחרה
#מבקשים בresp מהאתר לקבל ומה שאנו מקבלים ממירים לפורמט JSON
#עושים לולאה על התגובה ,"results" זה חלק מהסינטקס של הסיפריה 
#שמנו [] למקרה ולא קיבלנו תשובה שיהיה כבררת מחדל רשימה ריקה
#בתוך המשתנה opts שמים את הערכים של המילון שנמצא בספריה תשובת נכונות ולא נכונות
#מכניסים את השאלות שהם העצמים לרשימה 
#במקרה ויש תקלה אל תקריס את הקוד אלא תתעלם על ידי pass 
        try:
            url = f"https://opentdb.com/api.php?amount=20&category=18&difficulty={diff_choice}&type=multiple"
            resp = requests.get(url).json()
            for item in resp.get('results', []):
                opts = item['incorrect_answers'] + [item['correct_answer']]
                self.web_questions.append(QuestionModel(
                    question=item['question'], options=opts, correct=item['correct_answer'], 
                    category="Computers", difficulty=item['difficulty']))
        except: pass

        # אם חסר כמות של 20 שאלות
        #list comperhntion - עושים לולאה עם משתנה זמני q ועוד אחד בגלל סינטקס ובודקים אם הם לא נמצאים בשאלות שכבר השגנו מהספריה
        #מערבבים את השאלות המקומיות שעשינו שלא יקבל כל הזמן אותן שאלות 
        #מוסיפים את השאלות שחסרות 
        #מערבבים את ה20 שאלות המוכנות 
        #list comperhention שיוצר מילון . אנחנו יוצרים תכונה חדשה בעצם של מילון של שחקנים 
        #הi מתחיל מ0 וכולם מתחילים בניקוד 0 ועושים לולאה על פי הכמות שהגדיר הלקוח ככה הלולאה נעה 
        
        if len(self.web_questions) < 20:
            extra = [q for q in self.local_questions if q not in self.web_questions]
            random.shuffle(extra)
            self.web_questions += extra[:20 - len(self.web_questions)]
        
        random.shuffle(self.web_questions)
        self.players = [{"name": f"Player {i+1}", "score": 0} for i in range(num_players)]
#יוצרים פ. עם 2 משתנים אחד על מספר השחקן ואחד על שאלה נוכחית
#לולאה כל נותרו שאלות ברשימה או שיש עדיין שאלה שנוכחת 
#בודקים אל איזה שחקן פונים עכשיו
    def run(self):
        p_idx, current_q = 0, None
        while self.web_questions or current_q:
            player = self.players[p_idx]
#אם current_q הוא none 
#אם כן אתה לוקח את השאלה העליונה מוחק אותה מהמקור ושם אותה במשתנה current_q
#מערבבים את התוצאות האפשריות

            if not current_q:
                current_q = self.web_questions.pop(0)
                random.shuffle(current_q.options)
#מדפיסים את שם השחקן הקטגוריה והקושי ואז את השאלה הוא לא בוחר רמה אלא רואה 
#עושים לולאה עם משתנים זמניים של i,opt על current_q.options ומתחילים לספור מ1 ומדפיסים
            print(f"\n{player['name']}'s Turn | {current_q.category} ({current_q.difficulty})")
            print(f"Question: {current_q.question}")
            for i, opt in enumerate(current_q.options, 1): print(f"{i}. {opt}")
#שמים אינפוט לתשובה של הלקוח 
#העצם שבנינו יש לו מאפיין של options שבו נמצא הנכון והלא נכון גם יש לו מאפיין של correrct 
#אם הם זהים מדפיסים ומעלים ב1 את הניקוד(זה מילון)
#מחזירים את current_q 1 ל none כדי שהם יוכלו להיתקע על שאלה אם לא ענו ורק מתי שסיימו שימשיכו      
# עוברים לשאלה הבאה       
            try:
                ans = int(input("Answer #: "))
                if current_q.options[ans-1] == current_q.correct:
                    print("Correct!"); player['score'] += 1
                    current_q = None 
                else:
                    print("Wrong! Same question for next player.")
#חלק מהמנגנון שלא יקרוס הקוד אם הכניס תשובה לא חוקית
#הפרמטרים הם built in . בין אם יש טעות באינדקס או טעות בערך אל תקרוס 
#נעים במעגל על ידי מודלו 
#ברגע שאין שאלות מפעילים פונקצית end game
            except (ValueError, IndexError):
                print("Invalid input! Use numbers only.")
                continue 
            
            p_idx = (p_idx + 1) % len(self.players)
        self.end_game()
#הדפסה של תוצאה סופית
    def end_game(self):
        print("\n--- Final Scores ---")
        for p in self.players: print(f"{p['name']}: {p['score']}")

#בודקים אם הקובץ הופעל ישירות
#משתמשים ב argparse כדי לשלוט בתוכנית דרך הטרמינל .ArgumentParser מפענח איזה סוג ערך שמת אם זה דגל סטרינג וכו'
#מאלצים כדי להתחיל לרשום את שם הקובץ ומספר השחקנים 
#שומרים את המתונים במשתנה args
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file"); parser.add_argument("players", type=int)
    args = parser.parse_args()
    TriviaGame(args.file, args.players).run()