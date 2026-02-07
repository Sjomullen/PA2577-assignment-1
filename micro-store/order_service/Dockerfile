FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# ^ This line copies the new 'templates' folder automatically.
EXPOSE 5001
CMD ["python", "app.py"]