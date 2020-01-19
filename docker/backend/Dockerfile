FROM python:3.8

COPY backend /odas

WORKDIR odas

RUN pip3 install --requirement requirements.txt


ENV FLASK_APP=app.py
ENV PORT=1000

RUN mkdir ssl

# RUN rm -r ssl
# WORKDIR odas/ssl
COPY ./ssl/localhost.pem ssl/server.pem
COPY ./ssl/localhost.key ssl/server.key

# WORKDIR odas

EXPOSE ${PORT}

ENTRYPOINT ["python3","-u", "odas/main.py"]
