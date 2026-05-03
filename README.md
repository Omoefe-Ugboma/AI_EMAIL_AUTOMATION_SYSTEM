# 🤖 AI Email Automation System

An AI-powered backend system that automatically reads incoming emails, classifies them, generates intelligent replies, and applies workflow automation using the Gmail API.

---

## 🚀 Overview

This system simulates a real-world email automation platform used in universities or customer support environments. It integrates Artificial Intelligence with backend engineering to process emails intelligently and efficiently.

---

## ✨ Core Features

### 📩 Email Processing
- Reads real emails from Gmail
- Sends automated AI-generated replies
- Marks emails as read after processing

---

### 🧠 AI Classification (Hybrid System)
- Rule-based + AI fallback classification
- Categories include:
  - Finance
  - Admissions
  - Academic
  - Complaint
  - Inquiry
  - General

---

### ✉️ Smart Reply Generation
- Context-aware responses using OpenAI
- Personalized replies (recipient name)
- Department-based responses
- Tone adaptation (formal, empathetic, etc.)
- No placeholders (production-ready responses)

---

### ⚙️ Workflow Automation
- Automatically labels emails:
  - `Processed`
  - Category labels (Finance, Admissions, etc.)
- Prevents duplicate processing using `message_id`
- Skips self-generated emails
- Prevents infinite reply loops

---

### 🔐 Authentication & Security
- JWT-based authentication
- Multi-user support
- Secure API endpoints
- User-specific data isolation

---

### 💾 Database & Persistence
- PostgreSQL database
- Stores:
  - Email content
  - Category
  - Generated reply
  - Response time
  - User association
- Prevents duplicate email processing

## 🏗️ System Architecture

- Gmail Inbox
- ↓
- Fetch Emails (Gmail API)
- ↓
- Filter (self, duplicates, replies)
- ↓
- AI Classification
- ↓
- AI Reply Generation
- ↓
- Send Reply (Gmail API)
- ↓
- Mark as Read
- ↓
- Apply Labels (Processed + Category)
- ↓
- Save to Database
- ↓
- Expose via API

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **AI:** OpenAI API
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Email Integration:** Gmail API

## 📂 Project Structure

- app/
- │── api/ # API routes
- │── core/ # Config, security, database
- │── models/ # Database models
- │── schemas/ # Request/response schemas
- │── services/ # AI, Gmail, DB logic
- │── utils/ # Helper functions

## 🔑 API Endpoints

- | Endpoint | Description |
- |--------|------------|
- | POST `/auth/register` | Register new user |
- | POST `/auth/login` | Login and get token |
- | GET `/auth/me` | Get current user |
- | POST `/generate-reply` | Generate AI reply (manual input) |
- | GET `/process-inbox` | Simulated email processing |
- | GET `/gmail-process` | Process real Gmail inbox |
- | GET `/my-emails` | Retrieve processed emails |

## ⚙️ Installation & Setup

### 1. Clone Repository

- ```bash
- git clone https://github.com/YOUR_USERNAME/ai-email-assistant.git
- cd ai-email-assistant

- python -m venv venv
- venv\Scripts\activate   # Windows

- Install Dependencies
- pip install -r requirements.txt

### 2. Configure Environment Variables

- Create a .env file:

- OPENAI_API_KEY=your_openai_api_key
- DATABASE_URL=postgresql://user:password@localhost:5432/db_name
- SECRET_KEY=your_secret_key

## Run Application

- python -m uvicorn app.main:app --reload

## 🧪 Testing the System

- Option 1: Real Gmail Processing
- Send an email to your Gmail
- Call:
- GET /gmail-process
- Verify:
- Reply sent ✔
- Email labeled ✔
- Saved in DB ✔

- Option 2: Simulated Emails
- GET /process-inbox
- 🧠 Production-Level Features
- No duplicate replies
- No infinite loops
- Message tracking with message_id
- Error handling for robustness
- Clean modular architecture
- Scalable backend design

## 🎓 Academic Value

- This project demonstrates:

- AI + Backend integration
- Workflow automation (RPA concepts)
- Intelligent decision systems
- Real-world API integration (Gmail)
- Hybrid classification (rule-based + AI)

## 💼 Real-World Use Cases

- University email automation system
- Customer support automation
- Enterprise workflow automation
- AI-powered helpdesk systems

## 🔮 Future Improvements

- Web dashboard (React)
- Email sentiment analysis
- Multi-language support
- Cloud deployment (AWS / Render)
- Admin analytics panel

## 👨‍💻 Author

- Ugboma Omoefe Ugboma
- MSc Artificial Intelligence – University of Mauritius
- AI Engineer

## ⭐ Acknowledgements

- OpenAI API
- Gmail API
- FastAPI
- SQLAlchemy