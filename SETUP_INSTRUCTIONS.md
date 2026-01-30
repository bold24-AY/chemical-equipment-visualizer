# Quick Setup Instructions

## ⚡ Fastest Way to Get Started

### Step 1: Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
# Create: username=trial12, password=Trial@1234
python manage.py runserver
```
✅ Backend running at `http://127.0.0.1:8000`

### Step 2: Web Frontend (React)
```bash
# New terminal
cd web-frontend
npm install
npm start
```
✅ Web app opens at `http://localhost:3000`

### Step 3: Desktop App (PyQt5)
```bash
# New terminal
cd desktop-app
pip install -r requirements.txt
python main.py
```
✅ Desktop app launches

## 🔐 Login Credentials
- Username: `trial12`
- Password: `Trial@1234`

## 📄 Test CSV
Use the included `sample_equipment_data.csv` file to test uploads.

## ⚠️ Common Issues

**Backend won't start:**
- Check Python version: `python --version` (need 3.10+)
- Ensure virtual environment is activated

**Frontend won't start:**
- Check Node version: `node --version` (need 16+)
- Delete `node_modules` and run `npm install` again

**Desktop app won't connect:**
- Ensure backend is running on port 8000
- Check firewall settings

## 📚 Full Documentation
See `README.md` for complete documentation.
