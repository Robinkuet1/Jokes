FROM python:3.9
COPY . .
RUN pip install mysql-connector-python Flask flask-cors requests tqdm
EXPOSE 5678
CMD ["python", "main.py"]
