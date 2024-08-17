FROM python:3.11.9

WORKDIR /usr/src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip
COPY ../requirements.txt /usr/src/requirements.txt
RUN pip install -r requirements.txt

COPY ./app/dbt_anime /usr/src/dbt_anime  

COPY ./app/trivia /usr/src/trivia
RUN cd /usr/src/dbt_anime && dbt clean && dbt deps
# RUN cd .. && chmod +x /usr/src/entry.sh
CMD ["/usr/src/entry.sh"]
# CMD ["tail", "-f", "/dev/null"]

