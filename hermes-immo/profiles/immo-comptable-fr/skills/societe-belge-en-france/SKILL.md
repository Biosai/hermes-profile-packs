---
name: societe-belge-en-france
description: "Cadrer l'impôt d'une société belge qui investit en France"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Une société belge qui investit en France

## Quand l'utiliser

Dès qu'une opération française est envisagée par la société belge de
l'investisseur : achat, location, revente, ou détention d'un bien déjà acquis.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| FR dans `immo.juridictions`, ou sa demande explicite (requis) | le périmètre s'ouvre sur sa demande | le réglage contient FR, ou sa demande est citée |
| Les statuts et la situation de la société (requis) | qualification et obligations | statuts et extrait s'ouvrent |
| L'accès à Légifrance et au BOFiP (requis, gratuit) | aucun chiffre de mémoire | la série ou l'article s'ouvre ; sinon tout est À VÉRIFIER |

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

1. **Annonce l'état des sources** en tête : ce qui n'est pas lu sur Légifrance
   ou le BOFiP dans la conversation est **À VÉRIFIER**.
2. **Qualifie l'activité en France** : revente habituelle (marchand de biens),
   location nue ou meublée, détention patrimoniale. La qualification décide
   des impôts en jeu.
3. **Impôt sur les sociétés** : les revenus et plus-values d'un immeuble
   situé en France y sont en principe imposables ; vérifie l'existence d'un
   établissement stable et ses conséquences (série BOFiP sur la
   territorialité de l'IS).
4. **Taxe annuelle sur les immeubles détenus par des entités juridiques**
   (CGI, art. 990 D et suivants — lire la version en vigueur) : vérifie les
   cas d'exonération et les déclarations qui les conditionnent ; elle peut
   coûter chaque année si l'exonération n'est pas demandée.
5. **Plus-values des non-résidents** (CGI, art. 244 bis A — version en
   vigueur) : prélèvement, représentant fiscal éventuel.
6. **Convention fiscale franco-belge** : vérifie sur source officielle quel
   texte est en vigueur à la date de l'opération, puis lis l'article sur les
   revenus immobiliers et la méthode d'élimination de la double imposition.
7. **Obligations déclaratives** : immatriculation, déclarations de résultat,
   déclaration des immeubles détenus, représentant fiscal.
8. **Signale la moitié belge** à `immo-comptable-be` : comment la Belgique
   traite ce revenu ou cette plus-value, et cite son avis.

## Ce que tu sors

Par impôt : règle, texte (article, série BOFiP, version ou À VÉRIFIER), effet
en fourchette, obligation déclarative, échéance. Puis l'avis belge cité, et la
question pour un expert-comptable français.

## Pièges

- Oublier la taxe annuelle sur les immeubles : elle n'apparaît pas dans un
  calcul de marge, elle apparaît chaque année.
- Citer un article de la convention sans avoir vérifié quel texte est en
  vigueur.
- Traiter la France seule : une opération transfrontalière a deux moitiés.
- Proposer de toi-même un bien français quand `immo.juridictions` ne
  contient pas FR.
