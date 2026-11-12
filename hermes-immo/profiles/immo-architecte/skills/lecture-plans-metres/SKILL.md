---
name: lecture-plans-metres
description: "Tirer surfaces, métrés et quantités de plans ou relevés"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Lecture de plans, métrés et quantités

## Quand l'utiliser

Quand un dossier fournit des plans (permis, acte de base, plans d'architecte,
croquis d'agence) ; quand `immo-conducteur-travaux` a besoin de quantités ;
quand la surface annoncée doit être confrontée à une pièce.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Les plans ou relevés (requis) | tout métré en part | échelle ou cotes lisibles |
| La définition de surface applicable (si vente ou bail) | les surfaces légales diffèrent par pays | le texte qui la définit est lu |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : décide quelle définition légale de surface lire (en
  France, la surface privative d'un lot de copropriété a la sienne). `detect`
  (défaut) : pays déduit de l'adresse.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Identifie chaque pièce** : nature, auteur, date, échelle, indice de
   révision. Un plan sans échelle ni cote n'est qu'un croquis.
2. **Distingue les surfaces** : habitable, utile, brute, au sol, et celle que
   l'annonce utilise. Dis laquelle tu mesures.
3. **Relève les cotes écrites** plutôt que de mesurer sur un dessin ; si tu
   dois mesurer à l'échelle, dis-le et élargis la fourchette.
4. **Confronte** : plan contre acte, plan contre annonce, plan contre photos.
   Un écart de surface est un fait à remonter à `immo-associe` : il est souvent
   la décote, ou le piège.
5. **Fais les métrés par ouvrage** : murs (longueur × hauteur, ouvertures
   déduites), sols et plafonds, toiture (pente comprise), menuiseries (nombre
   et dimensions), réseaux (longueurs estimées).
6. **Ajoute les pertes et chutes** comme un poste séparé, jamais noyé dans la
   quantité.
7. **Transmets les quantités** à `immo-conducteur-travaux` avec leur source
   et leur précision.

## Ce que tu sors

Un tableau de surfaces (pièce, type de surface, valeur, source, précision) et
un tableau de quantités (ouvrage, unité, quantité, méthode, source). En tête :
l'écart principal entre pièces, s'il y en a un.

## Pièges

- Prendre la surface d'annonce pour acquise : elle sert à vendre.
- Mesurer un plan imprimé ou scanné sans vérifier l'échelle réelle.
- Oublier les hauteurs : une surface sous un certain plafond ne compte pas
  toujours comme habitable.
- Mélanger des plans de dates différentes sans le dire.
