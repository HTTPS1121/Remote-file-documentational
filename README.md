# תיעוד קבצים - File Documentation System

מערכת לניהול ותיעוד קבצים עם ממשק משתמש בעברית. המערכת מאפשרת ניווט בתיקיות, הצגת מידע על קבצים, וייצוא נתונים בפורמט תמונה.

- (נכתב בעזרת Claude, בתוך Cursor)

## תכונות עיקריות

- **ניווט בתיקיות**: ניווט נוח במערכת הקבצים עם אפשרות להזנת נתיב ידנית
- **תצוגת קבצים**: הצגת רשימת קבצים עם מידע מפורט כולל גודל ומשך (לקבצי מדיה)
- **סינון**: אפשרות לסינון לפי סוגי קבצים (MP3, MP4)
- **מיון**: מיון לפי שם, גודל או משך
- **התאמה אישית**: שליטה מלאה על מראה הטבלה כולל רוחב עמודות, עובי קווים ועיגול פינות
- **ייצוא**: ייצוא הנתונים כתמונה (JPG/PNG) עם אפשרות לייצוא נפרד של קבצי אודיו ווידאו

## דרישות מערכת

### Backend
- Python 3.8+
- Flask 2.3.3
- Werkzeug 2.3.7
- Flask-CORS 3.0.10
- Mutagen 1.45.1
- Pathlib 1.0.1

### Frontend
- Node.js 14+
- React 18.2.0
- html2canvas 1.4.1

## התקנה

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## שימוש

1. הפעל את השרת Backend בפורט 5000
2. הפעל את האפליקציית Frontend בפורט 3000
3. גש ל-`http://localhost:3000` בדפדפן

### תכונות עיקריות

- **ניווט**: השתמש בסייר הקבצים בצד שמאל או הזן נתיב ידנית
- **סינון**: בחר סוגי קבצים לסינון בפאנל התחתון
- **ייצוא**: השתמש בכפתורי הייצוא בתחתית המסך לשמירת הנתונים כתמונה
- **התאמה אישית**: לחץ על כפתור ההגדרות (⚙️) לשליטה במראה הבלה

## הגדרות

### הגדרות טבלה
- רוחב עמודות (שם, גודל, משך)
- עובי קווים אופקיים ואנכיים
- עובי מסגרת חיצונית
- עיגול פינות
- הצגת סיומות קבצים

### הגדרות ייצוא
- בחירת פורמט: JPG או PNG
- ייצוא מלא או ייצוא נפרד לקבצי אודיו/וידאו

## צילומי מסך

### ככה זה נראה באמצעות הכלי שכתבתי 👍

![1](https://github.com/user-attachments/assets/dcb665f8-0ae3-4e1d-8dd4-5d2229e795f1)
![2](https://github.com/user-attachments/assets/27e0f0b4-b164-44d3-982d-c994773e06f8)
![3](https://github.com/user-attachments/assets/dcb51ccf-83a8-4cc0-9eea-a9bb5431e0c5)
### ככה זה היה נראה עד עכשיו 🙈
![4](https://github.com/user-attachments/assets/c5523973-cd67-4ff8-80a3-bcd972208077)

