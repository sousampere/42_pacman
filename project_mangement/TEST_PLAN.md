# TEST_PLAN — Plan de recette
*Projet Pacman — Kebertra + gtourdia*

---

## Conventions

| Symbole | Signification |
|---|---|
| ☐ | Non testé |
| ✅ | Testé et validé |
| ⚠️ | Testé — comportement anormal, bug ouvert |
| ❌ | Testé — échec bloquant |

**Environnement de test** : Linux, Python 3.10+, `make install` effectué, package A-Maze-ing installé.

---

## 1. Lancement et configuration

### 1.1 Lancement nominal

| ID | Scénario | Commande | Résultat attendu | Statut |
|---|---|---|---|---|
| L01 | Lancement normal | `python3 pac-man.py config.json` | Jeu démarre, menu principal affiché | ☐ |
| L02 | Argument manquant | `python3 pac-man.py` | Message d'erreur clair, pas de traceback | ☐ |
| L03 | Argument en trop | `python3 pac-man.py a.json b.json` | Message d'erreur clair, pas de traceback | ☐ |
| L04 | Fichier inexistant | `python3 pac-man.py absent.json` | Message d'erreur clair, pas de traceback | ☐ |
| L05 | Fichier non JSON | `python3 pac-man.py README.md` | Message d'erreur clair, pas de traceback | ☐ |

### 1.2 Robustesse de la configuration

| ID | Scénario | Config injectée | Résultat attendu | Statut |
|---|---|---|---|---|
| C01 | Clé manquante (`lives`) | Supprimer `lives` du JSON | Clampe sur défaut (3), log message, jeu démarre | ☐ |
| C02 | Valeur négative (`lives: -1`) | `"lives": -1` | Clampe sur défaut (3), log message, jeu démarre | ☐ |
| C03 | Valeur trop élevée (`lives: 999`) | `"lives": 999` | Accepté ou clampe sur max, jeu démarre | ☐ |
| C04 | Mauvais type (`lives: "trois"`) | `"lives": "trois"` | Clampe sur défaut, log message, jeu démarre | ☐ |
| C05 | Clé inconnue | Ajouter `"foo": "bar"` | Clé ignorée, jeu démarre normalement | ☐ |
| C06 | JSON vide | `{}` | Tous les défauts appliqués, jeu démarre | ☐ |
| C07 | Commentaires `#` dans le JSON | Ligne `# commentaire` avant une clé | Ignoré, JSON parsé correctement | ☐ |
| C08 | Points négatifs (`points_per_pacgum: -5`) | `"points_per_pacgum": -5` | Clampe sur 0 ou défaut, log message | ☐ |
| C09 | Seed invalide (`seed: "abc"`) | `"seed": "abc"` | Clampe sur défaut (42), log message | ☐ |
| C10 | Timer à 0 (`level_max_time: 0`) | `"level_max_time": 0` | Clampe sur défaut ou min, log message | ☐ |

---

## 2. Génération de labyrinthe

| ID | Scénario | Résultat attendu | Statut |
|---|---|---|---|
| M01 | Niveau 1 avec seed fixe (42) | Labyrinthe identique à chaque lancement | ☐ |
| M02 | Niveaux suivants avec seed aléatoire | Labyrinthes différents à chaque lancement | ☐ |
| M03 | Labyrinthe avec `PERFECT=False` | Corridors avec boucles, compatible Pac-Man | ☐ |
| M04 | Dimensions configurées (width, height) | Labyrinthe respecte les dimensions | ☐ |
| M05 | Package A-Maze-ing échoue (simuler exception) | Message d'erreur clair, pas de traceback | ☐ |

---

## 3. Joueur

| ID | Scénario | Résultat attendu | Statut |
|---|---|---|---|
| P01 | Déplacement vers le haut | Pac-Man se déplace, bloqué par les murs | ☐ |
| P02 | Déplacement vers le bas | Idem | ☐ |
| P03 | Déplacement vers la gauche | Idem | ☐ |
| P04 | Déplacement vers la droite | Idem | ☐ |
| P05 | Collision avec un mur | Pac-Man s'arrête, ne traverse pas | ☐ |
| P06 | Position de départ | Pac-Man apparaît au centre du labyrinthe | ☐ |
| P07 | Contact avec un fantôme (non-edible) | Perd une vie, réapparaît au centre | ☐ |
| P08 | Perte de la dernière vie | Game Over déclenché | ☐ |
| P09 | Réapparition après mort | Position centre, fantômes remis en place | ☐ |

---

## 4. Fantômes

| ID | Scénario | Résultat attendu | Statut |
|---|---|---|---|
| G01 | Mouvement autonome | 4 fantômes bougent dans les corridors | ☐ |
| G02 | Fantômes ne traversent pas les murs | Mouvement limité aux corridors | ☐ |
| G03 | Mode edible après super-pacgum | Fantômes changent d'apparence, fuient le joueur | ☐ |
| G04 | Durée du mode edible | Mode edible se termine après le temps configuré | ☐ |
| G05 | Manger un fantôme edible | Fantôme disparaît, score +200, réapparition après délai | ☐ |
| G06 | Réapparition au coin | Fantôme réapparaît dans son coin d'origine après 5–10s | ☐ |
| G07 | Fin du mode edible | Fantômes reprennent leur comportement normal | ☐ |

---

## 5. Pacgums et scoring

| ID | Scénario | Résultat attendu | Statut |
|---|---|---|---|
| S01 | Manger un pacgum | Score +10 (ou valeur config), pacgum disparaît | ☐ |
| S02 | Manger un super-pacgum | Score +50 (ou valeur config), mode edible déclenché | ☐ |
| S03 | Manger un fantôme edible | Score +200 (ou valeur config) | ☐ |
| S04 | Le score ne diminue jamais | Aucune action ne réduit le score | ☐ |
| S05 | Tous les pacgums mangés | Victoire du niveau déclenchée | ☐ |
| S06 | Score conservé entre niveaux | Score du niveau N visible au début du niveau N+1 | ☐ |
| S07 | Vies conservées entre niveaux | Vies restantes conservées | ☐ |

---

## 6. Progression et niveaux

| ID | Scénario | Résultat attendu | Statut |
|---|---|---|---|
| N01 | Compléter un niveau | Passage au niveau suivant | ☐ |
| N02 | 10 niveaux enchaînés | Tous les niveaux jouables sans crash | ☐ |
| N03 | Fin du dernier niveau | Écran de victoire affiché | ☐ |
| N04 | Timer atteint 0 | Comportement défini (game over ou restart) déclenché | ☐ |
| N05 | Timer visible en HUD | Temps restant mis à jour en temps réel | ☐ |

---

## 7. Interface utilisateur

| ID | Scénario | Résultat attendu | Statut |
|---|---|---|---|
| U01 | Menu principal affiché au démarrage | Boutons : Démarrer, Highscores, Instructions, Quitter | ☐ |
| U02 | Bouton Démarrer | Lance une nouvelle partie | ☐ |
| U03 | Bouton Highscores | Affiche le top 10 avec noms et scores | ☐ |
| U04 | Bouton Instructions | Affiche les contrôles et règles | ☐ |
| U05 | Bouton Quitter | Ferme le jeu proprement | ☐ |
| U06 | HUD in-game | Score, vies, niveau, timer visibles pendant la partie | ☐ |
| U07 | Pause (touche définie) | Jeu suspendu, menu pause affiché | ☐ |
| U08 | Reprise depuis le menu pause | Jeu reprend exactement où il s'était arrêté | ☐ |
| U09 | Retour menu principal depuis pause | Jeu abandonné, retour menu | ☐ |
| U10 | Écran Game Over | Score final affiché, saisie nom joueur proposée | ☐ |
| U11 | Écran Victoire | Score final + félicitations, saisie nom joueur | ☐ |
| U12 | Saisie nom joueur (10 car. max) | Nom tronqué ou refusé si > 10 caractères | ☐ |
| U13 | Saisie nom avec caractères spéciaux | Refusé (alphanum + espaces uniquement) | ☐ |

---

## 8. Highscores

| ID | Scénario | Résultat attendu | Statut |
|---|---|---|---|
| H01 | Sauvegarde d'un nouveau score | Score enregistré dans le JSON après la partie | ☐ |
| H02 | Chargement des highscores au démarrage | Top 10 visible dans le menu | ☐ |
| H03 | Score dans le top 10 | Inséré à la bonne position (tri décroissant) | ☐ |
| H04 | Score hors top 10 | Non enregistré ou position 11+ ignorée | ☐ |
| H05 | Fichier highscores absent | Créé automatiquement, pas de crash | ☐ |
| H06 | Fichier highscores corrompu | Réinitialisé proprement avec log, pas de crash | ☐ |
| H07 | 10 scores déjà présents, nouveau meilleur score | Remplace le 10e, liste reste à 10 entrées | ☐ |

---

## 9. Mode triche

| ID | Fonctionnalité | Activation | Résultat attendu | Statut |
|---|---|---|---|---|
| T01 | Invincibilité | Touche dédiée | Fantômes ne peuvent plus tuer le joueur | ☐ |
| T02 | Level skip | Touche dédiée | Passe immédiatement au niveau suivant | ☐ |
| T03 | Freeze fantômes | Touche dédiée | Tous les fantômes s'arrêtent | ☐ |
| T04 | Vies bonus | Touche dédiée | +1 vie ajoutée, visible dans le HUD | ☐ |
| T05 | Vitesse augmentée | Touche dédiée | Pac-Man se déplace plus vite | ☐ |
| T06 | Désactivation des cheats | Re-touche ou toggle | Comportement normal restauré | ☐ |
| T07 | Cheats utilisables en combinaison | Activer T01 + T03 | Les deux effets actifs simultanément | ☐ |

---

## 10. Qualité du code

| ID | Vérification | Commande | Résultat attendu | Statut |
|---|---|---|---|---|
| Q01 | make install | `make install` | Dépendances installées sans erreur | ☐ |
| Q02 | make run | `make run` | Jeu démarre | ☐ |
| Q03 | make lint (flake8) | `make lint` | 0 erreur flake8 | ☐ |
| Q04 | make lint (mypy) | `make lint` | 0 erreur mypy (flags obligatoires) | ☐ |
| Q05 | make clean | `make clean` | `__pycache__`, `.mypy_cache` supprimés | ☐ |
| Q06 | make debug | `make debug` | Jeu démarre en mode debug (pdb) | ☐ |

---

## 11. Déploiement

| ID | Scénario | Résultat attendu | Statut |
|---|---|---|---|
| D01 | Build PyInstaller généré | `make package` ou script dédié | Binaire ou archive produit sans erreur | ☐ |
| D02 | Binaire fonctionnel hors venv | Lancement du build dans env propre | Jeu démarre sans dépendances externes | ☐ |
| D03 | Jeu disponible sur la plateforme | Lien Steam / Itch.io | Téléchargeable et jouable | ☐ |
| D04 | Re-génération du build pendant la soutenance | `make package` relancé | Build reproduit en quelques minutes | ☐ |

---

## Suivi des bugs

> Ajouter une ligne à chaque bug trouvé.

| ID | Date | Description | Sévérité | Assigné | Statut |
|---|---|---|---|---|---|
| BUG-001 | À compléter | | | | |

---

*Dernière mise à jour : 29/04/2026*