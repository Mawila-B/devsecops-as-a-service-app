import os
import requests
import json

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")


def send_slack_alert(scan_id, results):
    if not SLACK_WEBHOOK_URL:
        print("Slack webhook URL not set, skipping Slack alert")
        return

    text = f"*DevSecOps Scan Completed* - Scan ID: {scan_id}\n"
    for tool, path in results.items():
        text += f"• {tool}: results saved at `{path}`\n"

    payload = {"text": text}
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if resp.status_code != 200:
            print(f"Slack alert failed: {resp.text}")
    except Exception as e:
        print(f"Slack alert error: {str(e)}")


def send_jira_issue(scan_id, results):
    if not all([JIRA_BASE_URL, JIRA_USERNAME, JIRA_API_TOKEN, JIRA_PROJECT_KEY]):
        print("JIRA credentials not set, skipping JIRA alert")
        return

    # Very simple issue creation with scan summary
    url = f"{JIRA_BASE_URL}/rest/api/2/issue"
    headers = {
        "Content-Type": "application/json",
    }
    auth = (JIRA_USERNAME, JIRA_API_TOKEN)

    description = f"DevSecOps Scan Completed. Scan ID: {scan_id}\n\nResults:\n"
    for tool, path in results.items():
        description += f"- {tool}: {path}\n"

    data = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": f"DevSecOps Scan Alert - {scan_id}",
            "description": description,
            "issuetype": {"name": "Task"},
        }
    }

    try:
        resp = requests.post(url, headers=headers, auth=auth, json=data)
        if resp.status_code not in [200, 201]:
            print(f"JIRA alert failed: {resp.text}")
    except Exception as e:
        print(f"JIRA alert error: {str(e)}")
