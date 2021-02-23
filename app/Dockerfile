FROM python:latest
ENV LOAD_OPTION=$LOAD_OPTION
ENV PYTHONUNBUFFERED=0
WORKDIR /usr/src/app
EXPOSE 5000
copy requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
copy . .
CMD ["python","app.py","--host","0.0.0.0"]
