# GUILDE (nom de travail)

Logiciel natif de **gestion d'entreprise en open world** : services = quartiers, clients/fournisseurs = PNJ pilotés par agents IA locaux, trésorerie = économie, tâches = quêtes.

> Candidature : [ASUS Ascent GX10 Local AI Developer Challenge](https://www.asus.com/) — clôture candidatures **4 octobre 2026**.

## Statut

Squelette **M0** : prouve l'architecture client ↔ ai-server local ↔ données fictives. Pas le produit final.

Dépôt : **https://github.com/nicovlr/guilde** (privé).

## Architecture (résumé)

Voir [docs/architecture.md](docs/architecture.md).

```
Godot client  --HTTP-->  FastAPI ai-server  -->  RAG mémoire + LLM local (ou mock)
                              |
                         data/ (seed)
```

## Démarrage rapide

Prérequis : Python 3.11+, Make, [Godot 4.3+](https://godotengine.org/) (pour le client).

```bash
git clone https://github.com/nicovlr/guilde.git
cd guilde
cp .env.example .env
make setup
make test
make run-server   # mock, http://127.0.0.1:8000
```

Puis ouvrir `client/project.godot` dans Godot → F5. Approcher un PNJ, touche **E**, dialoguer.

Health check :

```bash
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/npc/npc-1/talk \
  -H 'Content-Type: application/json' \
  -d '{"message":"Quelle est la trésorerie ?"}'
```

Mode LLM réel (Ollama / vLLM) :

```bash
export LLM_MODE=openai
export LLM_BASE_URL=http://127.0.0.1:11434/v1
export LLM_MODEL=llama3.1
make run-server
```

## Captures d'écran

Dossier prévu : `docs/screenshots/` — `TODO` : ajouter des captures Godot + dialogue mock pour la vidéo de candidature.

## Règles agents

Lire [AGENTS.md](AGENTS.md). Pas de push direct sur `main`, pas de secrets, pas de données réelles.

## Décisions en attente (Nico)

Nom définitif · moteur (Godot/Unity) · licence · open source — issues labellisées `question`.
