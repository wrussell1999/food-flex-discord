FROM python:3.7-buster
VOLUME [ "/data" ]
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
ENTRYPOINT [ "python3", "-m", "app" ]