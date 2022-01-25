From python:3
WORKDIR /usr/local/lib/python3.10/site-packages/booksapi
COPY code/booksapi-2022.1.23.1.tar.gz ./
RUN apt-get update && apt-get install -y vim
RUN pip install --no-cache-dir booksapi-2022.1.23.1.tar.gz
ENTRYPOINT ["python", "app.py"]