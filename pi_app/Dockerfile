#FROM python:3.6.4-onbuild
FROM python:3.6.5-slim

RUN apt-get update && apt-get install -y gcc \
    libgmp-dev libmpfr-dev libmpfr-doc libmpfr4 libmpfr4-dbg \
    mpc libmpc-dev

ADD ./requirements.txt /pi_app/
#COPY requirements.txt /pi_app
WORKDIR /pi_app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["pi_flaskapp.py"]