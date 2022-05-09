FROM postgres
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB quest
COPY quest.sql /docker-entrypoint-initdb.d/
