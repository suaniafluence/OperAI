# OperAI - ERP IA Conversational (MVP)

OperAI est une preuve de concept d'ERP piloté uniquement par une interface
conversationnelle via **Custom GPT Actions**. Aucune fenêtre de saisie
classique : l'utilisateur dicte ou saisit ses demandes, qui sont interprétées
par un modèle IA afin d'effectuer les opérations (création de devis, gestion de
stock, etc.).

## Stack technique

- **Backend API** : Python, [FastAPI](https://fastapi.tiangolo.com/) et
  [Strawberry GraphQL](https://strawberry.rocks/).
- **Authentification** : OAuth2 via Auth0.
- **Base de données** : MongoDB Atlas.
- **IA générative** : OpenAI `gpt-4.1-nano` avec l'API `responses`.
- **Transcription vocale** : OpenAI Whisper API.
- **Génération de PDF** : `fpdf2` (ou `ReportLab`).
- **Stockage des documents** : disque local d'une instance EC2.
- **Monitoring optionnel** : Grafana / Loki / Promtail.

## Installation

```bash
# 1. Cloner le dépôt
git clone <repo-url>
cd OperAI

# 2. Environnement Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Créer ensuite un fichier `.env` avec vos variables :

```bash
# MongoDB
MONGODB_URI=<url-mongodb>
MONGO_DB_NAME=erp_ia_db
MONGO_DB_COL=documents

# Auth0
AUTH0_DOMAIN=<domain>
AUTH0_API_AUDIENCE=<audience>
AUTH0_CLIENT_ID=<client-id>
AUTH0_CLIENT_SECRET=<client-secret>

# OpenAI
OPENAI_API_KEY=<your-openai-key>

# Chemin local pour les PDF
LOCAL_STORAGE_PATH=/path/to/pdfs
```

Lancer l'API en développement :

```bash
uvicorn app.main:app --reload
```

L'API GraphQL est disponible via `/graphql`. La route `/transcribe`
permet d'envoyer un fichier audio pour transcription via Whisper.

## Fonctionnement

1. L'utilisateur interagit avec un **Custom GPT** configuré pour appeler les
   endpoints GraphQL de l'ERP.
2. Les instructions textuelles (ou vocales via Whisper) sont converties en
   mutations GraphQL sécurisées.
3. Les données sont enregistrées dans MongoDB, les devis/factures générés en
   PDF puis stockés sur le disque local de l'EC2.
4. Le résultat (lien vers le PDF, réponse à une question de reporting, etc.) est
   renvoyé par le GPT à l'utilisateur.

## Roadmap

- Journalisation détaillée des actions.
- Déploiement éventuel d'un modèle LLM auto‑hébergé.
- Interface d'administration GraphQL.

## Licence

Projet privé destiné à des expérimentations autour de l'IA générative.
