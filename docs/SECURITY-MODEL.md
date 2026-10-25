# Modèle de sécurité

> La sécurité est le cœur du projet, pas une option. Ce document dit **ce qui est protégé**, **contre quoi**, et **ce qui ne peut pas être garanti** — car prétendre à l'infaillibilité serait déjà une faille.

## Actifs à protéger

| Actif | Sensibilité |
|---|---|
| Données réglementées (profession de santé) | Catégorie spéciale — RGPD art. 9 |
| Documents professionnels de l'utilisateur | Élevée |
| Secrets (identifiants, jetons, clés) | Critique |
| Disponibilité des services | Moyenne |

## Menaces considérées

- **Exfiltration de données sensibles** vers un cloud tiers → neutralisée par l'inférence **100 % locale** et le cloisonnement réseau.
- **Mouvement latéral** depuis le domaine cyber (le plus exposé) vers le domaine sensible → bloqué par la segmentation VLAN (deny inter-VLAN), **prouvé par test**.
- **Détournement de l'agent** par un tiers → l'accès est restreint par **liste blanche** ; un message d'une identité non autorisée est ignoré.
- **Hallucination / action erronée** (facture, document, envoi) → appels d'outils **validés** (schéma, types) ; le fichier livré est un *fait* retourné par l'outil, pas une phrase du modèle ; toute action irréversible passe par une **validation humaine**.
- **Fuite de secrets dans le code** → secrets exclus par `.gitignore`, chargés depuis l'environnement, jamais en clair dans le dépôt.

## Garde-fous de conception

- **Isolation par l'architecture, pas par le prompt.** Une consigne de prompt n'est pas une serrure : un petit modèle local se contourne par formulation. La protection réelle = réseau + liste blanche.
- **Humain aux commandes.** L'agent prépare ; l'humain valide le jugement métier et tout envoi externe. Pas de diagnostic ni d'envoi autonome.
- **Moindre privilège.** Jetons d'API restreints, comptes séparés, confirmation obligatoire pour les opérations destructrices.
- **Journalisation & traçabilité** des actions pour pouvoir dire *qui a fait quoi, quand*.

## Hors de portée (limites assumées)

- Un poste déjà compromis **pendant** une session ouverte.
- Une attaque physique sur le matériel.
- Les garanties « sécurité militaire » / « zéro faille » : **aucun logiciel n'est infaillible**. On vise la défense en profondeur et la rigueur, vérifiées par des tests ; pas l'absolu.

## Conformité (cadre de réflexion, non exhaustif)

- **RGPD** (art. 9 — données de santé) : minimisation, localisation des données, traçabilité.
- **Responsabilité professionnelle** : l'outil **assiste** le praticien, qui reste décisionnaire — ce qui évite le statut de dispositif médical (aide à la rédaction, pas diagnostic).
- Une mise en production réelle doit être validée par un professionnel du droit compétent.
