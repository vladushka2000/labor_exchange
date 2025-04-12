#!/usr/bin/env sh

set -eu

REALMS_FILE=/opt/keycloak/data/import/realms.json

sed -i -e "s#\${KC_CLIENT_SECRET}#${KC_CLIENT_SECRET}#g" "$REALMS_FILE"
sed -i -e "s#\${KC_REALM_NAME}#${KC_REALM_NAME}#g" "$REALMS_FILE"
sed -i -e "s#\${KC_CLIENT_ID}#${KC_CLIENT_ID}#g" "$REALMS_FILE"
sed -i -e "s#\${APP_URL}#${APP_URL}#g" "$REALMS_FILE"

sh /opt/keycloak/bin/kc.sh import --file=$REALMS_FILE --override=false
sh /opt/keycloak/bin/kc.sh start-dev

exec "$@"
