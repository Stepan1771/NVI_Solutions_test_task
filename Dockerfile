FROM python:3.12.10-slim

RUN apt-get update && apt-get install -y git curl build-essential && rm -rf /var/lib/apt/lists/*

RUN python -m ensurepip --upgrade
RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app .

RUN chmod +x prestart.sh
RUN chmod +x main.py

ENTRYPOINT ["./prestart.sh"]

CMD ["uvicorn", "main:shop_app", "--host", "0.0.0.0", "--port", "8000"]