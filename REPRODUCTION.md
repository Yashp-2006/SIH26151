# Reproduction Guide

A new engineer can reproduce the entire project state without external dependencies (other than Python 3.13).

## Prerequisites
- Windows / Linux / macOS
- Python 3.13.x

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
pip install -r requirements-research-lock.txt
```

## Running the Evaluation (Proves the Math)
```bash
python -m pramana.evaluate
```
*Expected Output:* A table demonstrating the False Merge Rate dropping from 29.8% to 1.5%.

## Running the API Gateway
```bash
uvicorn backend.app.main:app --reload
```
*Expected Output:* Uvicorn starts on port 8000. Navigate to `http://127.0.0.1:8000/docs` to see the OpenAPI schema, and hit `/calibration/tippett` for live metrics.
