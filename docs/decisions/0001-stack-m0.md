# ADR-0001 : Stack M0 proposée (Godot + FastAPI)

- Status: proposed (appliquée pour M0 tant que Nico n'a pas tranché)
- Date: 2026-09-30

## Contexte

Besoin d'un squelette natif + serveur d'IA local pour la candidature ASUS Ascent GX10.

## Décision

- Client : Godot 4 (GDScript)
- Serveur : Python + FastAPI
- LLM : API compatible OpenAI via env
- RAG : interface + mémoire d'abord

## Conséquences

Permet un M0 rapide et testable en CI. Le moteur (Godot vs Unity) reste une **question ouverte pour Nico**.
