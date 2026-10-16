# Slot-2 policy signer (instrument code, prototype/policy-signer/DESIGN.md). Python 3.14: the vendored P8
# decoder pins Unicode 16.0.0 tables, which Python 3.14 carries.
FROM python:3.14-slim
RUN python -c "import unicodedata,sys; sys.exit(unicodedata.unidata_version != '16.0.0')"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY p8_codec.py main.py ./
RUN python -c "import p8_codec"
USER 65534
ENTRYPOINT ["python", "-u", "/app/main.py"]
