---
name: questionnaire-garde-fou
description: "Passer le questionnaire garde-fou avant de signer"
metadata:
  hermes:
    config:
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
---
# Questionnaire garde-fou avant de signer

## Quand l'utiliser

Juste avant de signer un compromis, de lever une option ou d'enchérir ;
quand l'investisseur dit « on y va ».

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le dossier : pièces reçues, avis des experts (requis) | chaque réponse vient d'une pièce | les pièces s'ouvrent |
| La fiche investisseur | risques déjà acceptés, scénario sécurité | la fiche se lit ; sinon rien n'est « accepté » |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.fiche_investisseur` : les risques qu'il a acceptés par décision ; en
  `memory` (défaut), demande-les à `immo-bras-droit`.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Pose chaque question au dossier, pas de mémoire.** Pour chacune, la
   réponse vient d'une pièce citée, ou elle est « inconnue ».
   - Le nombre de logements que la stratégie suppose est-il reconnu ?
   - Le bien est-il libre ? Sinon, quels baux, opposables, jusqu'à quand ?
   - Existe-t-il un acte de base et un syndic ? Des travaux votés ?
   - Une infraction urbanistique, une expropriation, une préemption ?
   - Le sol, l'amiante, l'inondation : que disent les attestations ?
   - Le régime de droits visé : l'acte portera-t-il la mention requise ?
   - Le financement couvre-t-il le prix, les frais et le délai de paiement ?
   - Une condition suspensive protège-t-elle chaque risque non levé ?
   - Le prix tient-il dans le scénario sécurité de `immo-associe` ?
2. **Classe chaque réponse** : levée (pièce citée), à lever avant signature,
   couverte par une condition suspensive, acceptée par l'investisseur
   (décision enregistrée).
3. **Une réponse inattendue arrête la signature** jusqu'à décision : dis-le
   clairement, sans dramatiser.
4. **Rédige les questions restantes** en brouillon : au vendeur ou à l'agence,
   au notaire instrumentant, au syndic.
5. **Passe le relais** : risque juridique → `immo-avocat` ; régime de droits →
   `immo-comptable-be` ; logements → `immo-architecte`.

## Ce que tu sors

Le questionnaire rempli : question, réponse, pièce, statut. En tête : les
points qui doivent être levés avant de signer. Puis les brouillons de
questions.

## Pièges

- Passer le questionnaire après la signature : un compromis signé fige les
  risques.
- Cocher « levé » sur la foi d'une affirmation du vendeur sans pièce.
- Allonger la liste au point qu'il ne la lise plus : garde les questions qui
  peuvent arrêter l'opération.
