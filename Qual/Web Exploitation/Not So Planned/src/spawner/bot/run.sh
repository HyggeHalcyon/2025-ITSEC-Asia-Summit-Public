#!/usr/bin/env bash
if [[ -z "$SERVER" ]]; then
    SERVER="http://localhost:3000"
fi
printf "[+] Setting first page opened...\n"

RESPONSE=$(curl -s "$SERVER/get-plan/$UUID")

printf "[+] Received plan:\n%s\n\n" "$RESPONSE"

UUID_VALUE=$(echo "$RESPONSE" | jq -r '.plan.uuid')
TITLE_VALUE=$(echo "$RESPONSE" | jq -r '.plan.title')
TYPE_VALUE=$(echo "$RESPONSE" | jq -r '.plan.important_type')

if [[ -z "$UUID_VALUE" || -z "$TITLE_VALUE" || -z "$TYPE_VALUE" ]]; then
    echo "[-] Error: Plan data missing or malformed response"
    exit 1
fi

CONFIG_DIR="$HOME/.config/not-so-planned-chall"
mkdir -p "$CONFIG_DIR"

jq -n --arg uuid "$UUID_VALUE" --arg title "$TITLE_VALUE" --argjson type "$TYPE_VALUE" \
  '{"plans":[{"uuid":$uuid,"title":$title,"type":$type}]}' > "$CONFIG_DIR/config.json"

printf "[+] Plan saved to: $CONFIG_DIR/config.json\n"

printf "[+] Bot starting...\n"
Xvfb :0 &
DISPLAY=:0 ./not-so-planned-chall --no-sandbox