FROM gauseng/superset:v0.15.0

# Install
ENV SUPERSET_VERSION 0.15.1

RUN adduser --disabled-password --gecos '' --no-create-home superset

COPY . /app/
RUN pip3 uninstall -y superset && pip install superset-${SUPERSET_VERSION}-py3-none-any.whl

RUN mkdir -p /app/.superset && \
    touch /app/.superset/superset.db && \
    chown -R superset:superset /app

# Default config
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH=$PATH:/app/.bin \
    PYTHONPATH=/app/superset_config.py:$PYTHONPATH \
    SQLALCHEMY_DATABASE_URI=sqlite:////app/.superset/superset.db

USER superset

# Deploy
EXPOSE 8088
HEALTHCHECK CMD ["curl", "-f", "http://localhost:8088/health"]
#ENTRYPOINT ["superset"]
#CMD ["runserver"]
