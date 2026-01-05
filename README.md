# 📝 Notepad System: Setup Guide

Follow this guide **in order** to set up and run the application. This is a foolproof step-by-step process.

---

## 🛠️ Phase 1: Global Installations
Before doing anything, ensure you have these two things installed on your computer:
1. **Python (3.8+)**: [Download here](https://www.python.org/downloads/)
2. **Node.js (18+)**: [Download here](https://nodejs.org/)

---

## � Phase 2: Get Your AI API Key
The system uses AI for task summaries. **You must do this first.**
1. Go to [Hugging Face Tokens](https://huggingface.co/settings/tokens).
2. Create a **New Token** (Type: Read).
3. Copy the token. You will need it for the next phase.

---

## ⚙️ Phase 3: Running the Backend
*Run these commands one by one in your terminal.*

1. **Enter the backend folder**:
   ```bash
   cd backend
   ```
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```
3. **Activate the environment**:
   - **Windows**: `.\venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`
4. **Install all Python libraries**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Set up your Configuration (API Key)**:
   Create a file named `.env` inside the `backend` folder and paste this:
   ```env
   SECRET_KEY=my_secure_key
   DATABASE_URL=sqlite:///mydatabase.db
   AI_API_KEY=PASTE_YOUR_COPIED_TOKEN_HERE
   ```
6. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```
   *Keep this window open!*

---

## 🎨 Phase 4: Running the Frontend
*Open a **new, second terminal window**.*

1. **Enter the frontend folder**:
   ```bash
   cd frontend
   ```
2. **Install all UI libraries**:
   ```bash
   npm install
   ```
3. **Start the application**:
   ```bash
   npm run dev
   ```

---

## 🚀 Phase 5: View the Application
Once both terminals are running:
1. Open your browser.
2. Go to: **[http://localhost:5173](http://localhost:5173)**

---

## ✅ Checklist for Evaluation
- [ ] Python and Node.js are installed.
- [ ] Backend terminal is running `uvicorn`.
- [ ] Frontend terminal is running `npm run dev`.
- [ ] `.env` file exists in the `backend` folder with your API key.

## Project Structure

```text
Notepad/
├── backend/            # FastAPI application logic
│   ├── main.py         # API entry point
│   ├── models.py       # SQL Alchemy database models
│   └── ai_assistant.py # AI/LLM integration
├── frontend/           # Vite + React UI
│   ├── src/            # Components and hooks
│   └── index.html      # SPA entry point
└── README.md           # This guide
```
