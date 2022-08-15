FROM python:3.6

COPY build/nlm_scrubber /opt/nlm_scrubber
RUN chmod +x /opt/nlm_scrubber

COPY pyscrubber.py /opt/pyscrubber.py
#RUN chmod +x /opt/pyscrubber.py # TODO fails on raspbian linux/amd64 compilation

COPY docker/entrypoint.sh /opt/entrypoint.sh
#RUN chmod +x /opt/entrypoint.sh # TODO fails on raspbian linux/amd64 compilation

COPY docker/addons/sql_dates.nci2.txt /opt/sql_dates.nci2.txt

COPY docker/addons/convert_to_ascii.py /opt/convert_to_ascii.py
#RUN chmod +x /opt/convert_to_ascii.py

ENTRYPOINT ["/opt/entrypoint.sh"]
