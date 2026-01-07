# ⚡ Quick Start Guide

Get CreditWorkflowAgent running in 5 minutes!

## Prerequisites

- Docker Desktop installed
- OpenAI API key

## Setup Steps

### 1. Configure OpenAI API Key

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

### 2. Start the System

From project root:
```bash
docker-compose up --build
```

Wait for both services to start (takes 2-3 minutes first time).

### 3. Access the Demo

Open browser: **http://localhost:3000**

## Run Your First Demo

1. Click **"Unblock - Good Customer"** button
2. Wait 10-15 seconds for workflow to complete
3. View the 5-step timeline showing:
   - Credit Block Request
   - AI Analysis & Recommendation
   - Human Approval
   - SAP Update
   - Notification

## What You'll See

- **Real-time workflow timeline** with 5 steps
- **AI analysis panel** showing DSO, utilisation, risk signals
- **Confidence scores** for AI recommendations
- **Human approval decision** (auto-approved in demo)
- **SAP update confirmation** with reference ID
- **Demo talk track** for presentation

## API Documentation

Backend API docs: **http://localhost:8000/docs**

## Stopping the System

```bash
docker-compose down
```

## Troubleshooting

**Backend won't start?**
- Check your OpenAI API key in `backend/.env`
- Run: `docker-compose logs backend`

**Frontend shows error?**
- Wait 30 seconds for backend to fully start
- Refresh the page

## Next Steps

- Read full [README.md](README.md) for architecture details
- Explore API endpoints at `/docs`
- Try all 3 demo scenarios
- Customize demo data in `backend/app/tools/credit_tools.py`

---

**Need help?** Check the main README.md for detailed documentation.
