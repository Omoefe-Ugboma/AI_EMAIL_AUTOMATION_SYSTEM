# AI Email Assistant API

An AI-powered backend system that generates professional email responses using LLMs.

## Features
- Generate email replies from input
- Modular architecture
- FastAPI-based REST API
- Environment-based configuration

## Features

- Email classification (rule-based + AI hybrid)
- Context-aware response generation
- Category-based tone adaptation
- Modular backend architecture (FastAPI)

## Features

- Authentication ✔
- User identity ✔
- Data persistence ✔
- Data isolation ✔

- REAL multi-user backend system

## Example Categories

- Complaint → Apologetic response
- Request → Helpful response
- Inquiry → Informative response
- Feedback → Appreciative response

## 🚀Features

- AI-generated email replies (OpenAI)
- Email classification system
- JWT authentication
- Multi-user system
- PostgreSQL database
- REST API (FastAPI)

## 🌍 Live Demo

https://your-api-url

## 🧠Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- OpenAI API
- JWT Authentication

## 📌Endpoints

- POST /auth/register
- POST /auth/login
- GET /auth/me
- POST /generate-reply
- GET /my-emails

## Features (Advanced)

- Email storage with PostgreSQL
- API endpoint to retrieve email history
- Full AI pipeline (classification → response → persistence)

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload 