FROM keycloak/keycloak:26.1

COPY realms.json /opt/keycloak/data/import/
COPY entrypoint.sh /tmp/

USER root

RUN chmod +x /tmp/entrypoint.sh && \
    chown -R 1000:1000 /opt/keycloak/data/import/

USER 1000

ENTRYPOINT [ "/tmp/entrypoint.sh" ]
