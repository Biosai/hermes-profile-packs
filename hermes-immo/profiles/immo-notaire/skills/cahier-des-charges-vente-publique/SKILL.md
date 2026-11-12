---
name: cahier-des-charges-vente-publique
description: "Lire un cahier des charges de vente publique"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Cahier des charges d'une vente publique

## Quand l'utiliser

Avant toute enchère, sur la plateforme publique du notariat (Biddit en
Belgique) ou en salle ; dès que le cahier des charges est disponible.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le cahier des charges complet et ses annexes (requis) | la lecture est ligne par ligne | la version datée de l'étude s'ouvre |
| La région du bien (requis) | frais et pièces en dépendent | établie depuis l'adresse |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : règles régionales et plateforme de vente. `detect`
  (défaut) : déduis la région de l'adresse du bien, dis-la, fais-la confirmer.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Récupère le cahier complet** et ses annexes (renseignements
   urbanistiques, certificats, dossier de copropriété, baux). Note sa date et
   l'étude qui l'a établi.
2. **Frais d'adjudication** : barème ou pourcentage fixé par le cahier, base
   de calcul, qui paie quoi. Ils s'ajoutent au prix et suivent l'enchère.
3. **Délais de paiement** : prix, frais, intérêts de retard, sanctions
   (revente sur folle enchère ou équivalent). Confronte-les au financement.
4. **Occupation** : bien libre ou occupé, baux opposables, date de jouissance,
   indemnité d'occupation. Un bail en cours se lit avec `immo-avocat`.
5. **État du bien et garanties exclues** : vices cachés, contenance, nombre de
   logements, conformité urbanistique, sol. Ce qui est exclu, l'acquéreur le
   porte.
6. **Copropriété** : clause sur les travaux et appels de fonds votés avant la
   vente. La règle légale est supplétive ; la clause du cahier prime. Lis-la,
   ne la présume pas (skill `dossier-copropriete`).
7. **Surenchère, conditions d'admission, garanties à fournir** pour enchérir.
8. **Chiffre** tout ce que le cahier met à charge de l'adjudicataire et
   transmets-le à `immo-associe` pour le prix plafond.

## Ce que tu sors

Les clauses qui comptent, citées avec leur article ; un tableau des coûts à
charge de l'adjudicataire (poste, base, fourchette) ; l'occupation et ses
conséquences ; les pièces absentes ; la question à poser à l'étude avant la
séance.

## Pièges

- Enchérir sur un prix plafond calculé sans les frais d'adjudication, qui
  montent avec l'enchère.
- Présumer la règle légale sur les charges de copropriété : la clause du
  cahier peut l'écarter.
- Ignorer le délai de paiement : un financement qui tarde coûte des intérêts
  ou la vente.
- Croire qu'une clause de vente publique se négocie : elle se chiffre.
