# Chemical Equipment Parameter Visualizer
**Hybrid Web & Desktop Analytics Application**

---

## Introduction
The **Chemical Equipment Parameter Visualizer** is a full-stack analytics system designed to analyze chemical equipment data from CSV files and present meaningful insights through modern visualizations.

The system supports **both Web and Desktop applications**, powered by a **single shared Django REST backend**, ensuring consistency, scalability, and maintainability.

---

## Problem Statement
Analyzing raw CSV files containing chemical equipment parameters is error-prone and inefficient when done manually.

This project solves that problem by providing:
- Automated statistical analysis
- Interactive data visualization
- Historical tracking of uploads
- Exportable analytical reports

---

## Solution Overview
Users upload a CSV file containing equipment parameters.  
The system processes the data and provides:
- Summary statistics
- Visual charts
- Upload history
- PDF reports

This solution is ideal for **chemical labs, students, and data analysts**.

---

## Tech Stack

### Backend
- **Python**
- **Django**
- **Django REST Framework**
- **Pandas**
- **SQLite**
- **ReportLab (PDF generation)**

### Web Frontend
- **React.js**
- **Chart.js**
- **Axios**
- **CSS (Glassmorphism UI)**

### Desktop Frontend
- **PyQt5**
- **Matplotlib**
- **Requests**

---

## Features

### Core Features
✔ CSV file upload (Web & Desktop)  
✔ Automatic data validation  
✔ Summary statistics calculation  
✔ Equipment type distribution (Pie Chart)  
✔ Flowrate trend visualization (Desktop)  

### Advanced Features
✔ Upload history (last 5 datasets)  
✔ PDF report generation  
✔ Shared backend for Web & Desktop  
✔ Clean and responsive UI  
✔ Error handling and status feedback  

---

## Application Modes

### Web Application
- Runs in the browser
- Modern dashboard UI
- Interactive charts
- Upload history display
- PDF report download

### Desktop Application
- Native PyQt5 application
- KPI cards and charts
- Upload history support
- PDF report generation
- Uses the same backend API

---

## API Endpoints

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/api/upload/` | Upload CSV and get summary |
| GET | `/api/history/` | Fetch last 5 uploads |
| GET | `/api/report/pdf/` | Download PDF report |

---

## Project Structure
chemical-equipment-visualizer/
│
├── backend/
│ ├── analyzer/
│ ├── backend/
│ ├── manage.py
│ └── requirements.txt
│
├── web-frontend/
│ ├── src/
│ ├── public/
│ └── package.json
│
├── desktop-app/
│ ├── app.py
│ └── requirements.txt
│
├── sample_equipment_data.csv
├── README.md
└── .gitignore

## Setup Instructions

### Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Backend runs at:
👉 http://127.0.0.1:8000

Web Frontend Setup
cd web-frontend
npm install
npm start
Web App runs at:
👉 http://localhost:3000

Desktop Application Setup
cd desktop-app
pip install -r requirements.txt
python app.py
Sample CSV Format
A sample CSV file (sample_equipment_data.csv) is provided for testing and demo purposes.
