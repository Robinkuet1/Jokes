FROM python:3.9
COPY . .
RUN pip install mysql-connector-python Flask
EXPOSE 5678
CMD ["flask", "run"]
