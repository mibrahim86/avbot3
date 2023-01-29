FROM python:3
FROM gorialis/discord.py

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot
COPY . .
RUN pip install -r requirements.txt
RUN pip install spotipy

CMD [ "python3", "bot.py" ]