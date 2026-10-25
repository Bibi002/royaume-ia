# Décisions d'architecture (ADR)

> Chaque décision structurante est consignée ici : **contexte**, **décision**, **conséquences**. C'est ce qui permet de ne pas perdre le fil, et de défendre ses choix.

---

## ADR-001 — Inférence 100 % locale pour les données sensibles

**Contexte.** Le prototype initial envoyait chaque raisonnement (avec des données réglementées) vers une API cloud hors UE.
**Décision.** Le moteur d'inférence tourne en local, dans le domaine sensible ; aucune donnée réglementée ne sort.
**Conséquences.** Conformité RGPD tenable (pas de transfert hors UE), argument commercial fort (« les données ne quittent pas votre machine »). Contrepartie : inférence plus lente sur CPU → choix de petits modèles optimisés, prêt pour un GPU.

## ADR-002 — Cloisonnement par domaine de confiance (réseau)

**Contexte.** Agent offensif et données sensibles cohabitaient sur le même segment, séparés par une simple condition logicielle.
**Décision.** Segments VLAN dédiés ; l'isolation est réseau, en liste blanche, deny inter-VLAN par défaut.
**Conséquences.** Une compromission d'un domaine n'atteint pas l'autre. Isolation **vérifiable** (test de non-atteignabilité). Contrepartie : plus de configuration réseau, migrations de services à orchestrer.

## ADR-003 — Humain aux commandes pour les actions irréversibles / à responsabilité

**Contexte.** Un agent qui agit seul sur des documents légaux ou des envois externes engage la responsabilité de l'utilisateur.
**Décision.** L'agent **prépare** (brouillons, trames) ; l'humain **valide** le jugement métier et tout envoi. Pas de diagnostic automatique.
**Conséquences.** Gain de temps massif sans transfert de responsabilité au logiciel ; évite le statut de dispositif médical. Contrepartie : une étape de validation humaine subsiste (voulue).

## ADR-004 — *Function calling* structuré plutôt que parsing de texte

**Contexte.** L'ancien système extrayait les actions d'une réponse texte → hallucinations (montants, identifiants, chemins inventés).
**Décision.** Appels d'outils à **schéma JSON validé** ; un argument manquant ou mal typé est rejeté, jamais inventé.
**Conséquences.** Fiabilité déterministe sur les champs critiques. Le fichier livré est **le fichier réellement produit** par l'outil, pas une phrase du modèle. Si un outil échoue, l'agent le dit.

## ADR-005 — Pas d'agent offensif autonome

**Contexte.** Tentation d'un agent qui exécute des attaques sur simple instruction.
**Décision.** L'agent assiste et explique ; l'humain lance les outils offensifs, dans un périmètre **autorisé** (scope, règles d'engagement), sur un labo isolé.
**Conséquences.** Conforme au cadre légal ; cohérent avec le métier (une mission se cadre et s'autorise). Supprime un risque juridique majeur.

## ADR-006 — Pas d'auto-modification du code en production

**Contexte.** Idée d'agents qui réécrivent leur propre code pour « évoluer ».
**Décision.** L'amélioration passe par des tests qui doivent réussir, du versioning et un rollback. Pas de code qui se réécrit seul.
**Conséquences.** Système auditable et stable, indispensable sur une machine hébergeant des données sensibles. On garde le bon noyau (mémoire, évaluation) sous une forme contrôlée.

## ADR-007 — Choix du modèle : petit modèle *Instruct*, licence permissive

**Contexte.** Besoin d'un modèle rapide sur CPU, multilingue, et **commercialement réutilisable**.
**Décision.** Famille de petits modèles *Instruct* sous licence permissive (Apache-2.0), servie en GGUF ; variante *Instruct* (sans « réflexion ») par défaut.
**Conséquences.** Latence acceptable sur CPU (la variante « à réflexion » était plusieurs fois plus lente), français natif, aucun verrou de licence pour une commercialisation future. Bascule GPU transparente.

## ADR-008 — Secrets hors du dépôt, sécurité par l'architecture

**Contexte.** Risque de fuite de secrets et de dépendance à la « bonne volonté » du modèle.
**Décision.** Secrets chargés depuis l'environnement, exclus par `.gitignore`. Confidentialité assurée par isolation réseau + liste blanche d'accès.
**Conséquences.** Pas de secret versionné ; la sécurité ne repose pas sur une consigne de prompt contournable.
