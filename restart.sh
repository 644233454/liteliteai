source venv/bin/activate
export OPENAI_API_KEY=sk-xxxx
export TEL_TOKEN=xxxx
pkill -9 python
pkill -9 gunicorn
gunicorn app:app -b 0.0.0.0:5000 --daemon --log-file=logs/app.log --log-level=INFO --timeout 120 -k eventlet -w 1

nohup python3.9 service/telegrambot.py > ./logs/tbot.log 2>&1 &

