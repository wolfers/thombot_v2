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
RUN python3.6 -m pip install -r requirements.txt

COPY ./src /thombot

WORKDIR /thombot

CMD ["python3.6", "bot.py"]
