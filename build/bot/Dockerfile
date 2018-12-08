FROM python:3.6-stretch

ADD ./ /

RUN apt update && apt install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    openssl \
    ffmpeg \
    git
RUN python3.6 -m pip install pip --upgrade
RUN git clone https://github.com/Rapptz/discord.py.git
RUN cd discord.py && git checkout rewrite && python3.6 -m pip install -U .[voice]
RUN python3.6 -m pip install pony
RUN python3.6 -m pip install Pillow
RUN python3.6 -m pip install psycopg2
RUN python3.6 -m pip install requests
RUN python3.6 -m pip install youtube_dl

COPY ./src /thombot

WORKDIR /thombot

CMD ["python3.6", "bot.py"]
