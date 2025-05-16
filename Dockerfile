ccFROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY entrypoint.sh /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/
EXPOSE 5858
CMD ["sh","entrypoint.sh"]
