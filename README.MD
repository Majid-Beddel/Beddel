# 📝 BEDDEL Document Processor

BEDDEL is a smart AI-powered document processor that lets users:

- Upload Word documents (`.docx`)
- Describe desired changes in plain English (e.g., “Make text red”, “Replace all instances of OldCompany”)
- Automatically applies edits using Google Gemini AI
- Downloads the updated `.docx` or `.zip` file

---

## 🛠️ Project Setup (Using Docker)

This setup is beginner-friendly and does **not require installing Python or Node.js** manually. Everything runs in Docker containers.

---

### 1. Prerequisites

Install the following tools on your system:

- [**Git**](https://git-scm.com/downloads) – to clone the project
- [**Docker Desktop**](https://www.docker.com/products/docker-desktop) – to run the backend and frontend

---

### 2. Clone the Project


git clone https://github.com/Majid-Beddel/Beddel.git
cd Beddel


### 3. Run app with Docker

Make sure that the Docker Desktop downloaded in step 1 is running, once confirming it is, run the following: 

docker compose up --build

### 4. Access on browser

Go to http://localhost:3000/ 
