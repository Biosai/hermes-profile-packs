---
name: bibliotheque-ouvrages
description: "Tenir la bibliothèque d'ouvrages et ses prix datés"
metadata:
  hermes:
    config:
      - key: immo.bibliotheque_ouvrages
        description: "Chemin de la bibliothèque d'ouvrages, ou none"
        default: "none"
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Bibliothèque d'ouvrages

## Quand l'utiliser

Quand un poste de chiffrage n'a pas de ligne ; quand un prix a plus de
quelques mois ; quand l'investisseur donne un chantier réel ou un prix de
revient ; en revue périodique, si une tâche planifiée la porte.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Un emplacement pour la bibliothèque (requis pour la tenir) | une ligne doit survivre à la session | `immo.bibliotheque_ouvrages` désigne un chemin lisible et inscriptible |
| Des prix relevés, sourcés et datés (requis) | une ligne sans date ne sert pas | chaque prix a sa source |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.bibliotheque_ouvrages` : un chemin → la bibliothèque à lire et à
  mettre à jour ; `none` (défaut) → il n'y en a pas : propose d'en ouvrir une
  au chemin qu'il choisit ; d'ici là, les lignes restent dans la réponse,
  marquées « non conservées ».
- `immo.fiche_investisseur` : son coût horaire et ses prix de revient, s'il
  fait les travaux.
- `immo.juridictions` : l'indice de réindexation (en Belgique, l'indice ABEX ;
  en France, les index du bâtiment publiés). `detect` (défaut) : pays des
  chantiers.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Une ligne par ouvrage**, unité claire (m², ml, pièce, forfait) :
   description, composition (matériaux et quantités par unité), temps de pose
   par unité, sources.
2. **Matériaux** : prix fournisseur relevé, avec la source et la date ; prix
   hors TVA ; pertes et chutes en pourcentage séparé.
3. **Main-d'œuvre** : temps de pose × coût horaire. Si la fiche de
   l'investisseur donne son coût horaire réel, c'est son prix de revient ;
   sinon, un coût horaire d'entreprise, marqué comme estimation.
4. **Indexation** : chaque prix porte sa date ; réindexe-le sur un indice
   public du coût de la construction (en Belgique, l'indice ABEX), en disant
   l'indice et la date utilisés.
5. **Chantier réel** : quand l'investisseur donne un coût réel (facture,
   décompte), enregistre-le avec sa source ; il prime sur la ligne qu'il
   couvre, et sert à recaler la ligne.
6. **Statut de chaque ligne** : « chantier réel », « prix de revient de sa
   fiche », « bibliothèque, indicatif ».
7. **Contrôle** : une ligne sans source ou sans date ne sert pas au chiffrage
   tant qu'elle n'est pas complétée.

## Ce que tu sors

La ligne d'ouvrage complète (composition, temps, prix daté, indice, statut),
ou la liste des lignes à rafraîchir, avec leur âge.

## Pièges

- Recopier un prix moyen trouvé en ligne : c'est un prix vendeur, pas une
  ligne d'ouvrage.
- Mélanger hors TVA et TVA comprise dans une même ligne.
- Laisser une ligne vieillir sans réindexation : un chiffre sans date de relevé
  est un chiffre faux en puissance.
- Réclamer des chantiers réels à l'investisseur : ils améliorent la base, ils
  ne la conditionnent pas.
