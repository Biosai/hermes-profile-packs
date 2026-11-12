---
name: pieces-a-reclamer
description: "Lister les pièces à réclamer avant de signer"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Pièces à réclamer

## Quand l'utiliser

Dès qu'un bien devient sérieux : avant une offre, un compromis, une levée
d'option, une enchère.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| La région, le type de bien et le type de vente (requis) | la liste en dépend | établis par écrit |
| L'accès aux obligations en vigueur (requis) | la liste change dans le temps | la source officielle s'ouvre avec sa date |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : décide la liste (certificats et attestations selon la
  région ; diagnostics en France). `detect` (défaut) : déduis la région de
  l'adresse du bien, dis-la, fais-la confirmer.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Établis la région, le type de bien et le type de vente** (gré à gré,
   vente publique, vente sur plan). La liste en dépend, et elle change dans le
   temps : vérifie les obligations en vigueur sur la source officielle.
2. **Pièces techniques** : certificat de performance énergétique, contrôle de
   l'installation électrique, attestation amiante là où la région l'impose,
   information ou attestation de sol, dossier d'intervention ultérieure,
   citerne à mazout, rapport des pompiers si logements multiples.
3. **Pièces urbanistiques** : renseignements urbanistiques, permis et plans
   approuvés, infractions connues (avec `immo-architecte`).
4. **Pièces juridiques** : titre de propriété du vendeur, servitudes,
   hypothèques et saisies, baux en cours et leur enregistrement, droit de
   préemption.
5. **Copropriété** : acte de base, règlement, dossier du syndic (skill
   `dossier-copropriete`).
6. **France** : diagnostics du dossier technique, état des risques,
   documents de copropriété — **À VÉRIFIER** sur la liste en vigueur.
7. **Pour chaque pièce** : qui la détient (vendeur, notaire, commune, syndic,
   organisme), délai d'obtention, et ce qu'elle peut changer au dossier.

## Ce que tu sors

Un tableau : pièce, obligatoire ou utile, qui la détient, délai, statut
(reçue avec date / demandée / manquante), ce qu'elle peut changer. En tête,
les pièces manquantes qui peuvent faire tomber le dossier.

## Pièges

- Une liste de mémoire, ou celle d'une autre région.
- Une pièce « reçue » mais périmée ou relative à un autre lot.
- Attendre l'acte pour lire les renseignements urbanistiques : ils doivent
  être lus avant l'offre quand la stratégie en dépend.
- Réclamer toi-même au vendeur : le courriel est un brouillon pour
  l'investisseur.
