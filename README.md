# research-ops

Veille arXiv + suivi d'outreach recherche, automatisés via une routine
Claude Code quotidienne, envoyés par email.

Zéro dépendance externe (Python standard library uniquement).

## Setup

### 1. Créer le repo GitHub
Crée un repo (privé de préférence, `data/contacts.md` contient des infos
personnelles) et push le contenu de ce dossier dedans :

```bash
cd research-ops
git init
git add .
git commit -m "Initial setup: veille arXiv + tracker outreach"
git branch -M main
git remote add origin git@github.com:<ton-user>/research-ops.git
git push -u origin main
```

### 2. Générer un App Password Gmail
- Active la validation en 2 étapes sur ton compte Google si ce n'est pas
  déjà fait (obligatoire pour les App Passwords).
- Va sur https://myaccount.google.com/apppasswords
- Génère un mot de passe d'application (nom libre, ex. "research-ops"),
  garde le code à 16 caractères.

### 3. Connecter le repo à Claude Code on the web
- Va sur https://claude.ai/code, connecte GitHub, sélectionne ce repo.
- Crée un environnement cloud dédié (ou utilise le Default), et ajoute les
  variables d'environnement (secrets) :
  - `GMAIL_USER`
  - `GMAIL_APP_PASSWORD`
  - `EMAIL_TO`

### 4. Programmer la routine
Depuis le CLI Claude Code (ou l'interface web selon ce qui est disponible),
utilise `/schedule` pour créer une routine quotidienne, par exemple :

```
Fréquence : tous les jours à 8h00 (heure de Paris)
Prompt : Suis les instructions de CLAUDE.md à la lettre : récupère la
veille arXiv, évalue la pertinence toi-même, relis le tracker outreach,
compose et envoie l'email du jour.
```

### 5. Tester en local (optionnel, avant de tout automatiser)
```bash
cp .env.example .env
# édite .env avec tes vraies valeurs
export $(cat .env | xargs)
python scripts/fetch_arxiv.py --hours 48
python scripts/send_email.py --subject "Test" --body "Ça marche."
```

## Structure

```
CLAUDE.md           # contexte + instructions pour l'agent, relu à chaque run
data/topics.md       # sujets/catégories de veille (éditable)
data/contacts.md      # tracker outreach profs/labs (éditable)
scripts/fetch_arxiv.py  # récupère les papiers récents (pas de filtrage sémantique)
scripts/send_email.py   # envoie l'email final via Gmail SMTP
```

## Maintenance
- Édite `data/topics.md` et `data/contacts.md` directement dans le repo
  quand tes sujets ou tes contacts évoluent — l'agent les relit à chaque
  exécution, aucune autre config à toucher.
- Les credentials Gmail restent uniquement dans les secrets de
  l'environnement cloud, jamais dans le code.
