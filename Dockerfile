FROM python:3.9-slim-buster

RUN apt update -y && \
    apt install -y python3-pip

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install --pre gql[all]
RUN pip install -r requirements.txt

COPY . /app

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
# ENTRYPOINT [ "python" ]

# CMD [ "app.py" ]
