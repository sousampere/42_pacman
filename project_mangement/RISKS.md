# RISKS — Analyse des risques
*Projet Pacman — Kebertra + gtourdia*

---

## Matrice des risques

| ID | Risque | Probabilité | Impact | Criticité |
|---|---|---|---|---|
| R01 | Interface du package A-Maze-ing incompatible ou mal documentée | Moyenne | Élevé | 🔴 Critique |
| R02 | Config modifiée pendant la soutenance → crash ou comportement inattendu | Élevée | Élevé | 🔴 Critique |
| R03 | mypy ou flake8 échoue en dernière minute (typage incomplet) | Moyenne | Élevé | 🔴 Critique |
| R04 | Build PyInstaller ne fonctionne pas sur la plateforme cible | Moyenne | Élevé | 🔴 Critique |
| R05 | Retard sur le Core gameplay → MVP pas prêt à mi-parcours | Moyenne | Moyen | 🟠 Élevé |
| R06 | Arcade incompatible avec l'environnement Linux de l'évaluateur | Faible | Élevé | 🟠 Élevé |
| R07 | Mode triche incomplet → points perdus à la peer review | Faible | Moyen | 🟡 Modéré |
| R08 | Mauvaise gestion des erreurs → traceback visible pendant la soutenance | Faible | Élevé | 🟠 Élevé |
| R09 | Un membre de l'équipe indisponible sur une période clé | Faible | Moyen | 🟡 Modéré |
| R10 | Highscores corrompus ou perdus (fichier JSON invalide) | Faible | Faible | 🟢 Faible |

---

## Détail et mitigation

### 🔴 R01 — Package A-Maze-ing incompatible ou mal documentée

**Description** : Le package est produit par un autre groupe d'étudiants. Son interface peut être instable, mal documentée, ou changer entre le moment où on le reçoit et la peer review (le sujet précise qu'il sera réinstallé lors de la revue).

**Mitigation** :
- Lire la documentation du package dès S01, tester toutes les fonctions exposées.
- Écrire `maze_adapter.py` comme une couche d'abstraction complète : si l'interface change, seul l'adaptateur est à modifier.
- Prévoir un fallback : si le générateur lève une exception, afficher un message clair et proposer un labyrinthe de secours codé en dur (pour ne pas bloquer la démo).
- Ne jamais modifier le package (interdit par le sujet).

**Indicateur d'alerte** : L'adaptateur plante lors du premier test en S02.

---

### 🔴 R02 — Config modifiée pendant la soutenance

**Description** : Le sujet indique explicitement que la configuration sera modifiée lors de la défense. Des valeurs invalides, manquantes, ou hors limites seront probablement injectées.

**Mitigation** :
- Implémenter un clamping systématique sur toutes les valeurs (min/max définis et documentés dans le README).
- Tester avec des configs volontairement cassées dès S04 (clé manquante, valeur négative, type incorrect, fichier vide, fichier absent).
- Jamais de traceback exposé : tous les chemins d'erreur retournent un message clair et continuent avec les défauts.
- Documenter chaque clé et sa valeur par défaut dans le README.

**Indicateur d'alerte** : Un `KeyError` ou `ValueError` non intercepté lors des tests de S04.

---

### 🔴 R03 — mypy / flake8 échoue en dernière minute

**Description** : Ignorer le typage et le linting pendant le développement pour aller vite, puis découvrir des dizaines d'erreurs en S08.

**Mitigation** :
- Intégrer `make lint` dans la routine de développement dès S01 — le lancer après chaque session.
- Ajouter les type hints en même temps que le code, pas après.
- Ne pas utiliser `# type: ignore` sans raison documentée.
- Viser mypy strict (`--strict`) optionnellement pour anticiper.

**Indicateur d'alerte** : Plus de 20 erreurs mypy à la fin de S05.

---

### 🔴 R04 — Build PyInstaller défaillant

**Description** : PyInstaller peut échouer à embarquer les assets Arcade (images, sons, polices) ou produire un binaire non fonctionnel sur la plateforme cible.

**Mitigation** :
- Tester le build dès S07, pas seulement en S09.
- Utiliser `--add-data` pour embarquer les assets explicitement.
- Tester le binaire produit dans un environnement propre (sans le venv de dev).
- Prévoir un plan B : distribuer via un zip avec instructions `pip install + python3`.

**Indicateur d'alerte** : Le binaire plante au lancement lors du premier test en S07.

---

### 🟠 R05 — Retard sur le Core gameplay

**Description** : Le moteur de jeu (boucle, collisions, fantômes) est la partie la plus complexe. Un retard ici décale toutes les phases suivantes.

**Mitigation** :
- Livrer un MVP minimal à la fin de S05 (joueur qui se déplace, pacgums collectés, fantômes qui bougent).
- Ne pas sur-ingénier l'IA des fantômes en premier : commencer par un mouvement aléatoire valide, affiner ensuite.
- Points de synchro bi-hebdomadaires pour détecter les retards tôt.

**Indicateur d'alerte** : Pas de labyrinthe rendu à l'écran à la fin de S03.

---

### 🟠 R06 — Incompatibilité Arcade chez l'évaluateur

**Description** : Python Arcade nécessite OpenGL 3.3+. Certaines machines de l'école ou VMs peuvent ne pas le supporter.

**Mitigation** :
- Tester sur une machine différente de celle de développement dès S05.
- Documenter les prérequis système dans le README et dans le build.
- Prévoir le packaging comme solution principale (build standalone qui embarque les dépendances).

**Indicateur d'alerte** : Erreur OpenGL lors du test sur une machine école.

---

### 🟠 R08 — Traceback visible pendant la soutenance

**Description** : Une exception non interceptée lors de la démo (config modifiée, fichier manquant, erreur de générateur) = pénalité directe selon le sujet.

**Mitigation** :
- Convention d'équipe : tout `except` doit logger un message clair ET continuer proprement.
- Passer en revue tous les `except Exception` génériques avant S08.
- Tester les scénarios d'erreur dans le TEST_PLAN.

---

### 🟡 R07 — Mode triche incomplet

**Description** : Le mode triche est explicitement évalué lors de la peer review. Une fonctionnalité manquante ou buguée est visible immédiatement.

**Mitigation** :
- Lister toutes les fonctions triche dès S06 et les tester une par une avec le TEST_PLAN.
- Prévoir une interface claire pour activer chaque fonction (touches dédiées documentées).

---

### 🟡 R09 — Indisponibilité d'un membre

**Description** : Maladie, examens, contraintes personnelles sur une semaine clé.

**Mitigation** :
- Les deux membres connaissent l'ensemble du code (revue croisée systématique).
- Pas de "silo" : aucun module ne doit être compris par un seul membre.
- Prévoir du slack dans le planning (les phases 1 et 2 ont de la marge).

---

### 🟢 R10 — Highscores corrompus

**Description** : Le fichier JSON des highscores peut être absent, vide, ou mal formé.

**Mitigation** :
- `ScoreManager` doit gérer tous ces cas : fichier absent → créer un nouveau, contenu invalide → réinitialiser proprement avec log.
- Tester explicitement ces cas dans les tests unitaires.

---

## Suivi des risques

> Mettre à jour chaque semaine.

| ID | Statut actuel | Évolution | Notes |
|---|---|---|---|
| R01 | 🟡 En surveillance | — | Package reçu, à tester |
| R02 | 🟡 En surveillance | — | |
| R03 | 🟡 En surveillance | — | |
| R04 | 🟡 En surveillance | — | |
| R05 | 🟡 En surveillance | — | |
| R06 | 🟡 En surveillance | — | |
| R07 | 🟡 En surveillance | — | |
| R08 | 🟡 En surveillance | — | |
| R09 | 🟢 Faible | — | |
| R10 | 🟢 Faible | — | |

---

*Dernière mise à jour : 29/04/2026*