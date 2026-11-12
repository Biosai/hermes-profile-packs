---
name: obligations-et-aides-renovation
description: "Dire les obligations et aides de rénovation d'un bien"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Obligations et aides à la rénovation

## Quand l'utiliser

Quand un bien a une mauvaise classe énergétique ; quand l'acquéreur pourrait
être tenu de rénover ; quand un équipement (chauffage, citerne) est en fin de
vie ; quand une aide est évoquée dans un calcul.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'adresse et la date d'acquisition visée (requis) | les obligations en dépendent | région et date établies |
| Le certificat énergétique du bien | classe de départ | le certificat s'ouvre et se date |
| L'accès aux décrets et aux organismes d'aide (requis) | aucune échéance de mémoire | le texte s'ouvre avec sa date |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : décide quels décrets et quels régimes d'aide lire.
  `detect` (défaut) : déduis la région de l'adresse du bien, dis-la, fais-la
  confirmer.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Établis la région** et la date de l'acte : les obligations diffèrent par
   région et s'appliquent souvent à partir d'une date d'acquisition.
2. **Obligations de rénovation à l'achat** : existe-t-il une obligation
   d'atteindre une classe dans un délai après l'acquisition ? Lis le décret
   en vigueur, pas la page d'information : une page officielle et le décret
   ont déjà divergé sur le délai. Un projet de texte n'est pas une loi.
3. **Certificats et attestations à la vente** : certificat énergétique,
   attestation amiante, attestation de sol, selon la région.
4. **Interdictions de louer** sous une classe énergétique (en France
   notamment) : calendrier lu sur le texte.
5. **Équipements** : interdictions d'installer ou de remplacer certains
   chauffages fossiles, par étapes ; lis le calendrier sur le décret et ne
   budgète jamais un équipement en voie d'interdiction dans une rénovation
   lourde.
6. **Aides** : primes, prêts à taux réduit, réductions d'impôt. Pour chacune :
   texte et date, ouverte ou fermée, **ouverte à une société ? à un
   bailleur ?**, conditions (saut de classe, audit préalable, occupation
   personnelle, revenus), plafonds. Un régime peut être remplacé du jour au
   lendemain : vérifie qu'il est ouvert à la date de la demande.
7. **N'en crédite un dossier** que si toutes les conditions sont remplies et
   vérifiées ; sinon, scénario marqué **À VÉRIFIER**.

## Ce que tu sors

Un tableau des obligations (texte, version, échéance, coût en fourchette pour
la respecter) et un tableau des aides (texte, statut, éligibilité de
l'investisseur, conditions, montant en fourchette ou « non éligible »).

## Pièges

- Créditer une aide réservée aux ménages qui occupent le logement à une
  société qui achète pour revendre.
- Citer une échéance d'un communiqué de presse ou d'un site d'aide : cite le
  texte.
- Oublier qu'une obligation crée la décote que l'investisseur exploite : elle
  se chiffre, elle ne se contourne pas.
