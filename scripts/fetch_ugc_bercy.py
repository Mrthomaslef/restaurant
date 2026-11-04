#!/usr/bin/env python3
import html
import json
import urllib.request
from datetime import datetime, timedelta

def fetch_ugc_bercy_day(date_str):
    movies = []
    seen_ids = set()
    for page in (1, 2, 3):
        url = f"https://www.allocine.fr/_/showtimes/theater-C0026/d-{date_str}/p-{page}/"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json"
            }
        )
        try:
            raw = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
            data = json.loads(raw)
        except Exception:
            break

        results = data.get("results") or []
        for item in results:
            m = item.get("movie") or {}
            title = html.unescape(m.get("title") or "")
            if not title:
                continue
            mid = str(m.get("internalId") or title)
            if mid in seen_ids:
                continue
            seen_ids.add(mid)

            poster = (m.get("poster") or {}).get("url") or ""
            genres = [g.get("translate") for g in (m.get("genres") or []) if g.get("translate")]
            stats = m.get("stats") or {}
            ur_obj = stats.get("userRating") or {}
            pr_obj = stats.get("pressReview") or {}

            ur_score = ur_obj.get("score")
            ur_count = ur_obj.get("count") or 0
            pr_score = pr_obj.get("score")
            pr_count = pr_obj.get("count") or 0

            user_rating_str = f"{float(ur_score):.1f}".replace(".", ",") if ur_score else None
            press_rating_str = f"{float(pr_score):.1f}".replace(".", ",") if pr_score else None
            main_score = round(float(ur_score or pr_score or 0.0), 1)
            main_rating_str = f"{main_score:.1f}".replace(".", ",") if main_score > 0 else "—"

            full_synopsis = html.unescape((m.get("synopsis") or "").strip())

            st_obj = item.get("showtimes") or {}
            slots = []
            seen_slots = set()
            for _, arr in st_obj.items():
                if not isinstance(arr, list):
                    continue
                for s in arr:
                    starts = s.get("startsAt") or ""
                    if "T" not in starts:
                        continue
                    hhmm = starts.split("T")[1][:5]
                    ver = "VOST" if s.get("diffusionVersion") == "ORIGINAL" else "VF"
                    key = f"{hhmm}_{ver}"
                    if key in seen_slots:
                        continue
                    seen_slots.add(key)

                    ticketing = ((s.get("data") or {}).get("ticketing") or [])
                    ugc_url = "https://www.ugc.fr/cinema.html?id=14"
                    for tk in ticketing:
                        for u in (tk.get("urls") or []):
                            if "ugc.fr/reservationSeances" in u:
                                ugc_url = u.split("&mtm_")[0]
                                break
                    slots.append({"time": hhmm, "version": ver, "url": ugc_url})

            slots.sort(key=lambda x: x["time"])
            if slots:
                movies.append({
                    "id": mid,
                    "title": title,
                    "runtime": m.get("runtime") or "",
                    "genres": " • ".join(genres[:2]) if genres else "Cinéma",
                    "rating": main_rating_str,
                    "ratingNum": main_score,
                    "pressRating": press_rating_str,
                    "pressCount": pr_count,
                    "userRating": user_rating_str,
                    "userCount": ur_count,
                    "poster": poster,
                    "synopsis": full_synopsis,
                    "slots": slots
                })

        pag = data.get("pagination") or {}
        if page >= int(pag.get("totalPages") or 1):
            break

    return movies

def build_showtimes_bundle(base_date_str="2026-11-05", days=5):
    base_dt = datetime.strptime(base_date_str, "%Y-%m-%d")
    by_date = {}
    master_map = {}
    for i in range(days):
        d_str = (base_dt + timedelta(days=i)).strftime("%Y-%m-%d")
        day_movies = fetch_ugc_bercy_day(d_str)
        if day_movies:
            by_date[d_str] = day_movies
            for mv in day_movies:
                if mv["id"] not in master_map:
                    master_map[mv["id"]] = mv
    default_movies = by_date.get(base_date_str) or list(master_map.values())
    return {
        "theater": "UGC Ciné Cité Bercy (2 Cour Saint-Émilion, 75012 Paris)",
        "updatedAt": base_date_str,
        "movies": default_movies,
        "byDate": by_date
    }

if __name__ == "__main__":
    bundle = build_showtimes_bundle("2026-11-05", days=5)
    with open("ugc_bercy_showtimes.json", "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    print("Updated ugc_bercy_showtimes.json with full synopses and exact AlloCiné Presse + Spectateurs ratings.")
