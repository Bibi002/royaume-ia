# Exemples

Ces fichiers illustrent la **démarche** du projet sur des cas **génériques et autonomes**. Ils ne contiennent **aucun code produit**, aucune donnée réelle, aucun secret.

| Fichier | Démontre |
|---|---|
| [`minimal_agent.py`](minimal_agent.py) | Une boucle d'agent LLM local à *function calling* avec **validation des arguments** — le mécanisme qui empêche l'agent d'inventer des valeurs. Outil d'exemple anodin (conversion de température). |
| [`backup_strategy.sh`](backup_strategy.sh) | Le squelette d'une **stratégie de sauvegarde différenciée** : on sauvegarde souvent ce qui change (base + travail), et séparément ce qui est lourd et statique. Chemins en placeholders. |

## `minimal_agent.py`

Prérequis : un serveur [Ollama](https://ollama.com) local, et un modèle supportant les outils :

```bash
ollama pull qwen3:4b-instruct
python3 examples/minimal_agent.py
```

Aucune dépendance externe (bibliothèque standard Python uniquement).

## Portée

Ces exemples sont réutilisables librement (voir [`../LICENSE`](../LICENSE)). Les agents de production, eux, sont propriétaires et ne figurent pas dans ce dépôt.
