# StudySense 📚⏱️

StudySense is a smart study tracking web app built with **Flask** that helps students monitor study sessions, track focus efficiency, visualize analytics, and stay consistent with goals.

## ✨ Features

- Add and manage daily study sessions
- Track:
  - Subject
  - Study hours
  - Break time
  - Focus score / efficiency
- Dashboard metrics:
  - Total study hours
  - Most studied subject
  - Average break time
  - Focus efficiency
- Study streak tracking 🔥
- Daily goal progress bar 🎯
- Date-range filtering
- Export report as CSV
- Simple and clean UI for quick usage

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Bootstrap, Jinja2
- **Data Handling:** Pandas / CSV-based storage
- **Visualization:** Matplotlib/Seaborn (if used in your project)

## 📂 Project Structure

```bash
StudySense/
│── app.py
│── requirements.txt
│── data/
│   └── study_data.csv
│── static/
│   ├── css/
│   ├── js/
│   └── graphs/
│── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── analytics.html
│   └── ...
└── README.md
```

## ⚙️ Installation & Run

```bash
# 1) Clone repo
git clone [https://github.com/classyyfr/StudySense.git] or (https://github.com/SuyashPatil02/StudySense.git)
cd StudySense

# 2) Create virtual environment
python -m venv venv

# 3) Activate venv
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# 4) Install dependencies
pip install -r requirements.txt

# 5) Run app
python app.py
```

Open in browser:  
`http://127.0.0.1:5000`

## 📸 Screenshots

- Dashboard
- <img width="986" height="480" alt="image" src="https://github.com/user-attachments/assets/cd9f2d53-dade-442e-8b6a-6b3915cbd10c" />

- Analytics Graphs
- <img width="1293" height="871" alt="image" src="https://github.com/user-attachments/assets/f0e9d495-d929-4f93-9ded-25cb955c1d2b" />

- Recommendations Page
- <img width="1917" height="912" alt="image" src="https://github.com/user-attachments/assets/e1573f95-7d46-4545-9e57-e6091a0b12b6" />

- Goal Progress / Streak Card
<img width="1542" height="193" alt="image" src="https://github.com/user-attachments/assets/171aa19f-e269-4e3a-b9bb-3b35ea0b7a7c" />

## 🚀 Future Enhancements

- User authentication (Login/Signup)
- Cloud database (SQLite/MySQL/PostgreSQL)
- AI-based study recommendations
- Weekly email reports
- Notifications
- Converting into Applications 

## 👨‍💻 Contributors

- [@classyyfr](https://github.com/classyyfr)
- [@SuyashPatil02](https://github.com/SuyashPatil02)

## 📜 License

This project is for educational/final-year academic use.
