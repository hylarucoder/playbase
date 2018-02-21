FROM postgres:10
MAINTAINER twocucao <twocucao@gmail.com>

ENV POSTGIS_MAJOR 2.4
ENV POSTGIS_VERSION 2.4.2+dfsg-1.pgdg90+1

COPY ./compose/postgres/sources.list /etc/apt/
RUN apt-get update \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts=$POSTGIS_VERSION \
           postgis=$POSTGIS_VERSION \
      && rm -rf /var/lib/apt/lists/*


# add scripts
COPY ./compose/postgres/backup.sh /usr/local/bin/backup
COPY ./compose/postgres/restore.sh /usr/local/bin/restore
COPY ./compose/postgres/list-backups.sh /usr/local/bin/list-backups

# make them executable
RUN chmod +x /usr/local/bin/restore
RUN chmod +x /usr/local/bin/list-backups
RUN chmod +x /usr/local/bin/backup

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./compose/postgres/initdb-postgis.sh /docker-entrypoint-initdb.d/postgis.sh
COPY ./compose/postgres/update-postgis.sh /usr/local/bin

# initdb
EXPOSE 5432
