# 📝 BEDDEL Document Processor

BEDDEL is a smart document processor that lets users:
- Upload Word documents (`.docx`)
- Describe what they want changed (in plain English)
- Automatically applies edits using AI (Google Gemini) and downloads updated documents.
---

## 🖥️ Setup Instructions

### 1️) Prerequisites

Ensure the following software is installed on your machine:

- **Python 3.10+**  
  👉 Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)

- **Node.js + npm** (for frontend)  
  👉 Download: [https://nodejs.org/](https://nodejs.org/)

---

### 2) Clone or Extract Project

If you received this project as a ZIP file, unzip it somewhere convenient (e.g., `~/Documents/BEDDEL`).

If cloning from GitHub:


git clone https://github.com/Majid-Beddel/Beddel.git
cd ~/Documents/BEDDEL

---

### 3) Backend Setup

pip install -r requirements.txt
python3 -m uvicorn main:app --reload --port 8000

### 4) Frontend Setup 

 cd ~/Documents/BEDDEL/beddel-ui
 npm install
 npm run dev

### 5) Open in Browser

 Visit: http://localhost:3000


