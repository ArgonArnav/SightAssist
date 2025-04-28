FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy code
COPY . .

# expose port
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "web_app:app", "-b", "0.0.0.0:5000"]
