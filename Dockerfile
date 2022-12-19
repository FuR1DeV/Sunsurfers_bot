FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /sunsurfersbot

RUN pip install -U pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
RUN chmod 755 .
COPY . .
