FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

<<<<<<< Updated upstream
RUN pip install --no-cache-dir -r requirements.txt
=======
RUN pip install --no-chache-dir -r requirements.txt
>>>>>>> Stashed changes

COPY . .

EXPOSE 5000

WORKDIR /app/library-management

CMD ["python","run.py"]