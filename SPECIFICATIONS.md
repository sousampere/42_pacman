# Cahier des Charges — [Nom du Projet]

**Version :** 1.0
**Date :** JJ/MM/AAAA
**Auteur(s) :** [Nom]
**Statut :** Brouillon / En révision / Validé

---

## Sommaire

1. [Présentation du projet](#1-présentation-du-projet)
2. [Périmètre fonctionnel](#2-périmètre-fonctionnel)
3. [Exigences techniques](#3-exigences-techniques)
4. [Architecture et intégrations](#4-architecture-et-intégrations)
5. [Livrables et planning](#5-livrables-et-planning)
6. [Contraintes et hypothèses](#6-contraintes-et-hypothèses)
7. [Critères de recette](#7-critères-de-recette)
8. [Annexes](#8-annexes)

---

## 1. Présentation du projet

### 1.1 Contexte

Décrivez le contexte dans lequel s'inscrit le projet. Quel problème ou besoin a déclenché ce projet ?

> Exemple : L'entreprise X gère actuellement ses commandes via des fichiers Excel partagés, ce qui génère des erreurs et des pertes de temps.

### 1.2 Objectifs

- **Objectif 1 :** ...
- **Objectif 2 :** ...
- **Objectif 3 :** ...

### 1.3 Vision

> "Permettre à [utilisateur] de [faire quoi] en [gain mesurable]."

### 1.4 Parties prenantes

| Rôle | Nom | Responsabilité |
|------|-----|----------------|
| Commanditaire | | Validation finale |
| Chef de projet | | Coordination |
| Développeur(s) | | Réalisation |
| Utilisateurs finaux | | Tests et feedback |

---

## 2. Périmètre fonctionnel

### 2.1 Fonctionnalités — Méthode MoSCoW

**Must have (indispensable)**
- [ ] ...
- [ ] ...

**Should have (important)**
- [ ] ...

**Could have (souhaitable)**
- [ ] ...

**Won't have (hors périmètre)**
- ...

### 2.2 User Stories

| ID | Rôle | Action souhaitée | Bénéfice | Priorité |
|----|------|-----------------|----------|----------|
| US-01 | Utilisateur | Se connecter avec email/mdp | Accéder à mon espace | Must |
| US-02 | Admin | Créer/modifier des utilisateurs | Gérer les accès | Must |
| US-03 | | | | |

### 2.3 Cas d'usage principaux

**Cas d'usage 1 : [Titre]**

1. L'utilisateur fait...
2. Le système répond...
3. L'utilisateur confirme...

*Cas d'erreur :* ...

---

## 3. Exigences techniques

### 3.1 Stack technologique

| Composant | Technologie | Justification |
|-----------|------------|---------------|
| Frontend | | |
| Backend | | |
| Base de données | | |
| Hébergement | | |
| CI/CD | | |

### 3.2 Performances

| Critère | Valeur cible |
|---------|-------------|
| Temps de réponse moyen | < X ms |
| Disponibilité (uptime) | > 99,X % |
| Charge simultanée supportée | X utilisateurs |
| Temps de chargement page | < X s |

### 3.3 Sécurité

- [ ] Authentification : [JWT / OAuth / SSO / autre]
- [ ] Chiffrement des données en transit (HTTPS) et au repos
- [ ] Conformité RGPD : [Oui / Non — préciser]
- [ ] Gestion des rôles et permissions
- [ ] Journalisation des actions (logs)

### 3.4 Compatibilité

| Type | Cible |
|------|-------|
| Navigateurs | Chrome, Firefox, Safari, Edge (N-1) |
| Appareils | Desktop, tablette, mobile |
| OS serveur | Linux Ubuntu XX |
| Résolution minimale | 1280x720 |

---

## 4. Architecture et intégrations

### 4.1 Schéma d'architecture

```
[Frontend] <-> [API REST / GraphQL] <-> [Base de données]
                        |
                [Services tiers]
```

> Remplacer par un lien vers un schéma Figma, Draw.io ou une image.

### 4.2 Intégrations externes

| Service | Usage | Type d'intégration |
|---------|-------|-------------------|
| Stripe | Paiement | API REST |
| SendGrid | Emails transactionnels | SDK |
| | | |

### 4.3 Modèle de données (ébauche)

- **Entité 1** : attribut1, attribut2, ...
- **Entité 2** : attribut1, attribut2, ...
- Relations : Entité1 -> Entité2 (1-N), ...

---

## 5. Livrables et planning

### 5.1 Livrables

| Livrable | Description | Format | Date cible |
|----------|-------------|--------|-----------|
| Maquettes | Ecrans principaux | Figma | |
| MVP | Fonctionnalités Must | Déployé | |
| V1 complète | Toutes fonctionnalités | Déployé | |
| Documentation technique | | Markdown / Wiki | |
| Documentation utilisateur | | PDF | |

### 5.2 Planning macro

```
Phase 1 - Conception      [JJ/MM -> JJ/MM]
Phase 2 - Développement   [JJ/MM -> JJ/MM]
Phase 3 - Tests           [JJ/MM -> JJ/MM]
Phase 4 - Déploiement     [JJ/MM -> JJ/MM]
Phase 5 - Maintenance     [à partir du JJ/MM]
```

---

## 6. Contraintes et hypothèses

### 6.1 Contraintes

| Type | Description |
|------|-------------|
| Budget | X EUR maximum |
| Délai | Livraison impérative le JJ/MM/AAAA |
| Ressources | Equipe de X développeurs |
| Technique | Doit s'intégrer avec le système Y |
| Légale | Conformité RGPD obligatoire |

### 6.2 Hypothèses

- On suppose que l'API partenaire X est stable et documentée.
- On suppose que les utilisateurs disposent d'un navigateur moderne.
- ...

---

## 7. Critères de recette

### 7.1 Processus de validation

1. Recette fonctionnelle par le commanditaire
2. Tests de performance
3. Audit de sécurité (si requis)
4. Validation finale et mise en production

### 7.2 Critères d'acceptation

| Fonctionnalité | Critère de succès |
|---------------|------------------|
| Connexion | Réussie en < 2 s, erreurs affichées |
| | |

### 7.3 Tests attendus

- [ ] Tests unitaires (couverture > X %)
- [ ] Tests d'intégration
- [ ] Tests end-to-end (scénarios critiques)
- [ ] Tests de charge
- [ ] Tests de sécurité (OWASP)

---

## 8. Annexes

### 8.1 Glossaire

| Terme | Définition |
|-------|-----------|
| MVP | Minimum Viable Product |
| CDC | Cahier des charges |
| MoSCoW | Must / Should / Could / Won't |

### 8.2 Documents de référence

- [Lien vers les maquettes]
- [Lien vers la documentation existante]

### 8.3 Historique des révisions

| Version | Date | Auteur | Modifications |
|---------|------|--------|--------------|
| 1.0 | JJ/MM/AAAA | | Création initiale |