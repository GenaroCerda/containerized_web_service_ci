#!/usr/bin/env python3
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ENDPOINTS = os.environ.get(
    "ENDPOINTS", "http://localhost:8080/health,http://localhost:8080/ready"
).split(",")
TIMEOUT = float(os.environ.get("TIMEOUT", "3"))
RETRIES = int(os.environ.get("RETRIES", "3"))
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
STATE_FILE = os.environ.get("STATE_FILE", "/tmp/healthcheck_state.json")


def check(url):
    """Devuelve (ok, detalle). Reintenta antes de dar el fallo por bueno."""
    last = ""
    for attempt in range(1, RETRIES + 1):
        try:
            start = time.monotonic()
            with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
                ms = (time.monotonic() - start) * 1000
                if resp.status == 200:
                    return True, f"200 en {ms:.0f} ms"
                last = f"status {resp.status}"
        except Exception as exc:
            last = str(exc)
        time.sleep(1)
    return False, last


def notify(message):
    print(message)
    if not (TELEGRAM_TOKEN and TELEGRAM_CHAT_ID):
        return
    data = urllib.parse.urlencode(
        {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    ).encode()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        urllib.request.urlopen(url, data=data, timeout=10)
    except Exception as exc:
        print(f"No se pudo notificar: {exc}", file=sys.stderr)


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def main():
    state = load_state()
    new_state = {}
    failed = False

    for url in ENDPOINTS:
        ok, detail = check(url)
        new_state[url] = "up" if ok else "down"
        previous = state.get(url, "up")

        if not ok:
            failed = True
        if not ok and previous == "up":
            notify(f"🔴 CAÍDO: {url} ({detail})")
        elif ok and previous == "down":
            notify(f"🟢 RECUPERADO: {url} ({detail})")
        else:
            print(f"{'OK' if ok else 'SIGUE CAÍDO'}: {url} - {detail}")

    with open(STATE_FILE, "w") as f:
        json.dump(new_state, f)

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()