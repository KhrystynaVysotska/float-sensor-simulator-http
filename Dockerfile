FROM python:3.8-slim-buster

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

RUN mkdir -p /app/keys && touch /app/keys/rsa_private.pem

CMD ["python", "./simulator.py"]