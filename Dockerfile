FROM python:3.8

COPY . /odas

WORKDIR odas

RUN pip3 install --requirement requirements.txt


ENV FLASK_APP=app.py
ENV PORT=1000

EXPOSE ${PORT}

ENTRYPOINT ["python3","-u", "odas/app.py"]
