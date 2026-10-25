# Feuille de route

## Fait ✅

- [x] Cloisonnement réseau par domaine de confiance (VLANs, deny inter-VLAN), **isolation prouvée par test**
- [x] Moteur d'agent local à *function calling* avec validation des arguments
- [x] Agent métier en production : génération de documents, mémoire, archivage, recherche
- [x] Sauvegardes automatiques différenciées, chiffrées, **vérifiées restaurables**
- [x] Durcissement : mises à jour de sécurité, réduction de la surface d'attaque, garde-fous de stockage

## En cours 🚧

- [ ] Validation humaine obligatoire pour l'envoi de communications (fonction irréversible, traitée avec soin)
- [ ] Reconstruction de l'agent cyber sur le même socle

## Prévu 🗺️

- [ ] Intégrations tierces via **API officielles** (jamais par scraping fragile)
- [ ] Conscience temporelle de l'agent (briefing daté : fraîcheur des sources)
- [ ] Harnais d'évaluation rejouable (tests de non-régression des prompts/outils)
- [ ] Montée en charge matérielle (RAM puis GPU) → bascule transparente grâce au format GGUF
- [ ] Interfaces dédiées (bureau / mobile) sur briques open-source, une fois le socle éprouvé

## Principes qui guident la suite

- **Fiabilité avant fonctionnalités.** On ajoute une capacité seulement quand la précédente est irréprochable et testée.
- **Rien d'irréversible sans validation humaine.**
- **Chaque brique testée avant la suivante.**
