---
name: fournitures-quantites-prix
description: "Passer des métrés aux fournitures, quantités et prix"
metadata:
  hermes:
    config:
      - key: immo.bibliotheque_ouvrages
        description: "Chemin de la bibliothèque d'ouvrages, ou none"
        default: "none"
---
# Fournitures, quantités et prix

## Quand l'utiliser

Quand un chantier se prépare ; quand une ligne d'ouvrage doit être mise à
jour avec des prix actuels ; quand l'investisseur demande une liste d'achat
ou une comparaison de fournisseurs.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Les métrés sourcés (requis) | les quantités en partent | chaque quantité nomme sa source |
| L'accès aux prix des fournisseurs (requis) | prix relevés et datés | une page ou un devis daté s'ouvre |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.bibliotheque_ouvrages` : un chemin → mets à jour les lignes avec les
  prix relevés ; `none` (défaut) → les prix restent dans la réponse, datés.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Pars des métrés** (skill `lecture-plans-metres` de `immo-architecte`, ou
   relevé sur place) : chaque quantité porte sa source.
2. **Décompose chaque ouvrage en fournitures** : matériau principal, fixations,
   accessoires, consommables. Unité de vente du fournisseur (rouleau, palette,
   paquet), pas seulement unité d'ouvrage.
3. **Ajoute les pertes et chutes** par type de matériau, en ligne séparée.
4. **Relève les prix** chez au moins deux fournisseurs quand c'est possible :
   référence produit, prix hors TVA, unité, conditionnement, délai, date du
   relevé, source (lien ou devis).
5. **Arrondis à l'unité de vente** et calcule le coût réel commandé.
6. **Compare** : écart entre fournisseurs, produits équivalents, délais.
7. **Prépare la commande en brouillon** : fournisseur, références, quantités,
   prix relevé, livraison. Elle ne se valide jamais : c'est l'investisseur qui
   la passe.
8. **Mets à jour la bibliothèque**, si `immo.bibliotheque_ouvrages` en
   désigne une (skill `bibliotheque-ouvrages`), avec les prix relevés et leur
   date.

## Ce que tu sors

Une liste de fournitures : ouvrage, article, référence, quantité nette,
pertes, quantité commandée, prix unitaire, total, fournisseur, date du relevé.
Le comparatif fournisseurs en pied, et la commande en brouillon si demandée.

## Pièges

- Un prix sans date ni source : il ne s'utilise pas.
- Oublier l'arrondi au conditionnement : la commande coûte plus que le métré.
- Valider une commande parce qu'il a dit « vas-y » : la commande reste un
  brouillon, il la passe lui-même.
- Comparer des produits non équivalents (épaisseur, classe, certification).
