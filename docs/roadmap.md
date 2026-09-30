# Roadmap GUILDE

## M0 — Squelette bout-en-bout (jalon actuel)

- [x] Dépôt privé + CI (ruff, pytest, structure client)
- [x] ai-server `/health`, `/npc/{id}/talk` (mock + openai)
- [x] data seed + RAG mémoire
- [x] client Godot scène + dialogue HTTP
- [x] docs architecture / benchmark-plan / ADR
- [ ] Captures d'écran pour candidature vidéo (à faire sur machine avec Godot)

## M1 — Fidélité & DX

- [ ] Brancher un LLM local réel (Ollama ou vLLM) documenté
- [ ] Améliorer le prompt PNJ (personnalité par rôle)
- [ ] Export/import JSON entreprise fictive
- [ ] Première mesure latence PNJ → remplir benchmark (pas d'invention)

## M2 — Monde & agents

- [ ] Quartiers = services, navigation plus riche
- [ ] Plusieurs agents en parallèle (mesure TODO(measure))
- [ ] Quêtes = tâches métier simples

## M3 — Voix & multimédia (après validation Nico)

- [ ] Pipeline voix locale (STT/TTS)
- [ ] Génération d'images locale (si pertinent)

## Décisions en attente (Nico)

Voir issues `question` : nom définitif, moteur, licence, open source.
