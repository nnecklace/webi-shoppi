FROM postgres:12.3
ENV POSTGRES_DB webi_shoppi
ENV POSTGRES_HOST_AUTH_METHOD trust
ADD pre_install.sql /docker-entrypoint-initdb.d/
