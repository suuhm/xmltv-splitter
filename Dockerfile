# Basis-Image
FROM python:3.11-slim

# Arbeitsverzeichnis
WORKDIR /app

# Benötigte Pakete
RUN pip install lxml

# Skript kopieren
COPY xmltv-splitter.py .

# Entry-Point
ENTRYPOINT ["python3", "xmltv-splitter.py"]
