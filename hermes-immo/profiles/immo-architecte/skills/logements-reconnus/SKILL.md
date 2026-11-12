---
name: logements-reconnus
description: "Établir, lot par lot, si un logement est légalement reconnu"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
---
# Logements reconnus

## Quand l'utiliser

Avant toute option d'achat, division, revente par lots ou calcul locatif par
unité ; dès qu'une annonce, un cahier des charges ou un vendeur annonce un
nombre de logements.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'adresse ou la référence cadastrale (requis) | région, commune, pièces à chercher | la parcelle se retrouve sur le portail cadastral |
| Permis, renseignements urbanistiques (requis pour conclure) | seules ces pièces prouvent | la pièce s'ouvre et se date ; sans elle, le lot sort « inconnu » |
| Un compte sur un portail cadastral ou d'urbanisme (optionnel) | certaines données exigent une connexion | la connexion aboutit ; sinon, demande la pièce |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : la région désigne le code et les pièces probantes.
  `detect` (défaut) : déduis la région de l'adresse du bien, dis-la, fais-la
  confirmer. Hors de la liste configurée : signale-le avant de continuer.
- `immo.fiche_investisseur` : quelles stratégies exigent des logements
  reconnus ; illisible → donne le statut des lots sans conclure sur la
  stratégie.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Établis la région et la commune** : la règle et les pièces probantes en
   dépendent.
2. **Liste les lots annoncés** et la source de cette annonce (annonce, cahier
   des charges, bail, vendeur). C'est une affirmation, pas une preuve.
3. **Cherche les pièces, par force probante** :
   - le **permis** qui autorise ce nombre de logements (date, référence,
     objet exact) ;
   - les **renseignements urbanistiques** délivrés par la commune (le notaire
     les demande avant la vente ; en vente publique, ils sont souvent annexés
     au cahier des charges) ;
   - l'**inscription cadastrale** en logements distincts.
4. **Lis chaque pièce mot pour mot** : un permis pour « deux logements » ne
   couvre pas le troisième aménagé dans les combles ; un permis de
   transformation ne couvre pas forcément le changement de nombre d'unités.
5. **Vérifie la date** : une division antérieure à certaines dates peut
   bénéficier d'une présomption ou d'une prescription selon le droit régional
   — c'est une question de droit : consulte `immo-avocat`, texte en vigueur à
   l'appui.
6. **Classe chaque lot** : reconnu (pièce citée), non reconnu (pièce qui le
   dit, ou permis qui couvre moins de lots), inconnu (aucune pièce).
7. **Dis la conséquence** pour les stratégies de sa fiche : un lot non reconnu
   rend impossible une stratégie qui exige des logements reconnus ; signale-le
   à `immo-associe`.

## Ce que tu sors

Un tableau : lot, statut (reconnu / non reconnu / inconnu), pièce et date,
citation utile, conséquence. Puis la pièce manquante la plus utile et qui la
détient.

## Pièges

- Compteurs séparés, sonnettes, boîtes aux lettres, baux en cours : ils
  prouvent ce que le vendeur loue, pas ce que la commune a autorisé.
- Le notaire ne garantit en général pas le nombre de logements : une clause
  « sans garantie » le dit en toutes lettres.
- « Inconnu » arrondi à « reconnu » parce que l'immeuble « a toujours été
  loué comme ça ».
- Un cadastre à jour n'est pas un permis : il enregistre, il n'autorise pas.
