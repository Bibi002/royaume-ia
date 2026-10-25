# Politique de sécurité

## Périmètre

Ce dépôt ne contient **ni code de production, ni secret, ni donnée réelle**. Il décrit une architecture de référence et fournit des exemples pédagogiques. Les éléments sensibles (configuration, identifiants, données) vivent hors de ce dépôt et ne sont pas publiés.

## Signaler une vulnérabilité

Si vous identifiez un problème de sécurité dans les **exemples de code** de ce dépôt, merci de le signaler de façon responsable :

- ouvrez une *issue* en décrivant le problème **sans publier d'exploit fonctionnel**, ou
- contactez l'auteur en privé.

> *Divulgation responsable* : laissez un délai raisonnable pour un correctif avant toute publication. Aucune récompense financière n'est prévue (projet personnel).

## Hors périmètre

- Les infrastructures réelles décrites de façon générale dans la documentation ne sont pas des cibles : aucune adresse, aucun hôte réel n'est publié.
- Les exemples supposent un environnement local maîtrisé (serveur LLM sur `127.0.0.1`) ; ne les exposez pas tels quels sur un réseau non maîtrisé.

## Bonnes pratiques appliquées dans ce dépôt

- Secrets exclus par `.gitignore` et jamais versionnés.
- Aucune donnée personnelle ni de santé.
- Architecture présentée comme *patron de référence*, pas comme carte d'un réseau en production.
