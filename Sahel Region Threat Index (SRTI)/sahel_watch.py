"""
Sahel Region Threat Index (SRTI)
RSS-first OSINT pipeline for Mali, Niger, and Burkina Faso.
Outputs:
  - data/srti_latest.json
  - data/srti_history.json
  - Sahel Region Threat Index (SRTI)/sahel_data.csv
"""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin
from xml.etree import ElementTree as ET

import requests
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

SRTI_DIR = Path(__file__).resolve().parent
EVENT_LOG_CSV = SRTI_DIR / "sahel_data.csv"
LATEST_JSON = DATA_DIR / "srti_latest.json"
HISTORY_JSON = DATA_DIR / "srti_history.json"

USER_AGENT = "MonarchCastleSRTI/1.0 (+https://monarchcastle.tech)"
HEADERS = {"User-Agent": USER_AGENT}

WINDOW_HOURS = 72
HISTORY_LIMIT = 24 * 30
FORECAST_HOURS = 6
COUP_WINDOW_HOURS = 24
MAX_LOG_ROWS = 2000

SOURCES = [
    {
        "name": "ReliefWeb - Mali",
        "rss": "https://reliefweb.int/rss?search=country%3AMali",
        "html": "https://reliefweb.int/country/mli",
        "region_focus": True,
        "weight": 0.9,
    },
    {
        "name": "ReliefWeb - Niger",
        "rss": "https://reliefweb.int/rss?search=country%3ANiger",
        "html": "https://reliefweb.int/country/ner",
        "region_focus": True,
        "weight": 0.9,
    },
    {
        "name": "ReliefWeb - Burkina Faso",
        "rss": "https://reliefweb.int/rss?search=country%3ABurkina%20Faso",
        "html": "https://reliefweb.int/country/bfa",
        "region_focus": True,
        "weight": 0.9,
    },
    {
        "name": "MaliWeb",
        "rss": "https://www.maliweb.net/feed",
        "html": "https://www.maliweb.net/",
        "region_focus": True,
        "weight": 0.8,
    },
    {
        "name": "LeFaso",
        "rss": "https://lefaso.net/spip.php?page=backend",
        "html": "https://lefaso.net/",
        "region_focus": True,
        "weight": 0.8,
    },
    {
        "name": "ActuNiger",
        "rss": "https://www.actuniger.com/feed/",
        "html": "https://www.actuniger.com/",
        "region_focus": True,
        "weight": 0.8,
    },
    {
        "name": "BBC Africa",
        "rss": "https://feeds.bbci.co.uk/news/world/africa/rss.xml",
        "html": "https://www.bbc.com/news/world/africa",
        "region_focus": False,
        "weight": 0.6,
    },
    {
        "name": "UN News Africa",
        "rss": "https://news.un.org/feed/subscribe/en/news/region/africa/feed/rss.xml",
        "html": "https://news.un.org/en/news/region/africa",
        "region_focus": False,
        "weight": 0.6,
    },
    {
        "name": "Crisis Group",
        "rss": "https://www.crisisgroup.org/rss.xml",
        "html": "https://www.crisisgroup.org/africa",
        "region_focus": False,
        "weight": 0.6,
    },
    {
        "name": "France 24 - Africa",
        "rss": "https://www.france24.com/en/africa/rss",
        "html": "https://www.france24.com/en/africa/",
        "region_focus": False,
        "weight": 0.7,
    },
    {
        "name": "AllAfrica - Mali",
        "rss": "https://allafrica.com/tools/headlines/rdf/mali/headlines.rdf",
        "html": "https://allafrica.com/mali/",
        "region_focus": True,
        "weight": 0.6,
    },
    {
        "name": "AllAfrica - Niger",
        "rss": "https://allafrica.com/tools/headlines/rdf/niger/headlines.rdf",
        "html": "https://allafrica.com/niger/",
        "region_focus": True,
        "weight": 0.6,
    },
    {
        "name": "AllAfrica - Burkina Faso",
        "rss": "https://allafrica.com/tools/headlines/rdf/burkinafaso/headlines.rdf",
        "html": "https://allafrica.com/burkinafaso/",
        "region_focus": True,
        "weight": 0.6,
    },
]

REGION_KEYWORDS = [
    "sahel",
    "mali",
    "niger",
    "burkina",
    "burkina faso",
    "bamako",
    "niamey",
    "ouagadougou",
    "gao",
    "tillaberi",
    "menaka",
    "agadez",
]



CONFLICT_KEYWORDS = [
    "attack",
    "ambush",
    "raid",
    "clash",
    "battle",
    "offensive",
    "assault",
    "explosion",
    "armed group",
    "gunmen",
]

CIVILIAN_KEYWORDS = [
    "civilian",
    "massacre",
    "killed",
    "dead",
    "fatal",
    "abducted",
    "kidnapped",
    "displaced",
    "refugee",
    "camp",
]

EXTREMIST_KEYWORDS = [
    "isis",
    "islamic state",
    "isgs",
    "jnim",
    "al qaeda",
    "aqim",
    "boko haram",
]


BUCKETS = {
    "conflict_intensity": {
        "keywords": CONFLICT_KEYWORDS + EXTREMIST_KEYWORDS,
        "multiplier": 1.4,
        "scale": 12,
        "weight": 0.5,
    },
    "civilian_risk": {
        "keywords": CIVILIAN_KEYWORDS,
        "multiplier": 1.8,
        "scale": 14,
        "weight": 0.2,
    },
}

def utc_now() -> datetime:
    return datetime.now(timezone.utc)



def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1].lower()


def extract_text(node: ET.Element, names: List[str]) -> str:
    for child in list(node):
        if local_name(child.tag) in names and child.text:
            return child.text.strip()
    return ""


def extract_link(node: ET.Element) -> str:
    for child in list(node):
        if local_name(child.tag) == "link":
            href = child.attrib.get("href")
            if href:
                return href.strip()
            if child.text:
                return child.text.strip()
    return ""


def fetch_url(url: str) -> Optional[bytes]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code >= 400:
            return None
        return resp.content
    except requests.RequestException:
        return None


def parse_rss(content: bytes) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        return items

    if local_name(root.tag) == "rss":
        channel = next((c for c in root if local_name(c.tag) == "channel"), None)
        if channel is None:
            return items
        for item in [c for c in channel if local_name(c.tag) == "item"]:
            title = extract_text(item, ["title"])
            link = extract_text(item, ["link"]) or extract_link(item)
            summary = extract_text(item, ["description", "summary"])
            pub = extract_text(item, ["pubdate", "date", "dc:date"])
            items.append(
                {
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": pub,
                }
            )
        return items

    if local_name(root.tag) == "feed":
        for entry in [c for c in root if local_name(c.tag) == "entry"]:
            title = extract_text(entry, ["title"])
            link = extract_link(entry)
            summary = extract_text(entry, ["summary", "content"])
            pub = extract_text(entry, ["updated", "published"])
            items.append(
                {
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": pub,
                }
            )
    return items


def scrape_headlines(html: bytes, limit: int = 12) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    for tag in soup.find_all(["h1", "h2", "h3"], limit=60):
        text = tag.get_text(strip=True)
        if not text or len(text) < 6:
            continue
        link = ""
        anchor = tag.find("a")
        if anchor and anchor.get("href"):
            link = anchor["href"]
        candidates.append({"title": text, "link": link, "summary": "", "published": ""})
    return candidates[:limit]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)


def match_keywords(text: str, keywords: List[str]) -> List[str]:
    hits = []
    for kw in keywords:
        if kw in text:
            hits.append(kw)
    return hits


def region_match(text: str) -> List[str]:
    hits = []
    for kw in REGION_KEYWORDS:
        if kw in text:
            hits.append(kw)
    return hits


def recency_weight(published: datetime, now: datetime) -> float:
    age_hours = max(0.0, (now - published).total_seconds() / 3600)
    if age_hours > WINDOW_HOURS:
        return 0.0
    return max(0.35, 1 - (age_hours / WINDOW_HOURS))


def score_item(
    text: str,
    published: datetime,
    source_weight: float,
    now: datetime,
) -> Tuple[float, Dict[str, float], List[str], List[str]]:
    normalized = normalize_text(text)
    tags = []
    region_hits = region_match(normalized)
    bucket_scores: Dict[str, float] = {}
    decay = recency_weight(published, now)
    for bucket_name, config in BUCKETS.items():
        hits = match_keywords(normalized, config["keywords"])
        if hits:
            tags.append(bucket_name)
        bucket_scores[bucket_name] = min(3, len(hits)) * config["multiplier"] * source_weight * decay
    total_score = sum(bucket_scores.values())
    return total_score, bucket_scores, tags, region_hits


def load_existing_links() -> set:
    if not EVENT_LOG_CSV.exists():
        return set()
    links = set()
    with EVENT_LOG_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            link = (row.get("link") or "").strip()
            if link:
                links.add(link)
    return links


def append_event_log(rows: List[Dict[str, str]]) -> None:
    file_exists = EVENT_LOG_CSV.exists()
    with EVENT_LOG_CSV.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "fetched_at",
                "published_at",
                "source",
                "title",
                "link",
                "regions",
                "tags",
                "score",
            ],
        )
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)

    if EVENT_LOG_CSV.exists():
        with EVENT_LOG_CSV.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > MAX_LOG_ROWS + 1:
            header = lines[0]
            trimmed = lines[-MAX_LOG_ROWS:]
            with EVENT_LOG_CSV.open("w", encoding="utf-8", newline="") as f:
                f.write(header)
                f.writelines(trimmed)


def load_history() -> List[Dict[str, object]]:
    if not HISTORY_JSON.exists():
        return []
    with HISTORY_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_history(entries: List[Dict[str, object]]) -> None:
    with HISTORY_JSON.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def normalize_bucket(raw: float, scale: float) -> float:
    return max(0.0, min(100.0, raw * scale))


def classify_score(score: float) -> str:
    if score < 20:
        return "LOW"
    if score < 40:
        return "GUARDED"
    if score < 60:
        return "ELEVATED"
    if score < 80:
        return "HIGH"
    return "CRITICAL"


def forecast_scores(history: List[Dict[str, object]], hours: int) -> List[Dict[str, object]]:
    if len(history) < 4:
        return []
    window = history[-24:]
    scores = [float(item["score"]) for item in window]
    n = len(scores)
    xs = list(range(n))
    mean_x = sum(xs) / n
    mean_y = sum(scores) / n
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, scores))
    var = sum((x - mean_x) ** 2 for x in xs) or 1.0
    slope = cov / var
    intercept = mean_y - slope * mean_x

    last_time = datetime.fromisoformat(window[-1]["timestamp"])
    prev_time = datetime.fromisoformat(window[-2]["timestamp"])
    step_delta = last_time - prev_time
    if step_delta.total_seconds() <= 0:
        step_delta = timedelta(hours=1)
    forecast = []
    for step in range(1, hours + 1):
        predicted = intercept + slope * (n - 1 + step)
        predicted = max(0.0, min(100.0, predicted))
        ts = (last_time + (step * step_delta)).isoformat()
        forecast.append({"timestamp": ts, "score": round(predicted, 1)})
    return forecast


def main() -> None:
    now = utc_now()
    existing_links = load_existing_links()
    all_items = []
    source_status = []

    for source in SOURCES:
        items: List[Dict[str, str]] = []
        status = "ok"
        rss_content = fetch_url(source["rss"])
        if rss_content:
            items = parse_rss(rss_content)
        if not items and source.get("html"):
            html_content = fetch_url(source["html"])
            if html_content:
                items = scrape_headlines(html_content)
            else:
                status = "unreachable"
        if not items and status != "unreachable":
            status = "empty"

        all_items.extend([(source, item) for item in items])
        source_status.append(
            {
                "name": source["name"],
                "url": source["rss"],
                "status": status,
                "items": len(items),
            }
        )

    event_rows = []
    scored_items = []
    raw_buckets = {key: 0.0 for key in BUCKETS}

    for source, item in all_items:
        title = (item.get("title") or "").strip()
        summary = (item.get("summary") or "").strip()
        link = (item.get("link") or "").strip()
        if link:
            base_url = source.get("html") or source.get("rss")
            link = urljoin(base_url, link)
        published = parse_datetime(item.get("published")) or now

        combined = f"{title} {summary}".strip()
        combined = strip_html(combined)
        if not combined:
            continue

        normalized = normalize_text(combined)
        region_hits = region_match(normalized)
        if not source["region_focus"] and not region_hits:
            continue

        total_score, bucket_scores, tags, region_hits = score_item(
            combined,
            published,
            source["weight"],
            now,
        )

        if total_score <= 0:
            continue

        for bucket_name, value in bucket_scores.items():
            raw_buckets[bucket_name] += value

        scored_item = {
            "title": title,
            "link": link,
            "source": source["name"],
            "published_at": published.isoformat(),
            "score": round(total_score, 2),
            "tags": tags,
            "regions": region_hits,
        }
        scored_items.append(scored_item)

        if link and link in existing_links:
            continue

        event_rows.append(
            {
                "fetched_at": now.isoformat(),
                "published_at": published.isoformat(),
                "source": source["name"],
                "title": title,
                "link": link,
                "regions": ",".join(region_hits),
                "tags": ",".join(tags),
                "score": f"{total_score:.2f}",
            }
        )

    if event_rows:
        append_event_log(event_rows)

    normalized_buckets = {}
    for bucket_name, raw_value in raw_buckets.items():
        normalized_buckets[bucket_name] = round(
            normalize_bucket(raw_value, BUCKETS[bucket_name]["scale"]),
            1,
        )

    overall_score = 0.0
    for bucket_name, score in normalized_buckets.items():
        overall_score += score * BUCKETS[bucket_name]["weight"]
    overall_score = round(overall_score, 1)
    risk_level = classify_score(overall_score)

    scored_items.sort(key=lambda x: x["score"], reverse=True)
    top_items = scored_items[:8]

    history = load_history()
    history.append(
        {
            "timestamp": now.isoformat(),
            "score": overall_score,
            "risk_level": risk_level,
            "components": normalized_buckets,
            "items": len(scored_items),
        }
    )
    if len(history) > HISTORY_LIMIT:
        history = history[-HISTORY_LIMIT:]
    save_history(history)

    forecast = forecast_scores(history, FORECAST_HOURS)

    latest = {
        "fetched_at": now.isoformat(),
        "window_hours": WINDOW_HOURS,
        "score": overall_score,
        "risk_level": risk_level,
        "components": normalized_buckets,
        "weights": {key: BUCKETS[key]["weight"] for key in BUCKETS},
        "items_count": len(scored_items),
        "sources": source_status,
        "top_headlines": top_items,
        "forecast": forecast,
    }

    with LATEST_JSON.open("w", encoding="utf-8") as f:
        json.dump(latest, f, indent=2)

    print(f"[OK] SRTI score {overall_score} ({risk_level}) from {len(scored_items)} items")


if __name__ == "__main__":
    main()
