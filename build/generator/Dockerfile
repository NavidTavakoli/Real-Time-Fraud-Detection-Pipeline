FROM python:3.9-slim

WORKDIR /app

# Install DB drivers
RUN pip install --no-cache-dir psycopg2-binary pymysql

# Copy script
COPY generateItems.py .

# Run unbuffered for real-time logging
CMD ["python", "-u", "generateItems.py"]
