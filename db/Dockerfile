FROM postgres:latest
ENV POSTGRES_PASSWORD=1111
ENV POSTGRES_USER=check
ENV POSTGRES_DB=quest_db
COPY quest.sql /docker-entrypoint-initdb.d/quest.sql