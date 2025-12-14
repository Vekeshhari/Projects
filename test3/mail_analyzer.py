# mail_analyzer.py
from datetime import datetime
import json
import hashlib
import re
import requests
from bs4 import BeautifulSoup
from Levenshtein import distance as levenshtein_distance
from db_handler import (
    insert_trusted,
    insert_untrusted,
    insert_email_hash,
    get_not_spoofed_emails,
    insert_not_spoofed,
    insert_link_file,
    insert_spoofed 
)

# Optional: Set your VirusTotal API key
VIRUSTOTAL_API_KEY = "VirusTotal_API_key"

# Load suspicious terms
def load_suspicious_terms(path="suspicious_terms.txt"):
    with open(path, "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

# Load lookalike character map
def load_lookalike_map(path="lookalike_map.json"):
    with open(path, "r") as f:
        return json.load(f)

SUSPICIOUS_TERMS = load_suspicious_terms()
LOOKALIKE_MAP = load_lookalike_map()

# Generate hash for email ID and timestamp
def generate_email_hash(email_id, timestamp):
    return hashlib.sha256((email_id + timestamp).encode()).hexdigest()

# Extract links using regex
def extract_links(body):
    return re.findall(r'(https?://[^\s]+)', body)    # captures http + https

# Check for mismatched links
# Extracts: display text → what the user sees, actual href → the real destination
def check_link_mismatch(body):
    soup = BeautifulSoup(body, "html.parser")
    alerts = []
    for link in soup.find_all("a", href=True):
        display = link.get_text().strip()
        actual = link['href'].strip()
        if display and display != actual and not actual.startswith(display):
            alerts.append(f"⚠️ Mismatched link: Display '{display}' vs Actual '{actual}'")
    return alerts  

# Check for common URL shorteners
def check_url_shorteners(links):
    shorteners = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "buff.ly"]
    alerts = []
    for url in links:
        for short in shorteners:
            if short in url:
                alerts.append(f"⚠️ URL shortener used: {url}")
    return alerts

# Query VirusTotal for malicious URLs
def check_virustotal(url):
    try:
        headers = {"x-apikey": VIRUSTOTAL_API_KEY}
        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )
        if response.status_code != 200:
            return None

        url_id = response.json()["data"]["id"]
        result = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{url_id}",
            headers=headers
        ).json()

        score = result["data"]["attributes"]["stats"]["malicious"]
        if score >= 1:
            return f"⚠️ VirusTotal Alert: Malicious score {score} for URL: {url}"
    except Exception as e:
        print(f"VirusTotal error: {e}")
    return None

# Analyze links in the email ( perform above three function )
def analyze_links(email_id, body, time_received):
    links = extract_links(body)
    if not links:
        return []

    alerts = [f"⚠️ Email from {email_id} contains link(s), added to link_files."]

    # Insert each found link into link_files
    for url in links:
        insert_link_file(email_id, url, time_received)

    mismatch_alerts = check_link_mismatch(body)
    alerts.extend(mismatch_alerts)

    shortener_alerts = check_url_shorteners(links)
    alerts.extend(shortener_alerts)

    for url in links:
        vt_alert = check_virustotal(url)
        if vt_alert:
            alerts.append(vt_alert)

    return alerts

# Check for suspicious terms in subject and body
def check_content_for_terms(subject, body, email_id):
    text = (subject + " " + body).lower()
    for term in SUSPICIOUS_TERMS:
        if term in text:
            insert_untrusted(email_id, term)
            return f"⚠️ Suspicious term '{term}' found in email from {email_id}"
    if email_id in get_not_spoofed_emails():
        insert_trusted(email_id)
    return None

# Lookalike spoofing detection
def is_lookalike_spoof(email_id, known_emails):
    def is_similar_char(a, b):
        return b in LOOKALIKE_MAP.get(a.lower(), [])

    username = email_id.split('@')[0]

    for known in known_emails:
        if email_id == known:
            continue

        known_user = known.split('@')[0]

        # dynamic similarity threshold (80% for long names, 90% for short)
        if len(username) <= 6:
            similarity_threshold = 0.90     # short names need strict match
        else:
            similarity_threshold = 0.80     # long names allow small variation

        # compare only min length
        min_len = min(len(username), len(known_user))

        match_count = sum(
            username[i] == known_user[i] or is_similar_char(username[i], known_user[i])
            for i in range(min_len)
        )

        similarity = match_count / max(len(username), len(known_user))

        if similarity >= similarity_threshold:
            return True, known

    return False, None


# Levenshtein distance spoofing detection
def is_levenshtein_spoof(email_id, known_emails,):
    username = email_id.split('@')[0]
    threshold = max(1, int(len(username) * 0.25))
    for known in known_emails:
        if email_id == known:
            continue

        known_user = known.split('@')[0]
        distance = levenshtein_distance( username,known_user)
        if distance <= threshold:
            return True, known
    return False, None

# Main email analysis function
def analyze_email(email_id, subject, body, time_received):
    timestamp = time_received.strftime("%Y-%m-%d %H:%M:%S")
    email_hash = generate_email_hash(email_id, timestamp)
    insert_email_hash(email_id, email_hash, timestamp)

    alerts = []

    # Step 1: Analyze links
    link_alerts = analyze_links(email_id, body, time_received)
    if link_alerts:
        alerts.extend(link_alerts)

    # Step 2: Check spoofing
    not_spoofed_list = get_not_spoofed_emails()
    spoofing_detected = False

    if email_id not in not_spoofed_list:
        lookalike_flag, lookalike_match = is_lookalike_spoof(email_id, not_spoofed_list)
        if lookalike_flag:
            spoofing_detected = True
            insert_spoofed(email_id, time_received)
            alerts.append(f"⚠️ Spoofing alert! '{email_id}' mimics '{lookalike_match}' using lookalike characters.")
        else:
            levenshtein_flag, lev_match = is_levenshtein_spoof(email_id, not_spoofed_list)
            if levenshtein_flag:
                spoofing_detected = True
                insert_spoofed(email_id, time_received)
                alerts.append(f"⚠️ Spoofing alert! '{email_id}' is very similar to known email '{lev_match}'.")

        if not spoofing_detected:
            insert_not_spoofed(email_id)

    # Step 3: Suspicious terms
    suspicious_alert = check_content_for_terms(subject, body, email_id)
    if suspicious_alert:
        alerts.append(suspicious_alert)

    # Step 4: Safe email confirmation
    if (
        not link_alerts and           # no suspicious links
        not spoofing_detected and     # no spoofing
        not suspicious_alert          # no suspicious terms
    ):
        alerts.append(f"✅ Safe email from {email_id}")

    return alerts
