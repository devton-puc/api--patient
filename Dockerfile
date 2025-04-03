FROM python:3.11-slim AS builder

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install setuptools wheel

RUN python setup.py bdist_wheel

FROM python:3.11-slim AS final

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install gunicorn

COPY --from=builder /app/dist/*.whl /dist/

RUN pip install /dist/*.whl

WORKDIR /app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
