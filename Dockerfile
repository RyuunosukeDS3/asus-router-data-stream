FROM python:3.11-slim

WORKDIR /app
RUN mkdir /config
COPY . .

RUN pip install -U pip
RUN pip3 install -r requirements.txt

CMD [ "/bin/bash", "-c", "python3 main.py" ]