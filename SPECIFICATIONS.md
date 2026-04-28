# Cahier des Charges — Pac-man

**Version :** 1.0
**Date :** 2026-04-28
**Auteur(s) :** kebertra & gtourdia
**Statut :** Brouillon

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

Ce projet est realise dans le cadre de l'enseignement offert par le tronc commun 42.


### 1.2 Objectifs

- **Interface Graphique Polie :** Fournir une interface graphique complète utilisant une bibliothèque simple (type MLX), incluant un menu principal, la vue de jeu et la gestion du Game Over.
- **Menu Principal Interactif :** Implémenter une page d'accueil permettant de lancer une partie, consulter le Top 10 des scores, lire les instructions et quitter l'application.
- **Fenêtre de Jeu Dynamique :** Afficher en temps réel le score, le nombre de vies restantes (départ à 3), le niveau actuel et le temps restant.
- **Système de High-score Persistant :** Développer un système robuste de sauvegarde/chargement des 10 meilleurs scores (noms de 10 caractères max et scores entiers) dans un fichier JSON.
- **Cheat Mode :** Intégrer des fonctionnalités de triche pour faciliter l'évaluation (invincibilité, gel des fantômes, saut de niveau, etc.).
- **Progression et Niveaux :** Gérer au moins 10 niveaux successifs avec une limite de temps par niveau (ex: 90s).

<br>

- **Configuration par Fichier externe :** Permettre le paramétrage du jeu (vies, points, vitesse) via un fichier JSON supportant les commentaires (lignes débutant par #) passé en argument au lancement.  - **Intégration de Labyrinthe Tierce :** Adapter le moteur de jeu pour utiliser exclusivement le package 'A-Maze-ing' assigné pour la génération des couloirs, sans modification de son code source.  
- **Robustesse et Gestion d'Erreurs :** Garantir l'absence totale de crash ou de traceback Python, notamment lors de la lecture de fichiers de configuration corrompus ou manquants.

<br>

- **Qualité de Code :** Adhérer aux standards Python 3.10+, respecter la norme flake8 et valider l'intégralité du code avec des type hints via mypy.
- **Déploiement Public :** Livrer une version installable et fonctionnelle du jeu sur une plateforme de gaming publique (Steam ou Itch.io) en mode privé/unlisted.
- **Documentation et Traçabilité :** Produire un README.md complet et un dossier de gestion de projet contenant les preuves de suivi (Timeline, Kanban, analyse de risques). 



### 1.3 Vision

> "Permettre à [utilisateur] de [faire quoi] en [gain mesurable]."

> "Permettre a l'utilisateur de lancer une game de pac-man en 1 clic"

> "Permettre a l'utilisateur d enregistrer son score dans un leader board"

> "Permettre a l evaluateur de modifier les parametres du jeu sur un appui de touche"

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
- [❌] Fichier de configuration JSON(5) supportant les commentaires
- [❌] Jeu délployé sur un marketplace (ex: Itch.io)
- [❌] Menu d'accueil affichant le leaderboard
- [❌] Êcran Win/Lose
- [❌] Écran pour enregistrer son score dans le leaderboard
- [❌] Système d'enregistrement/récupération de scores
- [❌] God mode (code Konami: ↑↑↓↓←→←→ab)
- [❌] Mode "Pause"

**Should have (important)**
- [ ] ...

**Could have (souhaitable)**
- [❌] Effets visuels et sonores lors des power-ups, god mode et mort
- [ ] ...

**Won't have (hors périmètre) / Outstanding**
- [❌] Possibilité d'entrer l'IP d'un backend dans le menu d'accueil pour enregistrer et récupérer les scores
- [❌] Easter eggs
- ...

### 2.2 User Stories

| ID | Rôle | Action souhaitée | Bénéfice | Priorité |
|----|------|-----------------|----------|----------|
| US-01 | Utilisateur | Appuie sur SPACE depuis le menu d'accueil | Lance le jeu | Must |
| US-01 | Utilisateur | Appuie sur ESCAPE in-game | Met en pause le jeu | Must |
| US-01 | Utilisateur | Appuie sur ESCAPE in-game | Met en pause le jeu | Must |
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