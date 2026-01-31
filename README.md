# Chemical Equipment Parameter Visualizer

A **hybrid web + desktop application** for uploading, analyzing, and visualizing chemical equipment parameter data from CSV files.

**GitHub Repository:** [https://github.com/bold24-AY/chemical-equipment-visualizer](https://github.com/bold24-AY/chemical-equipment-visualizer)

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [CSV Format](#csv-format)
- [Demo Credentials](#demo-credentials)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

---

## ✨ Features

### Core Functionality
- ✅ **CSV Upload & Validation** - Upload equipment data with automatic validation
- ✅ **Analytics Engine** - Pandas-powered statistical analysis
- ✅ **Dual Interface** - Web (React) and Desktop (PyQt5) applications
- ✅ **Interactive Charts** - Bar and Pie charts (Chart.js & Matplotlib)
- ✅ **PDF Reports** - Generate detailed reports with charts and tables
- ✅ **Data Persistence** - SQLite database stores last 5 uploads (per user)
- ✅ **Secure Authentication** - User Registration & Login (Session-based)
- ✅ **Data Isolation** - Multi-tenancy support: Users only see their own data
- ✅ **RESTful API** - Django REST Framework backend

### Visualizations
- Summary statistics cards (Total, Avg Flowrate, Pressure, Temperature)
- Bar chart showing average equipment parameters
- Pie chart displaying equipment type distribution
- Sortable data table with all equipment records

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Web App  │────┐
└─────────────────┘    │
                       ├──> REST API ──> Django + DRF ──> SQLite
┌─────────────────┐    │
│ PyQt5 Desktop   │────┘
└─────────────────┘
```

### Why This Architecture?

- **Single Backend** → No data inconsistency between clients
- **REST API** → Frontend-agnostic design
- **SQLite** → Lightweight, perfect for "last 5 uploads" requirement
- **Pandas** → Reliable CSV analytics and data processing
- **Chart.js & Matplotlib** → Production-grade visualizations

---

## 📦 Prerequisites

### System Requirements
- **Python** 3.10 or higher
- **Node.js** 16.x or higher
- **npm** 8.x or higher

### Python Packages (installed via requirements.txt)
- Django 4.2.7
- Django REST Framework 3.14.0
- django-cors-headers 4.3.1
- pandas 2.1.3
- reportlab 4.0.7
- PyQt5 5.15.10
- matplotlib 3.8.2
- requests 2.31.0

### Node Packages (installed via package.json)
- React 18.2.0
- axios 1.6.2
- chart.js 4.4.0
- react-chartjs-2 5.2.0

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bold24-AY/chemical-equipment-visualizer
cd chemical-equipment-visualizer
```

### 2. Backend Setup (Django)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (for Django admin)
python manage.py createsuperuser
# Username: trial12
# Password: Trial@1234 (or your choice)

# Start development server
python manage.py runserver
```

The backend will be available at `http://127.0.0.1:8000`

### 3. Web Frontend Setup (React)

```bash
cd web-frontend

# Install dependencies
npm install

# Start development server
npm start
```

The web app will open at `http://localhost:3000`

### 4. Desktop App Setup (PyQt5)

```bash
cd desktop-app

# Install dependencies (use backend's virtual environment or create new one)
pip install -r requirements.txt

# Run application
python main.py
```

---

## 💻 Usage

### Web Application

1. **Login**
   - Navigate to `http://localhost:3000`
   - Enter credentials (default: `trial12` / `Trial@1234`)
   - Click "Login"

2. **Upload CSV**
   - Click the "📤 Upload" tab
   - Choose a CSV file with required columns
   - Click "Upload & Analyze"

3. **View Dashboard**
   - Automatically redirected after upload
   - View summary statistics, charts, and data table
   - Click "📄 Download PDF Report" to generate report

4. **View History**
   - Click "📜 History" tab
   - See last 5 uploads
   - Download reports for previous datasets

### Desktop Application

1. **Login**
   - Launch `main.py`
   - Enter credentials in login dialog
   - Click "OK"

2. **Upload CSV**
   - Go to "📤 Upload" tab
   - Click "Browse..." and select CSV file
   - Click "Upload & Analyze"

3. **View Dashboard**
   - Automatically switches to "📊 Dashboard"
   - View summary cards, Matplotlib charts, and data table
   - Click "📄 Download Report" to save PDF

4. **Refresh Data**
   - Click "🔄 Refresh" button to reload latest data

---

## 🔌 API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/register/` | POST | Register new user |
| `/api/login/` | POST | Login with username/password |
| `/api/logout/` | POST | Logout current session |
| `/api/check-auth/` | GET | Check authentication status |

### Dataset Operations

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/upload/` | POST | Upload & analyze CSV | ✅ |
| `/api/summary/` | GET | Get latest dataset | ✅ |
| `/api/history/` | GET | Get last 5 uploads | ✅ |
| `/api/dataset/<id>/` | GET | Get specific dataset | ✅ |
| `/api/report/` | GET | Download latest report | ✅ |
| `/api/report/<id>/` | GET | Download specific report | ✅ |

### Example API Calls

```bash
# Login
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "trial12", "password": "Trial@1234"}'

# Upload CSV
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -H "Cookie: sessionid=<your-session-id>" \
  -F "file=@sample_equipment_data.csv"

# Get summary
curl -X GET http://127.0.0.1:8000/api/summary/ \
  -H "Cookie: sessionid=<your-session-id>"
```

---

## 📄 CSV Format

### Required Columns (Case-Sensitive!)

Your CSV **must** contain these exact column names:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
```

### Column Requirements

| Column | Type | Description |
|--------|------|-------------|
| `Equipment Name` | Text | Name/ID of equipment (space in column name!) |
| `Type` | Text | Equipment type (e.g., Pump, Reactor, Valve) |
| `Flowrate` | Numeric | Flow rate value (no units in data) |
| `Pressure` | Numeric | Pressure value (no units in data) |
| `Temperature` | Numeric | Temperature value (no units in data) |

### Sample CSV

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,120.5,5.2,65
Reactor B,Reactor,300.0,15.8,450
Heat Exchanger C,Heat Exchanger,220.7,8.1,180
Valve D,Valve,90.2,3.5,40
```

**Important Notes:**
- ✅ Column names are **case-sensitive** and **space-sensitive**
- ✅ Use `Equipment Name` (with space), not `Equipment_Name` or `EquipmentName`
- ✅ Numeric columns must contain only numbers (decimals allowed)
- ❌ No units in column names (e.g., `Flowrate (m3/hr)` is invalid)
- ❌ No trailing/leading spaces in column names

### Validation

The backend validates:
1. File is `.csv` format
2. All required columns are present
3. Numeric columns contain only numeric values

If validation fails, you'll receive a clear error message.

---

## 🔑 Demo Credentials

For testing purposes:

**Username:** `trial12`
**Password:** `Trial@1234`

Create additional users via Django admin panel at `http://127.0.0.1:8000/admin/`

---

## 📁 Project Structure

```
chemical-equipment-visualizer/
│
├── README.md                           # This file
├── .gitignore                          # Git ignore rules
├── sample_equipment_data.csv           # Sample CSV for testing
│
├── backend/                            # Django Backend
│   ├── manage.py                       # Django management
│   ├── requirements.txt                # Python dependencies
│   ├── backend/                        # Project config
│   │   ├── settings.py                 # Django settings
│   │   ├── urls.py                     # URL routing
│   │   ├── wsgi.py / asgi.py          # Server configs
│   │
│   └── equipment/                      # Equipment app
│       ├── models.py                   # Dataset model
│       ├── views.py                    # API endpoints
│       ├── serializers.py              # DRF serializers
│       ├── utils.py                    # CSV analytics
│       ├── urls.py                     # App URLs
│       └── admin.py                    # Django admin
│
├── web-frontend/                       # React Web App
│   ├── package.json                    # npm dependencies
│   ├── public/
│   │   └── index.html                  # HTML template
│   └── src/
│       ├── App.js                      # Main component
│       ├── App.css                     # Styling
│       ├── assets/                     # Images & Static assets
│       │   └── chemical_lab_header.jpeg # Header image
│       ├── components/                 # React components
│       │   ├── Login.js
│       │   ├── UploadForm.js
│       │   ├── SummaryCards.js
│       │   ├── DataTable.js
│       │   └── Charts.js
│       └── services/                   # API layer
│           ├── api.js
│           └── auth.js
│
└── desktop-app/                        # PyQt5 Desktop App
    ├── main.py                         # Entry point
    ├── api_client.py                   # REST API client
    ├── requirements.txt                # Python dependencies
    ├── assets/                         # Resources
    │   └── chemical_lab_header.jpeg    # Header image
    └── ui/                             # UI components
        ├── main_window.py              # Main window
        ├── upload_widget.py            # Upload UI
        ├── summary_widget.py           # Summary cards
        ├── chart_widget.py             # Matplotlib charts
        └── table_widget.py             # Data table
```

---

## 🛠️ Technologies Used

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API building
- **Pandas** - Data analysis
- **ReportLab** - PDF generation
- **SQLite** - Database
- **CORS Headers** - Cross-origin support

### Web Frontend
- **React 18** - UI library
- **Axios** - HTTP client
- **Chart.js** - Interactive charts
- **React Chart.js 2** - React wrapper
- **CSS3** - Styling

### Desktop App
- **PyQt5** - Desktop GUI framework
- **Matplotlib** - Scientific plotting
- **Requests** - HTTP client

---

## 🎯 Key Features Explained

### 1. Last 5 Uploads Rule

The system automatically maintains only the 5 most recent uploads:

```python
# In views.py after upload
Dataset.objects.order_by('-uploaded_at')[5:].delete()
```

### 2. CSV Analytics

Pandas calculates:
- Total equipment count
- Average flowrate, pressure, temperature
- Min/max values for each parameter
- Equipment type distribution (counts per type)

### 3. PDF Reports

Reports include:
- Dataset metadata (filename, timestamps)
- Summary statistics table
- Equipment type distribution table
- Bar chart (average parameters)
- Pie chart (type distribution)

### 4. Session Authentication

Both web and desktop apps use Django session authentication:
- Login creates a session
- Session cookie authenticates subsequent requests
- Logout invalidates session

---

## 🐛 Troubleshooting

### Backend Issues

**Issue:** `ModuleNotFoundError: No module named 'rest_framework'`
```bash
# Solution: Install dependencies
pip install -r backend/requirements.txt
```

**Issue:** `django.db.utils.OperationalError: no such table`
```bash
# Solution: Run migrations
python manage.py makemigrations
python manage.py migrate
```

### Frontend Issues

**Issue:** `Cannot find module 'axios'`
```bash
# Solution: Install dependencies
cd web-frontend
npm install
```

**Issue:** `Proxy error: Could not proxy request`
```bash
# Solution: Ensure Django backend is running on port 8000
cd backend
python manage.py runserver
```

### Desktop App Issues

**Issue:** `ModuleNotFoundError: No module named 'PyQt5'`
```bash
# Solution: Install dependencies
pip install -r desktop-app/requirements.txt
```

**Issue:** `Connection Error: Could not connect to server`
```bash
# Solution: Ensure Django backend is running
cd backend
python manage.py runserver
```

---

## 📝 Quick Start Guide

```bash
# Terminal 1: Start Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # Create trial12/Trial@1234
python manage.py runserver

# Terminal 2: Start Web Frontend
cd web-frontend
npm install
npm start

# Terminal 3: Start Desktop App
cd desktop-app
pip install -r requirements.txt
python main.py
```

---

**Happy Analyzing! 📊🧪**
