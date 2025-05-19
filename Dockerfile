FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY entrypoint.sh /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations (optional — or run manually)
RUN python manage.py migrate --noinput

EXPOSE 5858
CMD ["daphne", "SubtitutesProject.asgi:application", "-p 5858", "-b 0.0.0.0"]
