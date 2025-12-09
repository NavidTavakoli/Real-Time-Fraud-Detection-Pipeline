FROM apache/spark:4.0.1

USER root

# Install Redis lib
RUN pip install --no-cache-dir redis==7.0.1

# Setup Ivy cache permissions
RUN mkdir -p /home/spark/ivy &&     chown -R spark:spark /home/spark/ivy

# Copy script
COPY redisSink.py /opt/spark/work-dir/redisSink.py

USER spark
