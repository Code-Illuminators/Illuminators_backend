FROM python:3.13-slim

WORKDIR /backend

COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libmariadb-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${BACKEND_PORT}

CMD ["python", "manage.py", "runserver", "0.0.0.0:${BACKEND_PORT}"]
