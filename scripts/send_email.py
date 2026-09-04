#!/usr/bin/env python3
"""
Envoie un email via Gmail SMTP en utilisant un App Password.

Variables d'environnement requises (à définir comme secrets dans
l'environnement cloud Claude Code, JAMAIS dans le repo) :
    GMAIL_USER          - ton adresse Gmail complète
    GMAIL_APP_PASSWORD  - le mot de passe d'application (16 caractères)
    EMAIL_TO            - adresse de destination (peut être la même)

Usage:
    python scripts/send_email.py --subject "Veille du jour" --body-file /tmp/body.txt
    # ou directement:
    python scripts/send_email.py --subject "..." --body "texte de l'email"
"""

import argparse
import os
import smtplib
import sys
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send(subject: str, body: str) -> None:
    user = os.environ.get("GMAIL_USER")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    to_addr = os.environ.get("EMAIL_TO")

    missing = [
        name
        for name, val in [
            ("GMAIL_USER", user),
            ("GMAIL_APP_PASSWORD", password),
            ("EMAIL_TO", to_addr),
        ]
        if not val
    ]
    if missing:
        print(f"Variables d'environnement manquantes: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_addr

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(user, [to_addr], msg.as_string())

    print(f"Email envoyé à {to_addr}: {subject}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body", help="Corps de l'email en texte direct")
    group.add_argument("--body-file", help="Chemin vers un fichier contenant le corps de l'email")
    args = parser.parse_args()

    body = args.body
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as f:
            body = f.read()

    send(args.subject, body)


if __name__ == "__main__":
    main()
