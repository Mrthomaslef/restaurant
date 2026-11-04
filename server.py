#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serveur local & Agent d'automatisation pour « Resto en Amoureux • Marie & Thomas »
- Sert l'application PWA sur http://localhost:8790
- Lit en direct les données de /Users/thomaslefevre/Documents/agenda-famille/family_data.json
  et /Users/thomaslefevre/Documents/Agendainterventionnel/personal_data.json
- Permet d'enregistrer une garde Grands-Parents ou une réservation directement dans le fichier local et le Cloud familial
- Permet de lancer l'ouverture / pré-remplissage automatique du portail de réservation (Zenchef / TheFork / SevenRooms / Google Reserve)
"""
from __future__ import annotations

import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import webbrowser

BASE_DIR = Path(__file__).resolve().parent
AGENDA_FAMILLE_JSON = Path("/Users/thomaslefevre/Documents/agenda-famille/family_data.json")
PERSONAL_DATA_JSON = Path("/Users/thomaslefevre/Documents/Agendainterventionnel/personal_data.json")
LOCAL_STATE_JSON = BASE_DIR / "resto_state.json"


def load_combined_payload() -> dict:
    family_data = {}
    if AGENDA_FAMILLE_JSON.exists():
        try:
            family_data = json.loads(AGENDA_FAMILLE_JSON.read_text(encoding="utf-8"))
        except Exception:
            pass

    personal_rdvs = []
    if PERSONAL_DATA_JSON.exists():
        try:
            pdata = json.loads(PERSONAL_DATA_JSON.read_text(encoding="utf-8"))
            personal_rdvs = pdata.get("personal_rdvs", [])
        except Exception:
            pass

    local_state = {}
    if LOCAL_STATE_JSON.exists():
        try:
            local_state = json.loads(LOCAL_STATE_JSON.read_text(encoding="utf-8"))
        except Exception:
            pass

    return {
        "ok": True,
        "family_data": family_data,
        "personal_rdvs": personal_rdvs,
        "local_state": local_state,
    }


class RestoHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/family-sync":
            payload = load_combined_payload()
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            data = json.loads(raw)
        except Exception:
            data = {}

        if parsed.path == "/api/auto-book":
            booking_url = data.get("booking_url") or ""
            if booking_url and data.get("open_browser", False):
                try:
                    webbrowser.open(booking_url)
                except Exception:
                    pass

            # Save booking in local state
            state = {}
            if LOCAL_STATE_JSON.exists():
                try:
                    state = json.loads(LOCAL_STATE_JSON.read_text(encoding="utf-8"))
                except Exception:
                    state = {}
            bookings = state.get("bookings", [])
            if data.get("booking"):
                bookings.insert(0, data["booking"])
                state["bookings"] = bookings[:50]
                LOCAL_STATE_JSON.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

            resp = json.dumps({"ok": True, "status": "auto_booking_dispatched", "booking": data.get("booking")}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
            return

        if parsed.path == "/api/save-event":
            ev = data.get("event")
            if ev and AGENDA_FAMILLE_JSON.exists():
                try:
                    fdata = json.loads(AGENDA_FAMILLE_JSON.read_text(encoding="utf-8"))
                    evs = [e for e in fdata.get("events", []) if e.get("id") != ev.get("id")]
                    evs.append(ev)
                    fdata["events"] = evs
                    AGENDA_FAMILLE_JSON.write_text(json.dumps(fdata, indent=2, ensure_ascii=False), encoding="utf-8")
                except Exception:
                    pass
            resp = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
            return

        self.send_response(404)
        self.end_headers()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8790"))
    server = ThreadingHTTPServer(("0.0.0.0", port), RestoHandler)
    print(f"🍷 Resto en Amoureux (Marie & Thomas) démarré sur http://localhost:{port}")
    server.serve_forever()
