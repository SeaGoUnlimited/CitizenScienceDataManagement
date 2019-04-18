FROM python:3.6-stretch

#ENV HOME /Users/seangoral/github/SeatizenScience


COPY website.py /
COPY json_data.py /
COPY database.py /
COPY update_whalealert.py /
COPY update_spotter.py /
COPY sqlite_to_csv.py /
#COPY spotter_pro_obis.csv /
#COPY whale_alert_obis.csv /
COPY main.sh /
COPY credentials.config /
COPY requirements.txt /tmp/
COPY spotter.sqlite /


RUN pip install -r /tmp/requirements.txt
RUN apt-get update
RUN apt-get install -y python3-dev gcc libsqlite3-mod-spatialite

CMD ["bash", "main.sh"]

