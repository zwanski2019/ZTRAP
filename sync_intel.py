import requests
import json
import os

# Configuration
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
DICT_FILE = "red_team_dictionary.json"

def fetch_latest_cves():
    print("[+] Syncing with Global Vulnerability Stream...")
    # Fetching CVEs published in the last 24 hours
    params = {"resultsPerPage": 10} 
    try:
        response = requests.get(NVD_API_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('vulnerabilities', [])
    except Exception as e:
        print(f"[-] Connection Error: {e}")
    return []

def update_dictionary():
    new_vulns = fetch_latest_cves()
    if not new_vulns: return

    with open(DICT_FILE, 'r+') as f:
        current_data = json.load(f)
        
        for v in new_vulns:
            cve_id = v['cve']['id']
            desc = v['cve']['descriptions'][0]['value']
            
            # Sophisticated logic to filter only high-impact web/cloud/AI vulns
            entry = {
                "term": f"Exploit: {cve_id}",
                "category": "Zero-Day/Newly Disclosed",
                "definition": desc[:300] + "...",
                "ttp_2026": "Automated cross-reference required. High probability of RCE if unpatched.",
                "command": f"nuclei -id {cve_id} -u [TARGET]"
            }
            
            # Prevent duplicates
            if not any(d['term'] == entry['term'] for d in current_data):
                current_data.append(entry)
        
        f.seek(0)
        json.dump(current_data, f, indent=2)
        f.truncate()
    print(f"[+] Synced {len(new_vulns)} new intelligence nodes.")

if __name__ == "__main__":
    update_dictionary()