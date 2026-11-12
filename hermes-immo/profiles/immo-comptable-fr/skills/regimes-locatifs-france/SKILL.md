---
name: regimes-locatifs-france
description: "Comparer les régimes locatifs français et les structures"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Régimes locatifs en France

## Quand l'utiliser

Quand un bien français est destiné à la location, ou quand l'investisseur se
demande par quelle structure détenir un bien français.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'adresse du bien et le type de location (requis) | autorisations communales, régime | commune connue |
| L'accès à Légifrance et au BOFiP (requis, gratuit) | aucun chiffre de mémoire | le texte s'ouvre ; sinon À VÉRIFIER |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : sans FR, signale que la France n'est pas configurée et
  ne propose rien de français ; une question qu'il pose lui-même reçoit sa
  réponse. `detect` (défaut) : FR si le bien est en France, confirmé.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Annonce l'état des sources** : sans texte lu, **À VÉRIFIER**.
2. **Qualifie la location** : nue (revenus fonciers), meublée de longue
   durée, meublé de tourisme (courte durée), location à des entreprises. Les
   règles du meublé de tourisme changent par réformes successives : lis la version
   en vigueur.
3. **Autorisations** : changement d'usage, enregistrement et numéro de
   déclaration, plafonds de nuitées dans certaines communes — à vérifier avec
   `immo-architecte` pour l'urbanisme et la commune.
4. **Interdictions de louer** par classe énergétique (DPE) : calendrier à lire
   sur Légifrance, à croiser avec `immo-conducteur-travaux`.
5. **Structure** : société belge, société civile française, société par
   actions française, détention directe. Pour chacune : impôt sur les
   résultats, amortissement possible ou non, sortie (plus-value, droits sur
   cession des parts), obligations. Présente-les en tableau, sans trancher.
6. **Moitié belge** : comment la Belgique traite les revenus selon la
   structure ; consulte `immo-comptable-be`.
7. **Cash-flow** : les chiffres de loyer et de charges viennent de
   `immo-associe` ; toi, tu ajoutes l'impôt par structure, en fourchette.

## Ce que tu sors

Un tableau régime × structure : impôt, amortissement, autorisations,
obligations, sortie, effet en fourchette, texte et version (ou À VÉRIFIER).
Puis l'avis belge cité et la question pour un expert-comptable français.

## Pièges

- Choisir la structure après l'achat : la changer ensuite coûte des droits.
- Calculer une rentabilité de courte durée sans avoir vérifié qu'elle est
  autorisée dans la commune.
- Ignorer un calendrier d'interdiction de louer qui tombe pendant la durée de
  détention.
- Présenter une structure comme « la meilleure » : c'est l'arbitrage de
  l'investisseur et de son expert-comptable.
