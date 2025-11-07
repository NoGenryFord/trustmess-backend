# Use Python 3.12 slim image (3.14 not available yet, use 3.12)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy application code first
COPY . .

# Install dependencies directly with pip
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    pydantic \
    pyjwt \
    "pwdlib[argon2]" \
    websockets \
    aiosqlite \
    sqlalchemy

# Expose port
EXPOSE 8000

# Initialize database and start server
CMD python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000
