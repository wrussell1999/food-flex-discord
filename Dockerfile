FROM python:3.7-buster
VOLUME [ "/data" ]
WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3", "-m", "foodflex" ]