---
name: dossier-copropriete
description: "Lire le dossier du syndic et l'acte de base"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Dossier de copropriété

## Quand l'utiliser

Pour tout appartement ou lot en copropriété ; pour tout immeuble que
l'investisseur veut revendre par lots ; avant toute enchère sur un lot.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le dossier du syndic (requis pour un prix plafond) | sans lui, pas de prix plafond | procès-verbaux, fonds, travaux, charges s'ouvrent |
| L'acte de base et le règlement (requis pour une vente par lots) | lots vendables, quotités | l'acte s'ouvre |
| Le cahier des charges ou le compromis | la clause de répartition | la clause se cite |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : quelle règle de répartition lire (Code civil belge ;
  en France, régime de la copropriété, À VÉRIFIER sans texte lu). `detect`
  (défaut) : déduis la région de l'adresse du bien, dis-la, fais-la confirmer.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Existe-t-il un acte de base et un syndic ?** C'est la première question,
   avant tout calcul. Sans acte de base, pas de lot vendable séparément.
2. **Réclame le dossier du syndic** : procès-verbaux des dernières assemblées,
   état du fonds de roulement et du fonds de réserve, travaux votés ou
   envisagés, appels de fonds en cours, charges ordinaires des dernières
   années, litiges en cours, dettes de la copropriété.
3. **Lis les assemblées** : travaux votés (montant, échéancier, quote-part du
   lot), travaux discutés mais non votés, procédures.
4. **Qui paie quoi après la vente** : en Belgique, la loi règle le partage
   entre vendeur et acquéreur des dépenses votées avant la vente (art. 3.94,
   § 2 du Code civil — lire la version en vigueur), mais c'est une règle
   **supplétive** : de gré à gré elle se négocie, en vente publique la clause
   du cahier des charges prime. Lis la clause.
5. **Acte de base et règlement** : parties privatives et communes, quotités,
   affectation des lots, restrictions d'usage (location courte durée,
   activité professionnelle).
6. **Pour une vente par lots** : faut-il établir ou modifier l'acte de base,
   avec quel coût (géomètre, notaire) et quel délai ?
7. **Chiffre** la quote-part des travaux votés, les charges annuelles et le
   fonds de réserve, et transmets-les à `immo-associe`.

## Ce que tu sors

Existence de l'acte de base et du syndic ; un tableau des engagements du lot
(travaux votés, appels de fonds, charges, fonds de réserve) avec leur source ;
la clause qui répartit les dépenses entre vendeur et acquéreur, citée ; les
restrictions d'usage ; les pièces manquantes.

## Pièges

- Sortir un prix plafond sur un appartement sans le dossier du syndic :
  interdit. Il sort sans prix plafond, et la raison se dit.
- Calculer un appartement comme une maison : charges, travaux communs et
  règlement changent tout.
- Ignorer une restriction d'usage qui interdit la stratégie locative visée.
- Présumer la répartition légale alors qu'une clause l'écarte.
