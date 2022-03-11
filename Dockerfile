FROM python:3.10-alpine

WORKDIR /DiscordAvatarsBot
COPY . .

RUN apk add git
RUN apk add --no-cache python3 py3-pip
RUN pip install -r requirements.txt

ENTRYPOINT python bot.py ${KIYOHIME_TOKEN} ${KIYOHIME_GUILD}
