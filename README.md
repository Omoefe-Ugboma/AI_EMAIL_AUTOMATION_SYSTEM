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

## Example Categories

- Complaint → Apologetic response
- Request → Helpful response
- Inquiry → Informative response
- Feedback → Appreciative response

## Tech Stack
- Python
- FastAPI
- OpenAI API

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload