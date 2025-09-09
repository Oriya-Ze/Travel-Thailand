from flask import Flask
import os
import redis

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
cache = redis.Redis(host=redis_host, port=redis_port, db=0)

@app.route("/")
def index():
    count = cache.incr("hits")
    return f"Hello from Flask behind NGINX! Hits: {count}\n"

@app.route("/health")
def health():
    try:
        cache.ping()
        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "redis_unavailable", "error": str(e)}, 503

# Gunicorn מחפש אובייקט בשם app בקובץ זה
