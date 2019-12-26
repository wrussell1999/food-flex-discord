FROM python:3.7-buster

WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3", "-m", "foodflex" ]