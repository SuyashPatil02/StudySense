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
git clone https://github.com/classyyfr/StudySense.git
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

> Add your screenshots here before final submission.

- Dashboard
- Analytics Graphs
- Recommendations Page
- Goal Progress / Streak Card

## 🚀 Future Enhancements

- User authentication (Login/Signup)
- Cloud database (SQLite/MySQL/PostgreSQL)
- Pomodoro timer integration
- AI-based study recommendations
- Weekly email reports

## 👨‍💻 Contributors

- [@classyyfr](https://github.com/classyyfr)
- [@SuyashPatil02](https://github.com/SuyashPatil02)

## 📜 License

This project is for educational/final-year academic use.
