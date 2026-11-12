---
name: lecture-photo-travaux
description: "Lire annonce, photos et certificats d'un bien"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Lecture des photos et de l'annonce

## Quand l'utiliser

Dès qu'un bien arrive avec une annonce, des photos, un certificat énergétique
ou un rapport ; avant tout chiffrage ; pour préparer une visite.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'annonce et ses photos (requis) | on lit ce qui est montré | les photos s'ouvrent en taille lisible |
| Les certificats annoncés | énergie, électricité, amiante | chaque certificat s'ouvre et se date |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : nomme les certificats attendus (PEB en Wallonie et à
  Bruxelles, EPC en Flandre, DPE en France) et les obligations qu'ils
  déclenchent. `detect` (défaut) : déduits de l'adresse.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Inventorie ce que tu as** : nombre de photos, pièces montrées, pièces
   absentes, certificats (énergie, électricité, amiante, sol) et leur date.
2. **Pièce par pièce, ce que la photo montre** : sols, murs, plafonds,
   menuiseries, sanitaires, cuisine, radiateurs, tableau électrique, traces
   d'humidité, fissures. Note le numéro de la photo.
3. **Enveloppe** : toiture (type, état visible, angle de vue), façades,
   châssis, gouttières, isolation visible. Une toiture vue d'en bas ne dit pas
   son état.
4. **Signaux de risque** : fissures en escalier, auréoles, salpêtre, odeurs
   signalées, installation électrique ancienne, chaudière ancienne, matériaux
   susceptibles de contenir de l'amiante selon l'époque, affaissements.
5. **Certificats** : classe énergétique et ce qu'elle implique (obligations,
   aides, interdictions de louer : skill `obligations-et-aides-renovation`),
   remarques du contrôle électrique.
6. **Cohérence** : l'annonce dit « rénové », la photo montre un tableau
   ancien ; la surface annoncée ne colle pas au nombre de pièces. Remonte
   l'écart.
7. **Ce qui manque** : chaque élément non visible devient une ligne « à voir
   en visite », jamais une hypothèse.

## Ce que tu sors

Un tableau de postes visibles (élément, état observé, photo n°, niveau
d'intervention probable), les signaux de risque, et la liste « à voir en
visite » classée par impact sur le budget.

## Pièges

- Supposer l'état de ce qui n'est pas photographié : une cave absente des
  photos est souvent la raison de son absence.
- Prendre une photo d'agence retouchée ou ancienne pour l'état actuel.
- Conclure sur la structure à partir d'une seule photo : signale, ne
  diagnostique pas — un ingénieur ou un expert le fera.
- Oublier les parties communes d'un immeuble en copropriété.
