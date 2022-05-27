FROM python:3.8.12

WORKDIR /app

# RUN pip freeze > requirements.txt
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["main.py"]

# CMD ["streamlit", "run", "app.py"]
# CMD streamlit run app.py