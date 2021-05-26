# Python 3.9.5 on Debian Buster
FROM python@sha256:f265c5096aa52bdd478d2a5ed097727f51721fda20686523ab1b3038cc7d6417

ARG USER_UID=1000

RUN adduser --shell /bin/sh --uid "${USER_UID}" default
USER default

ENV PYTHONPATH $PYTHONPATH:/opt
ENV PATH $PATH:/home/default/.local/bin

WORKDIR /opt

ADD ./requirements.txt ./requirements.txt
RUN pip install --user -r requirements.txt

ADD --chown=default:default . /opt

WORKDIR /opt/code

CMD ["python", "prisonersDilemma.py"]

