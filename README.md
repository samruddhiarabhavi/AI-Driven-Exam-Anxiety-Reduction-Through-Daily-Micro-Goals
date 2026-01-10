🧠 AI-Driven Exam Anxiety Reduction Through Daily Micro-Goals
📌 Project Overview

This project is a Python-based AI Exam Guide system designed to reduce exam anxiety by breaking syllabus preparation into small, achievable daily micro-goals, tracking progress trends, and generating personalized encouragement messages.
Instead of focusing only on marks, the system emphasizes confidence, consistency, and mental well-being during exam preparation.

This project was built as part of the Theta Dynamics Hackathon Assessment.

🎯 Problem Statement

Students often feel overwhelmed during exam preparation due to:

Lack of clear daily goals

No visibility into real progress

Absence of positive reinforcement

This system addresses these issues using data-driven insights and AI-based logic to support students psychologically while improving academic outcomes.

🛠️ Tools & Technologies Used
🔹 Backend & Logic

Python

Flask (REST APIs & routing)

SQLAlchemy ORM

SQLite Database

Blueprint architecture for modular routing

🔹 Data & Analytics

Pandas & NumPy – performance analysis

Custom rule-based logic for:

Micro-goal generation

Confidence & readiness scoring

Progress trend analysis

🔹 AI / Intelligence Layer

Daily micro-goal engine

Confidence & exam readiness score (0–100)

Encouragement message generator based on real data

Anxiety signal detection using consistency trends

🔹 Frontend

HTML, CSS, JavaScript

Chart.js / Plotly for progress visualization

Minimal, student-first UI (non-competitive design)

🧩 System Architecture
User (Student)
   ↓
Flask REST APIs
   ↓
AI Logic & Analytics Engine
   ↓
Database (SQLite)
   ↓
Dashboard (HTML/CSS/JS)

⚙️ Key Features
✅ Daily Micro-Goal Engine

Converts syllabus + performance into 2–4 small daily goals

Time-boxed and low cognitive load

Example:

“Revise formulas of Chapter 3 (20 mins)”

“Attempt 5 medium questions without time pressure”

📊 Progress Tracking & Confidence Score

Tracks:

Study consistency

Completion streaks

Improvement trends

Effort vs outcome ratio

Generates:

Confidence Score (0–100)

Exam readiness indicator

💬 Encouragement & Feedback Engine

Generates empathetic, non-judgmental messages

Based on real student data

Examples:

“Your accuracy improved by 12% this week — keep going 💪”

“Consistency matters more than speed. You’re on track.”

🖥️ Student Dashboard

Displays:

Today’s micro-goals

Confidence trend graph

Progress history

One positive reinforcement message

🚫 No ranking or competitive elements (anxiety-free UX)


🚀 How to Run the Project
1️⃣ Clone the Repository
git clone <your-repo-link>
cd project_root

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install flask sqlalchemy pandas numpy

4️⃣ Run the Application
python app.py


Open browser:

http://127.0.0.1:5000

📸 Results & Screenshots

🔹 Signup and Login 

<img width="1895" height="919" alt="ex1" src="https://github.com/user-attachments/assets/32ebbba2-bb15-4b47-964a-245565d773f9" />

<img width="1887" height="906" alt="ex 2" src="https://github.com/user-attachments/assets/fb5866fa-750e-4013-8a50-47e09eb37285" />


🔹 Student Dashboard

<img width="1886" height="923" alt="ex dash" src="https://github.com/user-attachments/assets/2530ad20-6f49-4eb4-b1b4-5aba0b527ea5" />

🔹 Daily Micro-Goals

<img width="1888" height="914" alt="es dash2" src="https://github.com/user-attachments/assets/04235ff5-d54b-4dcd-a87c-17ab195e87e5" />

<img width="1885" height="916" alt="ex dash3" src="https://github.com/user-attachments/assets/5bf50015-f3d8-4c85-a8e3-bd4c53a929dc" />

<img width="1852" height="913" alt="ex dash4" src="https://github.com/user-attachments/assets/e438de62-a656-425d-a4bd-2660ecc30feb" />

🔹 Parent Dashboard

<img width="1889" height="925" alt="ex parent" src="https://github.com/user-attachments/assets/95bf846c-fa8f-4603-9416-1e90c9a9fa48" />


🧠 Assessment Alignment (Why This Solves the Problem)

✔ Converts syllabus into achievable micro-goals
✔ Tracks confidence instead of just marks
✔ Uses AI-driven encouragement
✔ Reduces anxiety through consistency visualization
✔ Student-first, pressure-free design

🏁 Conclusion

This project demonstrates how AI + data analytics + psychology can be combined to support students emotionally while improving exam preparedness.
It focuses on confidence building, habit formation, and stress reduction, not just academic performance.

👩‍💻 Author

Samruddhi Arabhavi
Computer Science & Engineering
Python | Flask | AI | Data Analytics
