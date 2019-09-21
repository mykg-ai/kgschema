FROM godbaby/chromit-api:base
ADD . /code/
WORKDIR /code
#RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]