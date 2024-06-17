FROM python:alpine3.11
RUN pip install pytest
COPY pspy /app/pspy
COPY test_pspy.py /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "/usr/local/bin/pytest", "-v" ]