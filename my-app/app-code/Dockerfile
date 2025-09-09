FROM python:3.10-slim

WORKDIR /app

# התקנות בסיסיות
RUN pip install --no-cache-dir --upgrade pip

# תלות לפני קוד (שכבת cache טובה)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# קוד האפליקציה
COPY app.py .

EXPOSE 5000

# שרת פרודקשן קליל
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
