FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN apt-get update

# Necesario para ejecutar OpenCV
RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["python", "PeopleCounterLib/main.py"]