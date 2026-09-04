# research-ops — contexte pour l'agent

## Qui je suis
Aaron, étudiant ingénieur (Télécom SudParis + MIT ASP), en préparation d'une
césure recherche en AI/ML. Objectif : PhD en AI/ML. Sujets d'intérêt actuels :
inference-time steering des modèles de diffusion, sampling/SMC, deep learning
théorique.

## Ce que ce repo automatise
Deux choses, exécutées chaque matin par une routine Claude Code :

1. **Veille arXiv** — repérer les nouveaux papiers pertinents pour mes sujets
   (voir `data/topics.md`) et n'en garder que 3 à 6 vraiment intéressants,
   pas une liste brute filtrée par mot-clé.
2. **Suivi outreach** — relire `data/contacts.md` et signaler :
   - les relances dues (pas de réponse depuis X jours après un contact)
   - toute nouvelle publication d'un des contacts listés (bon prétexte de
     relance)

## Ce que je veux de toi (agent) à chaque run

1. Exécute `python scripts/fetch_arxiv.py` pour récupérer les papiers des
   dernières 24h dans les catégories listées dans `data/topics.md`.
2. **Ne te contente pas de filtrer par mot-clé.** Lis les abstracts, juge
   toi-même la pertinence par rapport à mes sujets et à ma trajectoire de
   recherche, et ne garde que ce qui vaut vraiment la peine d'être lu.
   Pour chaque papier retenu, écris 1-2 phrases expliquant pourquoi ça
   m'intéresse, pas juste un résumé de l'abstract.
3. Relis `data/contacts.md`. Si une relance est due ou si un contact a publié
   quelque chose de nouveau (tu peux chercher son nom + arXiv/Google Scholar),
   signale-le avec une suggestion concrète d'angle de relance.
4. Compose un email court (pas un rapport interminable) avec ces deux
   sections, et envoie-le avec `python scripts/send_email.py` (voir le
   script pour les arguments attendus).
5. Ne modifie `data/contacts.md` que si je te le demande explicitement dans
   un message — sinon laisse le fichier tel quel, je le mets à jour moi-même.

## Style
- Emails en français, direct, sans blabla.
- Si vraiment rien de pertinent un jour donné, envoie un email très court
  qui le dit plutôt que de forcer du contenu.
