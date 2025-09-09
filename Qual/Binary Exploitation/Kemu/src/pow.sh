#!/bin/sh
# Minimal, safer Hashcash gate with backoff

set -eu

# ---- Tunables (can be overridden via environment) ----
LENGTH="${LENGTH:-16}"            # resource length
STRENGTH="${STRENGTH:-26}"        # PoW difficulty (bits)
MAX_TRIES="${MAX_TRIES:-3}"       # attempts before exit
WRONG_DELAY_BASE="${WRONG_DELAY_BASE:-2}"  # seconds; backoff base 2,4,8,...
SDB="${SDB:-/tmp/hashcash.sdb}"   # double-spend database (persists across runs)

# ---- Dependency checks ----
for bin in hashcash dd base64 tr cut; do
  command -v "$bin" >/dev/null 2>&1 || { echo "Missing dependency: $bin" >&2; exit 1; }
done

# ---- Prepare DB file with restrictive perms ----
umask 077
: > "$SDB" 2>/dev/null || touch "$SDB"

# ---- Create a URL-/shell-safe challenge resource ----
challenge="$(
  dd if=/dev/urandom bs=32 count=1 2>/dev/null \
  | base64 \
  | tr '+/' '_.' \
  | tr -d '\n' \
  | cut -c -"${LENGTH}"
)"

printf 'Solve this proof-of-work challenge:\nhashcash -mb%s -r %s\n' "$STRENGTH" "$challenge"

tries=0
while [ "$tries" -lt "$MAX_TRIES" ]; do
  printf 'Enter your hashcash token: '
  IFS= read -r token || { echo "[-] No input"; exit 1; }

  # Lightweight sanity check to filter obvious garbage/paste noise
  if printf '%s' "$token" | LC_ALL=C tr -d 'A-Za-z0-9_+.:/=$' | grep -q .; then
    echo "[-] Invalid token characters"
  elif hashcash -q -cdb"$STRENGTH" -f "$SDB" -r "$challenge" "$token" 2>/dev/null; then
    echo "[+] Correct"
    exec /home/pwn/run.sh
  else
    echo "[-] Wrong"
  fi

  tries=$((tries + 1))
  delay=$((WRONG_DELAY_BASE << (tries - 1)))   # 2,4,8,... seconds
  echo "Waiting $delay s before next attempt..."
  sleep "$delay"
done

echo "[!] Too many attempts"
exit 1
