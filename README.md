# Thought Agent

Minimal MVP for thought agent project.

## Run Instructions

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database and environment variables:
   ```bash
   cp .env.example .env
   # Edit .env to set your DATABASE_URL
   ```
4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
