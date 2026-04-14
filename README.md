# CareerOS PDF Service

Python/ReportLab microservice that generates the CareerOS Pro Report PDF.

## Endpoints

- `GET /health` — Health check
- `POST /generate-report` — Generate PDF from JSON data, returns PDF bytes

## Deploy on Render

1. Connect this repo to Render as a Web Service
2. Runtime: Python 3
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn server:app --bind 0.0.0.0:$PORT`
5. Plan: Free

## Keep-Alive

Set up a cron job at cron-job.org to hit `/health` every 14 minutes to prevent cold starts.
