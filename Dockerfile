FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/
CMD ["daphne" ,"SubtitutesProject.asgi:application","-p" ,"5858","-b","0.0.0.0"]