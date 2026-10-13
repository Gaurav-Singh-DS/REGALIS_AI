FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

COPY requirements.txt ./requirements.txt

RUN python -m pip install --no-cache-dir --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Copy shared data only if it exists inside the backend build context.
# If your data directory is at the repository root, see the note below.

EXPOSE 8080

CMD ["python", "-m", "app.main"]