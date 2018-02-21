FROM postgres:10
MAINTAINER twocucao <twocucao@gmail.com>

# add scripts
COPY ./compose/postgres/backup.sh /usr/local/bin/backup
COPY ./compose/postgres/restore.sh /usr/local/bin/restore
COPY ./compose/postgres/list-backups.sh /usr/local/bin/list-backups

# make them executable
RUN chmod +x /usr/local/bin/restore
RUN chmod +x /usr/local/bin/list-backups
RUN chmod +x /usr/local/bin/backup

EXPOSE 5432
