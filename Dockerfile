FROM python:3.9

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "climate_comfort:app"]
