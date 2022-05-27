FROM python:3.8.12

WORKDIR /app

# RUN pip freeze > requirements.txt
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

# CMD ["uvicorn", "main:app", "--reload"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# ENTRYPOINT [ "executable" ]