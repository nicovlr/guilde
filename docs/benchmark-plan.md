# Plan de benchmark GUILDE

Ce document décrit le **protocole de mesure**. Aucun résultat chiffré ici tant qu'une exécution réelle n'a pas été faite. Sinon : `TODO(measure)`.

## Objectif

Comparer l'expérience PNJ **locale** (GX10 / machine lab) à une référence **cloud** (ex. Claude Sonnet) **uniquement sur données fictives**.

## Métriques

| ID | Métrique | Définition | Unité |
|----|----------|------------|-------|
| L1 | Latence réponse PNJ | Temps entre fin `POST /npc/{id}/talk` côté client et réception HTTP 200 | ms (p50, p95) |
| L2 | Latence bout-en-bout UI | Temps entre clic Envoyer et affichage de la réponse | ms |
| P1 | Agents en parallèle | Nombre de dialogues simultanés sans erreur | count |
| F1 | Fidélité aux données | % de réponses qui citent correctement un fait du seed (grille manuelle) | % |
| M1 | Taille modèle | Paramètres / artefact chargé | params / Go |
| M2 | Quantification | Schéma (fp16, int8, q4_…) | label |
| C1 | Local vs cloud | Même prompts fictifs, même grille F1, latences L1 | tableau comparatif |

## Protocole

1. Fixer `COMPANY_SEED` (ex. 42) et exporter le JSON (`make generate-data`).
2. Préparer une **bank de 20 prompts** couvrant trésorerie, factures, clients, fournisseurs, historique d'échanges.
3. Exécuter 3 warm-up puis N=30 requêtes par condition.
4. Conditions minimales :
   - mock (baseline CI)
   - LLM local (modèle + quantif documentés)
   - cloud référence (données fictives uniquement)
5. Pour F1 : deux réviseurs humains notent indépendamment (oui/non/partiel) ; divergences tranchées.
6. Journaliser hardware (CPU/GPU/RAM), versions (`LLM_MODEL`, commit git).

## Ce qui est interdit

- Inventer des latences ou scores.
- Utiliser des données réelles d'entreprise.
- Publier des clés API dans le dépôt.

## Résultats

`TODO(measure)` — table à ajouter après première campagne (issue dédiée).
