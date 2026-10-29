# Tessera V1 slot-2 policy signer (service/signer-gcp). Build context: the directory deploy.sh stages, holding
# signer-gcp/ (this package) and verifier/ (the service verifier, used as the frame codec). Python 3.14 because the
# verifier and the profile pin Unicode 16.0.0 tables, which 3.14 carries; the build fails otherwise.
FROM python:3.14-slim
RUN python -c "import unicodedata,sys; sys.exit(unicodedata.unidata_version != '16.0.0')"
WORKDIR /app
COPY signer-gcp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY verifier/pyproject.toml /src/verifier/pyproject.toml
COPY verifier/tessera_verify /src/verifier/tessera_verify
COPY signer-gcp/pyproject.toml /src/signer-gcp/pyproject.toml
COPY signer-gcp/tessera_signer /src/signer-gcp/tessera_signer
RUN pip install --no-cache-dir --no-deps /src/verifier /src/signer-gcp \
 && python -c "import tessera_signer.main, tessera_signer.gcp"
USER 65534
ENTRYPOINT ["python", "-u", "-m", "tessera_signer.main"]
