FROM python:3.10.8

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /app/

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt


COPY ./src ./src



CMD [ "python3", "./src/API/manage.py", "runserver", "0.0.0.0:8000" ]