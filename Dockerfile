FROM python:3.8

ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=app/app.py
ENV BLOBNAME=$blobname

RUN apt update && apt install -y tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY . /code

WORKDIR /code

CMD ["python","ocr_image_process.py"]
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]