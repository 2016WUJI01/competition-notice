from datetime import date
import os
import json
import requests
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv

load_dotenv()

today = date.today().isoformat()
API_URL = f"https://www.worldcubeassociation.org/api/v0/competitions?country_iso2=CN&start={today}&sort=-announced_at"
RESULT_FILE = "last_result.json"

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")


def fetch_api():
    resp = requests.get(API_URL)
    resp.raise_for_status()
    return resp.json()


def extract_names(api_result):
    if isinstance(api_result, list):
        return [item.get("name", "") for item in api_result]
    return []


def load_last_result():
    if not os.path.exists(RESULT_FILE):
        return None
    with open(RESULT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_result(names):
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(names, f, ensure_ascii=False, indent=2)


def send_email(subject, content):
    if not (EMAIL_USER and EMAIL_PASS and EMAIL_TO):
        print("[WARN] 邮箱环境变量未设置，跳过邮件发送。")
        return

    # 支持多个收件人，用逗号分隔
    recipients = [email.strip() for email in EMAIL_TO.split(",")]

    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = Header(EMAIL_USER)
    msg["To"] = Header(", ".join(recipients))
    msg["Subject"] = Header(subject, "utf-8")
    try:
        with smtplib.SMTP_SSL("smtp.163.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, recipients, msg.as_string())
        print(f"[INFO] 邮件已发送至: {', '.join(recipients)}")
    except Exception as e:
        print(f"[ERROR] 邮件发送失败: {e}")


def git_commit_and_push():
    subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
    subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=True)
    subprocess.run(["git", "add", RESULT_FILE], check=True)
    subprocess.run(["git", "commit", "-m", "chore: update API result [auto]"], check=True)
    subprocess.run(["git", "push"], check=True)


def get_diff(old, new):
    old_set = set(old or [])
    new_set = set(new or [])
    added = list(new_set - old_set)
    removed = list(old_set - new_set)
    diff_msg = ""
    if added:
        diff_msg += f"新增比赛：\n" + "\n".join(added) + "\n"
    if removed:
        diff_msg += f"结束比赛：\n" + "\n".join(removed) + "\n"
    if not diff_msg:
        diff_msg = "无新增或结束比赛，仅顺序变化。"
    return diff_msg


def main():
    current = fetch_api()
    current_names = extract_names(current)
    last_names = load_last_result()
    if last_names != current_names:
        diff = get_diff(last_names, current_names)
        save_result(current_names)
        send_email(subject="WCA官网 - 公示比赛变更提醒", content=diff)
    else:
        print("[INFO] API结果无变化。")


if __name__ == "__main__":
    main()
