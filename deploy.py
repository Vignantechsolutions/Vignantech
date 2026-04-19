"""
deploy.py — Automated deployment to GitHub + Render
Usage: python deploy.py
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
import getpass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── helpers ──────────────────────────────────────────────────────────────────

def run(cmd, cwd=BASE_DIR, check=True):
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()

def api(url, token, method="GET", data=None):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github+json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

def render_api(url, token, method="GET", data=None):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

# ── step 1: collect tokens ────────────────────────────────────────────────────

print("\n=== Vignan TechSolutions — Automated Deployment ===\n")
print("You need two API tokens. Get them from:")
print("  GitHub : https://github.com/settings/tokens/new  (scopes: repo)")
print("  Render : https://dashboard.render.com/u/settings  → API Keys\n")

GITHUB_TOKEN  = getpass.getpass("GitHub Personal Access Token: ").strip()
GITHUB_USER   = input("GitHub username: ").strip()
REPO_NAME     = input("GitHub repo name [vignan-techsolutions]: ").strip() or "vignan-techsolutions"
RENDER_TOKEN  = getpass.getpass("Render API Key: ").strip()

print()

# ── step 2: secrets for Render ────────────────────────────────────────────────

print("Enter production secrets (leave blank to set later in Render dashboard):")
SENDGRID_KEY  = getpass.getpass("  SENDGRID_API_KEY: ").strip()
RZP_KEY_ID    = input("  RAZORPAY_KEY_ID: ").strip()
RZP_SECRET    = getpass.getpass("  RAZORPAY_KEY_SECRET: ").strip()

# ── step 3: git init + push ───────────────────────────────────────────────────

print("\n[1/4] Initialising git repository...")

if not os.path.exists(os.path.join(BASE_DIR, ".git")):
    run("git init")
    run("git branch -M main")

run("git add .")
commit_out = run("git commit -m \"Deploy: Vignan TechSolutions\"", check=False)
if "nothing to commit" in commit_out:
    print("  Nothing new to commit, continuing...")

print("[2/4] Creating GitHub repository...")
gh_resp = api(
    "https://api.github.com/user/repos",
    GITHUB_TOKEN,
    method="POST",
    data={"name": REPO_NAME, "private": False, "description": "Vignan TechSolutions Corporate Training Platform"}
)

if "clone_url" in gh_resp:
    clone_url = gh_resp["clone_url"]
    print(f"  Created: {clone_url}")
elif gh_resp.get("errors", [{}])[0].get("message") == "name already exists on this account":
    clone_url = f"https://github.com/{GITHUB_USER}/{REPO_NAME}.git"
    print(f"  Repo already exists: {clone_url}")
else:
    print(f"  GitHub error: {gh_resp}")
    sys.exit(1)

# set remote
remotes = run("git remote", check=False)
if "origin" in remotes:
    run("git remote set-url origin " + clone_url)
else:
    run("git remote add origin " + clone_url)

auth_url = clone_url.replace("https://", f"https://{GITHUB_USER}:{GITHUB_TOKEN}@")
run(f"git push -u {auth_url} main --force")
print("  Pushed to GitHub ✓")

# ── step 4: create Render service via Blueprint ───────────────────────────────

print("[3/4] Deploying to Render via Blueprint...")

REPO_URL = f"https://github.com/{GITHUB_USER}/{REPO_NAME}"

# get owner id
owner = render_api("https://api.render.com/v1/owners?limit=1", RENDER_TOKEN)
owner_id = owner[0]["owner"]["id"] if isinstance(owner, list) else None

if not owner_id:
    print(f"  Render auth error: {owner}")
    sys.exit(1)

# create service
env_vars = [
    {"key": "DEBUG",            "value": "False"},
    {"key": "ALLOWED_HOSTS",    "value": "vignan-techsolutions.onrender.com"},
    {"key": "COMPANY_NAME",     "value": "Vignan TechSolutions"},
    {"key": "COMPANY_EMAIL",    "value": "vignantechsolutions@gmail.com"},
    {"key": "COMPANY_PHONE",    "value": "+91-9110478047 / +91-9148215446"},
    {"key": "COMPANY_ADDRESS",  "value": "Kalaburagi, Karnataka, India"},
    {"key": "DEFAULT_FROM_EMAIL", "value": "Vignan TechSolutions <vignantechsolutions@gmail.com>"},
]
if SENDGRID_KEY:
    env_vars.append({"key": "SENDGRID_API_KEY", "value": SENDGRID_KEY})
if RZP_KEY_ID:
    env_vars.append({"key": "RAZORPAY_KEY_ID", "value": RZP_KEY_ID})
if RZP_SECRET:
    env_vars.append({"key": "RAZORPAY_KEY_SECRET", "value": RZP_SECRET})

payload = {
    "type": "web_service",
    "name": "vignan-techsolutions",
    "ownerId": owner_id,
    "repo": REPO_URL,
    "branch": "main",
    "region": "singapore",
    "plan": "free",
    "runtime": "python",
    "buildCommand": "./build.sh",
    "startCommand": "gunicorn vignan_tech.wsgi:application --bind 0.0.0.0:$PORT --workers 2",
    "envVars": env_vars,
    "autoDeploy": "yes",
}

svc = render_api("https://api.render.com/v1/services", RENDER_TOKEN, method="POST", data=payload)

if "service" in svc:
    service_id  = svc["service"]["id"]
    service_url = svc["service"].get("serviceDetails", {}).get("url", "")
    print(f"  Web service created: {service_url} ✓")
elif svc.get("id"):
    service_id  = svc["id"]
    service_url = svc.get("serviceDetails", {}).get("url", "")
    print(f"  Web service created ✓")
else:
    print(f"  Render response: {json.dumps(svc, indent=2)}")
    print("  Check Render dashboard — service may still have been created.")
    service_id = None

# ── step 5: create PostgreSQL database ───────────────────────────────────────

print("[4/4] Creating PostgreSQL database on Render...")

db_payload = {
    "name": "vignan-db",
    "databaseName": "vignan_techsolutions",
    "ownerId": owner_id,
    "region": "singapore",
    "plan": "free",
}

db = render_api("https://api.render.com/v1/postgres", RENDER_TOKEN, method="POST", data=db_payload)

if db.get("id") or (isinstance(db, dict) and "id" in db):
    db_id = db.get("id") or db["id"]
    print(f"  PostgreSQL database created (id: {db_id}) ✓")
    print("  NOTE: Link DATABASE_URL manually in Render dashboard:")
    print("        Service → Environment → Add from Database → vignan-db → connectionString")
else:
    print(f"  DB response: {json.dumps(db, indent=2)}")

# ── done ──────────────────────────────────────────────────────────────────────

print("\n=== Deployment initiated ✓ ===")
print(f"  GitHub : https://github.com/{GITHUB_USER}/{REPO_NAME}")
print(f"  Render : https://dashboard.render.com")
print()
print("Next steps:")
print("  1. In Render dashboard → vignan-techsolutions → Environment")
print("     → Add DATABASE_URL from vignan-db (Internal Connection String)")
print("  2. Wait for build to complete (~3-5 min)")
print("  3. Open Render Shell → run: python manage.py createsuperuser")
print()
