import requests
import time
import json

# --- CONFIGURATION ---
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/YOUR_SECRET_LINK"
TARGET_TECH_STACK = ["paypal", "twilio", "jinja2", "oauth2", "dex", "subdomain-takeover"]

def check_new_cves():
    # Calling the NVD API for the latest vulnerabilities
    api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate=2026-02-01T00:00:00.000"
    try:
        response = requests.get(api_url).json()
        for vulnerability in response.get('vulnerabilities', []):
            cve_id = vulnerability['cve']['id']
            description = vulnerability['cve']['descriptions'][0]['value'].lower()
            
            # Match against your elite target list
            if any(tech in description for tech in TARGET_TECH_STACK):
                send_alert(f"🚨 **URGENT CVE MATCH:** {cve_id}\nTarget Context: {description[:200]}...")
    except Exception as e:
        print(f"Error checking NVD: {e}")

def send_alert(message):
    requests.post(DISCORD_WEBHOOK, json={"content": message})

if __name__ == "__main__":
    while True:
        check_new_cves()
        time.sleep(3600)  # Check every hour
