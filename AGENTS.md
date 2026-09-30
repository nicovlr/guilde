# Règles pour les agents — GUILDE

Ce fichier reprend les sections 4 et 10 du brief. À lire avant toute contribution.

## Règles non négociables

1. **Dépôt privé.** Aucun secret commité (tokens, clés, `.env`). Seulement un `.env.example`.
2. **Aucune donnée réelle d'entreprise**, ni code/données issus d'un autre projet ou employeur. Uniquement des données fictives générées.
3. **Aucun chiffre de performance inventé.** Toute mesure vient d'une exécution réelle, sinon écrire `TODO(measure)`.
4. **Pas de push direct sur `main` :** branche → PR → CI verte. (Protection de branche : convention si le plan GitHub ne la permet pas.)
5. **Doute produit :** ouvrir une issue `question`, ne pas improviser.
6. **Pas de dépendance lourde ou payante** sans validation de Nico.
7. **Pas de fichier LICENSE** tant que Nico n'a pas décidé.

## Méthode de travail

- Un agent = une branche (ou worktree) `feat/<zone>-<sujet>` (préfixes : `docs/`, `infra/`, `ai/`, `client/`, `data/`).
- Créer l'issue **avant** de coder.
- Petites PR, une par sujet. Conventional Commits : `feat:`, `fix:`, `docs:`, `chore:`.
- Le Lead tient `docs/roadmap.md` à jour et arbitre les conflits.
- Rapport de fin de session : **fait / bloqué / prochaine étape / décisions requises de Nico**.

## Décisions réservées à Nico

Ne pas trancher seuls — issues `question` :

- Nom définitif du produit
- Moteur (Godot vs Unity)
- Licence
- Publication open source ou non

Stack proposée (à appliquer tant que Nico n'a pas tranché autrement) : Godot 4 + FastAPI + LLM OpenAI-compatible local.
