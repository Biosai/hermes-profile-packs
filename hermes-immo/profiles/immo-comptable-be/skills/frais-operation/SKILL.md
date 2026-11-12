---
name: frais-operation
description: "Lister et chiffrer tous les frais d'une opération"
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
# Frais de l'opération

## Quand l'utiliser

Pour tout prix plafond, tout calcul de marge ou de rendement, et pour
contrôler un tableau de rentabilité venu d'ailleurs.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'adresse, le prix et le type de vente (requis) | les frais en dépendent | région établie, prix sourcé |
| Le cahier des charges (requis en vente publique) | frais d'adjudication | le cahier complet s'ouvre |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : droits, taxes locales et barèmes de la région.
  `detect` (défaut) : déduis la région de l'adresse du bien, dis-la, fais-la
  confirmer.
- `immo.fiche_investisseur` : si l'impôt entre dans les frais de sortie, selon
  sa règle de présentation.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Frais d'entrée** : droits d'enregistrement ou TVA (skills dédiés), frais
   d'acte et honoraires du notaire (barème légal à lire, débours), frais de
   vente publique fixés par le cahier des charges, frais d'hypothèque et de
   dossier de crédit, frais de recherche ou de commission éventuels.
2. **Frais de portage** : intérêts, précompte immobilier ou taxe foncière,
   assurances, charges de copropriété, énergie et entretien d'un bien vide,
   taxes communales sur les immeubles inoccupés, durée prise du scénario.
3. **Frais de sortie** : commission d'agence ou frais de vente publique,
   certificats et attestations exigés à la vente, mainlevée d'hypothèque,
   frais de division (acte de base, géomètre), impôt selon la règle de sa fiche.
4. **Source chaque frais** : barème lu (avec sa date), devis, cahier des
   charges cité, ou hypothèse marquée comme telle.
5. **Calcule les frais qui dépendent du prix** comme des fonctions du prix,
   pas comme des montants fixes : ils bougent avec l'enchère.
6. **Montage mixte** : les frais d'acquisition portent sur ce qui est acheté,
   pas sur le prix total d'un montage où une partie passe sous option.

## Ce que tu sors

Un tableau en trois blocs (entrée, portage, sortie) : poste, base de calcul,
montant en fourchette, source et date. Le total en pourcentage du prix, pour
contrôle, jamais comme règle de calcul.

## Pièges

- Un pourcentage forfaitaire de « frais de notaire » : il cache des postes qui
  ne suivent pas la même base.
- Oublier le portage d'un bien vide pendant un permis ou des travaux.
- Les frais d'adjudication d'une vente publique diffèrent d'une vente de gré
  à gré : lis le cahier des charges.
- Compter deux fois un même poste dans les frais et dans les travaux.
