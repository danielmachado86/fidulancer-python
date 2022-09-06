FROM tiangolo/uwsgi-nginx-flask:latest
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./