# Cahier des charges et inventaire exhaustif des fonctionnalités et technologies

## Projet : Template RAG Azure — `{{cookiecutter.repository_name}}`

- **Auteur de l'analyse :** GitHub Copilot
- **Date :** Mai 2026
- **Propriété intellectuelle :** © 2022–2026 Schneider Electric Industries SAS. Tous droits réservés.

---

## 1. Vue d'ensemble du projet

Ce dossier constitue un **archétype (template) de projet RAG (Retrieval-Augmented Generation)** déployable sur Microsoft Azure. Il est conçu par et pour les équipes AI de Schneider Electric dans le cadre de la plateforme interne **AIHub**. Il est généré via **Cookiecutter** (variables du type `{{cookiecutter.use_case_name}}`), ce qui en fait un modèle paramétrable que chaque cas d'usage instancie avec ses propres valeurs.

Le projet déploie **deux Azure Function Apps indépendantes** :

- **Processing Function App** : pipeline d'ingestion de documents (chargement, découpage, vectorisation, injection dans une base vectorielle).
- **Orchestrator Function App** : agent conversationnel RAG exposé via une API REST FastAPI (sessions, questions-réponses, feedback).

Ces deux applications sont conteneurisées (Docker), versionnées via Git (SemVer), packagées en wheel Python, et déployées via des pipelines GitHub Actions sur quatre environnements : `dev`, `qa`, `prv` (private preview), et `prd` (production).

---

## 2. Structure du dossier — Inventaire complet

```
{{cookiecutter.repository_name}}/
├── .dockerignore
├── .github/
│   ├── env/                         # Fichiers d'environnement par environnement (dev/qa/prv/prd)
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
│       ├── ci.yaml
│       ├── cicd-dev.yaml
│       ├── cicd-prv.yaml
│       ├── cicd-qa.yaml
│       ├── cd-prd.yaml
│       ├── documentation-preview.yml
│       ├── tag-official-release.yaml
│       └── update-from-template.yaml
├── .gitignore
├── .gitleaks.toml
├── .hadolint.yaml
├── .pre-commit-config.yaml
├── adf/                             # Azure Data Factory
│   ├── dataset/
│   ├── deployment/
│   ├── factory/
│   ├── integrationRuntime/
│   ├── linkedService/
│   │   ├── AmazonS3.json
│   │   ├── AzureADLS.json
│   │   ├── AzureFunction.json
│   │   └── AzureKeyVault.json
│   ├── managedVirtualNetwork/
│   ├── pipeline/
│   │   ├── rag-ingestion-pipeline.json
│   │   ├── rag-ingestion-trigger-pipeline.json
│   │   ├── rag-process-documents.json
│   │   └── rag-retrieve-documents.json
│   ├── publish_config.json
│   └── trigger/
│       └── pdf-trigger.json
├── ai-search/
│   └── index.json                   # Définition JSON de l'index Azure AI Search
├── bruno/
│   └── {{cookiecutter.use_case_name}} API/  # Tests d'API via Bruno
├── certs/
├── AGENTS.md                        # Instructions pour agents AI
├── CHANGELOG.md
├── CONTRIBUTING.md
├── coverity.yaml                    # Configuration analyse Coverity
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── noxfile.py                       # Automatisation CI/CD locale
├── pyproject.toml                   # Gestion des dépendances & métadonnées
├── README.md
├── uv.lock
├── scripts/
│   ├── azure_function_settings.py
│   ├── pg_vector_deployment.py
│   ├── reserved_settings.py
│   └── utils.py
├── tests/
│   ├── conftest.py
│   ├── end_to_end/
│   ├── environment/
│   ├── integration/
│   └── unit/
└── {{cookiecutter.python_package_name}}/
    ├── __init__.py
    ├── metainfo.py
    ├── observability.py
    ├── ai_search/
    │   ├── __init__.py
    │   └── cli.py
    ├── evaluation/
    │   ├── __init__.py
    │   ├── constants.py
    │   ├── datasets.py
    │   ├── evaluators.py
    │   ├── experiments.py
    │   └── target.py
    ├── orchestrator/
    │   ├── __init__.py
    │   ├── exceptions.py
    │   ├── run.py
    │   ├── conversational/
    │   │   ├── __init__.py
    │   │   ├── config.py
    │   │   ├── context.py
    │   │   ├── core.py
    │   │   ├── graph_conversation.py
    │   │   ├── schemas.py
    │   │   └── session.py
    │   ├── function_app/
    │   │   ├── __init__.py
    │   │   ├── function_app.py
    │   │   ├── host.json
    │   │   ├── local.settings.example.json
    │   │   ├── runtime-settings.env
    │   │   └── .env.example
    │   ├── vector_stores/
    │   │   ├── __init__.py
    │   │   └── postgres.py
    │   └── web_server/
    │       ├── __init__.py
    │       ├── config.py
    │       ├── errors.py
    │       ├── exception_handlers.py
    │       ├── main.py
    │       ├── models/
    │       │   ├── __init__.py
    │       │   ├── feedback.py
    │       │   └── session.py
    │       └── routers/
    │           ├── __init__.py
    │           ├── feedback.py
    │           ├── session.py
    │           └── technical.py
    └── processing/
        ├── function_app/
        │   ├── __init__.py
        │   ├── function_app.py
        │   ├── host.json
        │   ├── local.settings.example.json
        │   ├── runtime-settings.env
        │   ├── .env.example
        │   └── .funcignore
        └── data_ingestion/
            ├── __init__.py
            ├── processing.py
            ├── db_manager.py
            ├── document_injection/
            │   ├── __init__.py
            │   ├── config.py
            │   ├── embedding/
            │   │   ├── __init__.py
            │   │   └── embedder.py
            │   └── vector_store/
            │       ├── __init__.py
            │       ├── ai_search_vector_manager.py
            │       └── postgres_vector_manager.py
            ├── document_loading/
            │   ├── __init__.py
            │   ├── document_manager.py
            │   ├── azure/
            │   │   ├── __init__.py
            │   │   └── adls_loader.py
            │   ├── config/
            │   │   ├── __init__.py
            │   │   └── document_loader.py
            │   └── pypdf/
            │       ├── __init__.py
            │       └── file_loader.py
            ├── document_processing/
            │   ├── __init__.py
            │   └── cleaning.py
            └── utils/
                ├── __init__.py
                ├── common_tools.py
                ├── function_tools.py
                └── retry.py
```

---

## 3. Architecture technique globale

### 3.1 Paradigme RAG (Retrieval-Augmented Generation)

Le système suit le paradigme RAG en deux phases distinctes :

1. **Phase d'ingestion (offline)** : Les documents bruts (PDF, fichiers ADLS) sont chargés, découpés en chunks, vectorisés (embeddings) puis stockés dans une base vectorielle (Azure AI Search ou PostgreSQL/pgvector).
2. **Phase de conversation (online)** : L'utilisateur pose une question, l'agent ReAct récupère les passages pertinents du vector store par similarité cosinus, puis formule une réponse à l'aide d'un LLM (Azure OpenAI GPT).

### 3.2 Décomposition des deux Function Apps

| Fonctionnalité | Processing App | Orchestrator App |
|---|---|---|
| Type Azure | Durable Functions | ASGI (FastAPI) |
| Entrée | HTTP trigger + blob trigger | HTTP REST API |
| Cœur | Pipeline d'ingestion durable | Agent ReAct LangGraph |
| Stockage | Azure Blob (ADLS), AI Search, PGVector | CosmosDB (sessions + mémoire), AI Search / PGVector |
| Observabilité | OpenTelemetry → Dynatrace | OpenTelemetry → Dynatrace |

---

## 4. Inventaire détaillé des fonctionnalités

### 4.1 Pipeline de traitement des données (`processing/`)

#### 4.1.1 Chargement de documents (`document_loading/`)

**Fichiers :** `adls_loader.py`, `file_loader.py`, `document_loader.py`, `document_manager.py`

- **Chargement depuis Azure Data Lake Storage (ADLS)** : la classe `AdlsManager` charge les fichiers blob depuis un conteneur Azure Storage à l'aide d'une chaîne de connexion ou via Azure AD. Elle utilise `AzureBlobStorageFileLoader` de `langchain_community`.
- **Chargeur personnalisé** `NewAzureBlobStorageFileLoader` : extension de la classe LangChain qui télécharge le blob dans un répertoire temporaire, puis délègue le parsing au `FileLoader` interne. Conserve le nom du blob comme métadonnée `source`.
- **Chargeur PDF** (`pypdf/file_loader.py`) : utilise la bibliothèque `pypdf` (≥6.2.0) pour parser les documents PDF. Extraction page par page, conservation des métadonnées.
- **Abstraction `DocumentLoader`** (`config/document_loader.py`) : interface générique permettant d'ajouter d'autres sources de documents (S3, SharePoint, etc.) via l'énumération `DocumentLoaderType`.
- **Mesures d'observabilité** : les jauges `NUMBER_DOCUMENT_LOADED_SUCCESS` et `NUMBER_DOCUMENT_LOADED_FAIL` sont incrémentées à chaque opération de chargement.

#### 4.1.2 Traitement et découpage (`document_processing/`)

**Fichier :** cleaning.py

- **Chunking par `RecursiveCharacterTextSplitter`** (LangChain) avec encodage tiktoken `o200k_base` (compatible GPT-4o).
- **Paramètres configurables** : `chunk_size` (défaut 600 tokens), `chunk_overlap` (défaut 125 tokens).
- **Séparateurs hiérarchiques** : `\n\n`, `\n`, `. `, ` `, `""` pour découper intelligemment le texte en respectant la structure sémantique.
- Chaque chunk résultant est un objet `Document` LangChain portant les métadonnées d'origine (source, page…).

#### 4.1.3 Injection et vectorisation (`document_injection/`)

**Fichiers :** `embedder.py`, `ai_search_vector_manager.py`, `postgres_vector_manager.py`, `config.py`

- **Modèle d'embedding** : `text-embedding-ada-002` via Azure OpenAI (`AzureOpenAIEmbeddings` de LangChain). L'`EndpointConfig` centralise l'endpoint APIM, la clé API, la version d'API, le modèle d'embedding, la taille des chunks.
- **Double backend de stockage vectoriel** :
  - **Azure AI Search** (`ai_search_vector_manager.py`) : injection par batch dans un index Azure Cognitive Search avec champs `chunk_id`, `metadata`, `source`, `content`, `content_vector` (type `Collection(Edm.Single)`).
  - **PostgreSQL pgvector** (`postgres_vector_manager.py`) : injection via `langchain_postgres.PGVector`, avec index HNSW sur la colonne `embedding` pour des recherches ANN (Approximate Nearest Neighbor) performantes.
- **Mécanisme de retry** (`utils/retry.py`) : basé sur `tenacity`, avec logging structuré avant/après chaque tentative d'embedding. Évite les erreurs transitoires liées aux rate limits d'Azure OpenAI.
- **Métriques d'observabilité** : compteurs `NUMBER_TOKEN_USED_DURING_EMBEDDING`, `NUMBER_API_CALL_DURING_EMBEDDING`, `NUMBER_FAILED_EMBEDDING`.

#### 4.1.4 Orchestration durable (`function_app/function_app.py`)

- **Azure Durable Functions** (`azure-functions-durable`) avec pattern **fan-out / fan-in** :
  - L'orchestrateur `ingestion_orchestrator` charge tous les documents en parallèle (`task_all`), les prépare en parallèle (chunking), puis les injecte séquentiellement pour éviter les rate limits OpenAI.
  - `start_orchestrator` : HTTP trigger qui démarre une nouvelle instance de l'orchestration durable et retourne immédiatement un `check_status_response`.
  - Activités : `load_documents_from_storage`, `prepare_documents`, `embed_and_store_documents`.
- **Batching** : `batch_input_documents` découpe la liste de documents en lots de taille configurable.
- **`DFApp`** : application Azure Durable Functions initialisée avec `http_auth_level=ANONYMOUS` (sécurité gérée au niveau réseau/APIM).
- **host.json** : configuration de l'extension bundle (`Microsoft.Azure.Functions.ExtensionBundle` v4), activation de `acrUseManagedIdentityCreds`, `vnetImagePullEnabled`.

#### 4.1.5 Fonction de traitement HTTP (processing.py)

Trois fonctions d'entrée HTTP orchestrées par ADF :
- `main_load_files` : charge les fichiers depuis le stockage Azure.
- `main_process_files` : découpe les documents en chunks.
- `main_ingest_files` : vectorise et injecte dans le vector store.

Chacune désérialise les documents LangChain via `langchain_core.load.load()` (format JSON sérialisé), ce qui assure la compatibilité des métadonnées entre étapes.

---

### 4.2 Agent conversationnel RAG (`orchestrator/`)

#### 4.2.1 Architecture de l'agent (`conversational/`)

**Fichiers :** `core.py`, `graph_conversation.py`, `context.py`, `config.py`, `session.py`, `schemas.py`

- **`ConversationalCore`** : classe centrale qui initialise et coordonne tous les composants :
  - Client Azure OpenAI (`AzureChatOpenAI`)
  - Retriever de contexte (`ContextRetriever`)
  - Stockage de sessions (`SessionStorage`)
  - Graphe ReAct (`build_react_agent`)
  - Checkpointer CosmosDB (`CosmosDBSaver`)
- **Agent ReAct** (`graph_conversation.py`) : construit via `langchain.agents.create_agent`. L'agent dispose d'un outil `retrieve_context_tool` qui effectue une recherche de similarité dans le vector store. Prompt système : l'assistant ne doit pas répondre de mémoire sur des faits documentaires mais toujours utiliser l'outil de récupération.
- **Récupération de contexte** (`context.py`) : la classe `ContextRetriever` sélectionne dynamiquement le backend vector store (`AzureSearch` ou `PGVector`) selon la configuration. Recherche par similarité cosinus avec `k` documents récupérés (défaut 3). Initialisation différée pour éviter les appels Azure au démarrage.
- **Mémoire de conversation** : persistée dans **Azure Cosmos DB** via `langgraph-checkpoint-cosmosdb`. Deux conteneurs CosmosDB : `sessions` (métadonnées de session) et `memory` (historique des messages). Chaque message est estampillé avec son `trace_id` LangSmith.
- **Sessions** (session.py) : `SessionStorage` gère le CRUD des sessions dans CosmosDB avec `DefaultAzureCredential` (passwordless Azure AD). Requêtes SQL paramétrées pour éviter les injections.
- **Traçabilité LangSmith** : chaque appel à `graph.invoke()` génère un `trace_id` UUID v4 passé comme `run_id` dans le `RunnableConfig`. Ce trace_id est propagé dans les métadonnées de tous les messages, permettant le rattachement du feedback utilisateur à la trace exacte.
- **`ConversationalConfig`** : `pydantic-settings` avec valeurs par défaut pour dev (endpoint CosmosDB, modèle GPT-4.1, température 0.7, max_tokens 1000, top_p 0.95, frequency_penalty 0, presence_penalty 0). Clé API via `SecretStr` (jamais en clair dans le code).

#### 4.2.2 Méthodes principales de `ConversationalCore`

| Méthode | Description |
|---|---|
| `start_session()` | Crée une nouvelle session (UUID v1), persiste dans CosmosDB |
| `end_session(session_id)` | Supprime la session de CosmosDB |
| `get_session(session_id)` | Vérifie l'existence d'une session |
| `get_session_history(session_id)` | Récupère l'historique des messages depuis le checkpointer |
| `ask_question(session_id, query_text)` | Question simple → réponse texte + trace_id |
| `ask_question_with_context(session_id, query_text)` | Question avec retour du contexte récupéré → `AskQuestionWithContextReturnFormat` |
| `_invoke_graph_with_trace(session_id, query_text)` | Méthode interne partagée invoquant le graphe LangGraph |

---

### 4.3 Serveur web FastAPI (`orchestrator/web_server/`)

**Fichiers :** `main.py`, `config.py`, `routers/session.py`, `routers/feedback.py`, `routers/technical.py`, `models/session.py`, `models/feedback.py`, `errors.py`, `exception_handlers.py`

#### 4.3.1 Application FastAPI

- **`app = FastAPI(version=API_VERSIONS[-1])`** : version de l'API gérée dans `config.py` (liste `API_VERSIONS = ["1.0"]`).
- **Instrumentation OpenTelemetry** : `FastAPIInstrumentor.instrument_app()` avec les fournisseurs de traces et métriques configurés. Traces et métriques automatiquement exportées vers Dynatrace.
- **Redirection racine** : `GET /` → redirection vers `/docs` (Swagger UI automatique).
- **Structure "Big Applications"** : routeurs séparés par domaine, préfixe `/api`.
- **Gestion d'erreurs centralisée** : `ErrorRegistry` (bibliothèque interne `fastapi-error-manager`) avec gestionnaires pour `BaseError`, `RequestValidationError`, `Exception`. `UnknownSessionErrorModel` mappé sur `SessionNotFoundError` (404 Not Found).
- **`ConversationalCoreBuilder`** : singleton thread-safe qui initialise `ConversationalCore` à la première requête (initialisation différée). Résolution du type de vector store via la variable `VECTOR_STORE_TYPE` (valeurs `AI_SEARCH` ou `PG_VECTOR`).

#### 4.3.2 Routeur Sessions (`/api/sessions`)

| Endpoint | Méthode | Description |
|---|---|---|
| `POST /api/sessions/` | POST | Démarre une nouvelle session → retourne `Session(id=UUID)` |
| `GET /api/sessions/{session_id}` | GET | Vérifie qu'une session existe |
| `POST /api/sessions/{session_id}/messages` | POST | Envoie une question, retourne `MessageDetails(role, content, trace_id)` |
| `GET /api/sessions/{session_id}/messages` | GET | Retourne l'historique complet de la conversation |
| `DELETE /api/sessions/{session_id}` | DELETE | Termine et supprime la session |

Chaque gestionnaire enrichit la span OpenTelemetry courante avec l'attribut `session.id`.

#### 4.3.3 Routeur Feedback (`/api/feedback`)

Intégration complète avec **LangSmith** pour la collecte et la gestion du feedback utilisateur :

| Endpoint | Méthode | Description |
|---|---|---|
| `POST /api/feedback/traces/{trace_id}` | POST | Soumet un feedback (score, value, comment, correction) sur une trace |
| `GET /api/feedback/traces/{trace_id}` | GET | Lit le feedback associé à une trace |
| `PATCH /api/feedback/{feedback_id}` | PATCH | Met à jour un feedback existant |
| `DELETE /api/feedback/{feedback_id}` | DELETE | Supprime un feedback |

**Modèles Pydantic** :
- `FeedbackRequest` : score (float), value (str optionnel), comment (str optionnel), correction (dict optionnel).
- `FeedbackResponse` : feedback_id (UUID), status.
- `FeedbackDetail` : feedback complet avec timestamps `created_at`, `modified_at`.
- Validation de l'existence du trace en base LangSmith avant création du feedback (404 si inexistant).

#### 4.3.4 Routeur Technique (`/api/`)

| Endpoint | Description |
|---|---|
| `GET /api/alive` | Health check (204 No Content) |
| `GET /api/versions` | Retourne la liste des versions API supportées |
| `GET /api/code_version` | Retourne la version du package (lue via `__version__`) |

#### 4.3.5 En-têtes de sécurité HTTP

Configurés dans host.json pour toutes les réponses HTTP :
- `Cross-Origin-Opener-Policy: same-origin`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Cache-Control: no-store`
- `Content-Security-Policy: frame-ancestors 'none'`

---

### 4.4 Gestion des stockages vectoriels (`vector_stores/`)

#### 4.4.1 PGVector Manager (côté Orchestrateur)

**Fichier :** `orchestrator/vector_stores/postgres.py`

- `PGVectorManager` utilise SQLAlchemy avec le driver `psycopg` (v3).
- **Deux modes d'authentification** :
  - Mot de passe direct (dev/test)
  - **Passwordless via Azure AD** (`DefaultAzureCredential` + token AAD injecté via `@event.listens_for(engine, "do_connect")`)
- **Cache LRU** sur le moteur SQLAlchemy (`@lru_cache(maxsize=32)`) pour éviter la création redondante de connexions.
- `pool_pre_ping=True` : vérifie la connexion avant utilisation (robustesse).
- Paramètre `use_jsonb=True`, `create_extension=False` (l'extension pgvector est déjà installée sur l'infrastructure).

#### 4.4.2 AI Search (côté Orchestrateur et Processing)

- **`AzureSearch`** (LangChain) : recherche par similarité sémantique avec configuration `semantic_configuration_name="default"`.
- **Index JSON** (`ai-search/index.json`) : définition complète de l'index avec champs `chunk_id` (clé), `metadata`, `source`, `content` (searchable), `content_vector` (Collection(Edm.Single), vectorSearchProfile).
- **CLI** (`ai_search/cli.py`) : trois commandes Click (`create_collections`, `delete_collection`, `clean_deploy`) pour la gestion programmatique des index.

---

### 4.5 Module d'évaluation RAG (`evaluation/`)

**Fichiers :** evaluators.py, experiments.py, datasets.py, target.py, `constants.py`

#### 4.5.1 Évaluateurs LLM-as-judge (evaluators.py)

Quatre évaluateurs basés sur la bibliothèque `openevals` :

| Évaluateur | Clé de feedback | Description |
|---|---|---|
| Correctness | `correctness` | Comparer la réponse générée à la réponse de référence |
| Helpfulness | `helpfulness` | Mesurer la pertinence de la réponse pour la question posée |
| Groundedness | `groundedness` | Vérifier que la réponse est ancrée dans le contexte récupéré |
| Retrieval Relevance | `retrieval_relevance` | Évaluer la pertinence des documents récupérés |

Le juge LLM est un `AzureChatOpenAI` avec `temperature=0` et `max_retries=2`. Chaque évaluateur utilise des prompts standardisés (`CORRECTNESS_PROMPT`, `RAG_GROUNDEDNESS_PROMPT`, etc.).

#### 4.5.2 Création de datasets (datasets.py)

- Commande Click `create_dataset` : crée un dataset LangSmith avec des paires Q/R d'exemple.
- Gestion du conflit (dataset déjà existant) via `LangSmithConflictError`.
- Chaque exemple contient `inputs` (question), `outputs` (ground_truth_answer), `metadata` (question_id, difficulty, topic).

#### 4.5.3 Évaluation hors ligne (experiments.py)

- Commande Click `run_evaluation` : exécute `client.evaluate()` LangSmith avec les quatre évaluateurs et le dataset cible.
- Options : `--dataset_name`, `--max_concurrency` (défaut 2), `--experiment_prefix`.
- La fonction `target` (target.py) réutilise le `ConversationalCore` singleton et appelle `ask_question_with_context()` en instanciant une session par exemple du dataset.

---

### 4.6 Observabilité (observability.py)

**Bibliothèque interne :** `aiolly[azure]` (Schneider Electric AIHub)

#### 4.6.1 Configuration Dynatrace

- **`setup_observability()`** : configure Aiolly avec `AiollyConfiguration` (cloud/local), `ProjectMetadata` (usecase_name, version, repository_url, environment), et `DynatraceExporterProvider`.
- Export activé uniquement si `WEBSITE_SITE_NAME` est défini (Azure Functions), sinon mode local (pas d'export).
- Les endpoints OTLP sont lus depuis les variables d'environnement `OTEL_EXPORTER_OTLP_*_ENDPOINT`, eux-mêmes résolus depuis Azure Key Vault.

#### 4.6.2 Métriques instrumentées (`AvailableMetrics`)

| Métrique | Type | Description |
|---|---|---|
| `documents.chunking.duration` | Gauge (s) | Durée de découpage des documents |
| `documents.embedding.duration` | Gauge (s) | Durée de génération des embeddings des documents |
| `documents.loading.duration` | Gauge (s) | Durée de chargement des documents |
| `documents.loading.succeeded` | Gauge | Nombre de documents chargés avec succès |
| `documents.loading.failed` | Gauge | Nombre de documents en échec de chargement |
| `embedding.failed` | Counter | Nombre d'embeddings échoués |
| `embedding.api_call` | Counter | Nombre d'appels API OpenAI pour les embeddings |
| `embedding.tokens_used` | Counter (tokens) | Tokens consommés par OpenAI pour les embeddings |
| `orchestrator.number_of_questions` | Counter | Nombre total de questions posées à l'agent |

Les métriques sont initialisées en singleton via `get_all_metrics()` avec lazy init thread-safe.

#### 4.6.3 Traces distribuées

- `LangchainInstrumentor().instrument()` : trace automatique de tous les appels LangChain/LangGraph.
- `FastAPIInstrumentor.instrument_app()` : trace automatique des requêtes HTTP FastAPI.
- `TRACELOOP_TRACE_CONTENT` : contrôle si le contenu des prompts/completions est inclus dans les traces (désactivé en production pour la confidentialité des données).

---

### 4.7 Azure Data Factory (`adf/`)

Quatre pipelines ADF pour automatiser l'ingestion de données :

#### Pipelines

| Pipeline | Description |
|---|---|
| `rag-ingestion-pipeline.json` | Pipeline maître : appelle l'étape de récupération, puis celle de traitement |
| `rag-ingestion-trigger-pipeline.json` | Pipeline déclenché par événement blob |
| `rag-retrieve-documents.json` | Liste les fichiers disponibles dans le stockage |
| `rag-process-documents.json` | Appelle la Function App Processing via HTTP |

**Paramètres du pipeline maître** : `vector_store_type` (défaut "AI_SEARCH"), `container` (défaut "data-store"), `files_path` (défaut "01_raw"), `collection_name`, `API_VERSION`, `EMBEDDING_MODEL`.

#### Linked Services

| Linked Service | Type |
|---|---|
| `AmazonS3.json` | Source de données S3 |
| `AzureADLS.json` | Azure Data Lake Storage Gen2 |
| `AzureFunction.json` | Appel aux Azure Functions |
| `AzureKeyVault.json` | Résolution de secrets |

#### Trigger

- `pdf-trigger.json` : trigger basé sur des événements blob (nouveau PDF déposé) → déclenche automatiquement l'ingestion.

---

### 4.8 Scripts d'administration (`scripts/`)

#### pg_vector_deployment.py

Script de déploiement et initialisation du schéma PostgreSQL/pgvector :
- Activation de l'extension `pgvector`.
- Création des tables LangChain (`langchain_pg_embedding`, `langchain_pg_collection`).
- Création de l'index **HNSW** sur la colonne `embedding`.
- Gestion des droits : création des utilisateurs Azure AD, attribution de rôles `read-only` et `write`.
- Support des administrateurs Azure AD (`--grant-admin-users`).

#### `azure_function_settings.py`

Gestion programmatique des paramètres des Function Apps Azure :
- Lecture, écriture et synchronisation des variables d'environnement des Function Apps.
- Filtrage des clés réservées (listées dans `reserved_settings.py`) pour ne pas écraser les paramètres système Azure.

#### `reserved_settings.py`

Liste des variables d'environnement réservées par Azure Functions et qui ne doivent pas être écrasées lors des déploiements.

---

### 4.9 Infrastructure CI/CD (workflows)

#### Workflows GitHub Actions

| Workflow | Déclencheur | Description |
|---|---|---|
| `ci.yaml` | Pull request vers `develop` | Exécute la suite complète nox (format, lint, typing, test, doc) |
| `cicd-dev.yaml` | Push `develop` ou tag beta | CI + déploiement sur l'environnement dev |
| `cicd-qa.yaml` | Tag QA | CI + déploiement QA |
| `cicd-prv.yaml` | Tag PRV | Déploiement private preview |
| `cd-prd.yaml` | Manuel (`workflow_dispatch`) | Déploiement production (manuel uniquement) |
| `documentation-preview.yml` | PR | Prévisualisation de la doc sur GitHub Pages |
| `tag-official-release.yaml` | Manuel | Tag et publication d'une release officielle |
| `update-from-template.yaml` | Manuel | Récupère les mises à jour du template parent et crée une PR |

Tous les workflows réutilisent des workflows communs (`AIHub-Common/common-workflows@v10`) via `uses:`. L'image Docker est construite et poussée dans un **Azure Container Registry (ACR)** dédié par environnement.

#### Runners self-hosted

Les workflows s'exécutent sur des runners self-hosted Azure (`['self-hosted', 'Azure', 'domain', '{env}', '{region}']`), garantissant l'accès réseau aux ressources Azure privées.

---

### 4.10 Tests (`tests/`)

#### 4.10.1 Tests unitaires (`tests/unit/`)

- `test_adls_loader.py` : test du chargeur ADLS.
- `test_embedder.py` : test de la vectorisation.
- `test_functools.py` : test des utilitaires de batching.
- `test_injection.py` : test de l'injection dans les vector stores.
- `test_processing.py` : test du pipeline principal.
- `test_utils.py` : test des utilitaires communs (UUID, encodage base64, etc.).
- `test_vector_store_ai_search.py` : test du manager AI Search.
- `test_vector_store_postgres.py` : test du manager PGVector.
- Tests côté orchestrateur : `conversational/`, `function_app/`, `server/`, `test_script.py`.

#### 4.10.2 Tests d'intégration (`tests/integration/`)

- Tests du pipeline de processing complet.
- Tests de l'agent conversationnel avec mocks Azure.

#### 4.10.3 Tests end-to-end (`tests/end_to_end/`)

Tests contre une instance déployée :
- `test_server.py` : test complet du cycle session + question + historique. Vérifie la présence de tous les en-têtes de sécurité.
- `test_processing_endpoints.py` : test des endpoints de la Processing Function App.
- `test_adf.py` : test des pipelines Azure Data Factory.
- `e2e_utils.py` : utilitaires partagés.

#### 4.10.4 Tests d'environnement (`tests/environment/`)

- `env_utils.py` : utilitaires pour vérifier la configuration de l'environnement cible.

#### 4.10.5 Configuration des tests

- `conftest.py` racine : fixture `set_endpoint_env_variables` avec `monkeypatch` pour fausses clés OpenAI.
- `pytest-retry` : relances automatiques sur les tests instables.
- `pytest-order` : ordonnancement des tests (via `@pytest.mark.order(after=...)`).
- `freezegun` : gel du temps pour les tests dépendants de dates.
- **Seuil de couverture** : `fail_under=79` (ne pas abaisser).
- **Rapports HTML** : `pytest-html`, `junit2html` pour les rapports ruff/lint.

---

### 4.11 Containerisation (Dockerfile, docker-compose.yml)

#### Dockerfile multi-stage

- **Stage `lean`** : image de base `mcr.microsoft.com/azure-functions/python:4-python3.11`.
  - Installation minimale des packages système (`ca-certificates` uniquement).
  - Variables d'env Azure Functions (`AzureWebJobsScriptRoot`, `AzureWebJobsFeatureFlags=EnableWorkerIndexing`, `WEBSITE_HOSTNAME`).
  - `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`.
  - Installation des dépendances via `requirements.txt` (généré depuis le lock file), puis du wheel Python sans ses dépendances (`--no-deps`).
  - **Passage à un utilisateur non-root** : `useradd appuser && USER appuser` (principe du moindre privilège).
  - Secrets BuildKit (`--mount=type=secret`) pour l'index PyPI privé (JFrog) sans exposition dans les couches.
- **Stage `local`** : hérite de `lean`, ajoute Azure CLI pour le développement local.

#### docker-compose.yml

Trois services pour le développement local :
1. **Azurite** : émulateur Azure Storage (Blob, Queue, Table) sur ports 10000–10002.
2. **`pilot_rag_processing`** : Function App Processing avec volume `~/.azure` pour l'authentification locale.
3. **`pilot_rag_orchestrator`** : Function App Orchestrator.

---

### 4.12 Qualité et sécurité du code

#### Pre-commit (.pre-commit-config.yaml)

- **Gitleaks v8.21.2** : détection automatique des secrets dans le code (clés API, tokens, etc.) avant chaque commit.

#### Linting et formatage

- **Ruff** (≥0.14.1) : linter et formateur Python ultra-rapide. `ban-relative-imports="all"` (imports absolus obligatoires), longueur de ligne ≤120.
- **Hadolint** : linting des Dockerfiles (règles DL4006, SC3040 pour `pipefail`).
- **mypy** : typage statique avec plugin Pydantic. `disallow_any_generics=false`, `check_untyped_defs=true`.

#### Analyse de sécurité

- **Coverity** (coverity.yaml) : analyse statique de sécurité avancée. Exclut les répertoires de tests, documentation, builds. Utilise la liste de checkers sécurité Schneider Electric (`PSOcheckersP1Security.txt`).
- **Gitleaks** : prévention des fuites de secrets.
- **Scans CI** : `force-static-scan` et `force-dependencies-scan` disponibles via `workflow_dispatch`.

---

### 4.13 Gestion des dépendances et versioning

#### `uv` comme gestionnaire de paquets

- `uv` (≥0.8.0) comme backend de virtualenv et de lock file.
- `uv.lock` : lock file déterministe pour des builds reproductibles.
- Registre PyPI privé JFrog (`sd-aihub-common-pypi-prod-fed`) pour les bibliothèques internes Schneider Electric (`gizeh-doc`, `aiolly`).
- `UV_INDEX_COMMON_USERNAME` / `UV_INDEX_COMMON_PASSWORD` : identifiants JFrog injectés depuis l'environnement.

#### Versioning dynamique

- **`uv-dynamic-versioning`** + **Hatchling** comme build backend.
- Version inférée depuis les tags Git (pattern SemVer : `X.Y.Z`, `X.Y.Z-beta.N`).
- `_version.py` généré automatiquement au build et importé via metainfo.py.
- Fallback `"0.0.0-alpha.0"` si fichier absent (mode source).

#### Groupes de dépendances

| Groupe | Contenu principal |
|---|---|
| `core` | pydantic, pydantic-settings, click, loguru, ai-search, aiolly |
| `orchestrator` | fastapi, langchain, langchain-openai, langgraph, openai, uvicorn, azure-cosmos, opentelemetry, langsmith, psycopg, sqlalchemy |
| `processing` | azure-core, azure-functions, azure-functions-durable, azure-search-documents, azure-storage-blob, pypdf, langchain, psycopg, sqlalchemy, tenacity, python-magic |
| `evaluation` | openevals |
| `test` | pytest, coverage, pytest-mock, pytest-retry, pytest-order, freezegun, azure-mgmt-* |
| `dev` | nox, pre-commit |
| `format` | ruff |
| `lint` | ruff, junit2html, hadolint-py |
| `typing` | mypy, typing-extensions |
| `doc` | gizeh-doc, setuptools |
| `deploy` | python-dotenv |

---

### 4.14 Sessions Nox (noxfile.py)

| Session | Description |
|---|---|
| `dev` | Configuration complète de `.venv` + hooks pre-commit |
| `lock` | Mise à jour du lock file |
| `run_local_server` | Lance le serveur FastAPI via uvicorn |
| `rag_create_dataset` | Crée un dataset LangSmith |
| `rag_evaluate` | Évaluation offline RAG via LangSmith |
| `format` | Vérification du formatage Ruff |
| `lint` | Lint Ruff + Hadolint (avec rapports HTML) |
| `typing` | Vérification des types mypy |
| `test` | Tests unitaires + intégration + couverture |
| `test_end_to_end` | Tests E2E contre une instance déployée |
| `doc` | Construction de la documentation MkDocs |
| `docker_build` | Build des images Docker |
| `docker_deploy` | Push des images vers ACR |
| `deploy` | Déploiement complet (settings + images + vector stores) |

---

### 4.15 Documentation (doc)

**Technologie :** MkDocs avec `gizeh-doc` (bibliothèque interne Schneider Electric basée sur Material for MkDocs).

**Pages documentées** :
- `overview.md` : vue d'ensemble du projet
- `getting_started.md` : prérequis et démarrage rapide
- `api_reference.md` : référence API (générée depuis les schémas FastAPI)
- `api_error_codes.md` : codes d'erreur de l'API
- `openapi.md` : spécification OpenAPI
- `contributing.md` : guide de contribution
- `changelog.md` : historique des changements
- `qualimetry_reports.md` : rapports de qualimétrie
- `examples/` : exemples d'utilisation
- `images/` : assets visuels

**Configuration** (`conf.py`) : intègre `error_registry` pour exposer les modèles d'erreur dans la documentation API.

---

## 5. Technologies et bibliothèques — Inventaire exhaustif

### Cloud / Infrastructure Azure

| Technologie | Usage |
|---|---|
| **Azure Functions v4** (Python 3.11) | Runtime des deux applications |
| **Azure Durable Functions** | Orchestration fan-out/fan-in pour l'ingestion |
| **Azure ASGI** (`AsgiFunctionApp`) | Intégration FastAPI dans Azure Functions |
| **Azure Cosmos DB** | Stockage des sessions et historiques de conversation |
| **Azure AI Search (Cognitive Search)** | Base vectorielle principale |
| **Azure Data Lake Storage Gen2 (ADLS)** | Stockage des documents bruts |
| **Azure Blob Storage** | Stockage des blobs |
| **Azure OpenAI Service** | LLM (GPT-4.1) + Embeddings (text-embedding-ada-002) |
| **Azure Container Registry (ACR)** | Registre Docker par environnement |
| **Azure Key Vault** | Gestion des secrets (clés API, tokens OTLP) |
| **Azure API Management (APIM)** | Proxy API / endpoint OpenAI |
| **Azure PostgreSQL Flexible Server** | Backend pgvector alternatif |
| **Azure Data Factory (ADF)** | Pipeline d'orchestration data |
| **Azure Managed Identity / DefaultAzureCredential** | Authentification passwordless |
| **Azurite** | Émulateur Azure Storage local |
| **Amazon S3** | Source de données supportée via ADF |

### Intelligence Artificielle / LLM

| Bibliothèque | Version | Usage |
|---|---|---|
| **LangChain** | ≥1.2.0,<1.3.0 | Framework orchestration LLM |
| **LangChain Community** | ≥0.4.1,<0.5 | `AzureSearch`, `AzureBlobStorageFileLoader` |
| **LangChain OpenAI** | ≥0.3.0,<0.5 | `AzureChatOpenAI`, `AzureOpenAIEmbeddings` |
| **LangChain Postgres** | >0.0.13,<0.2.0 | `PGVector`, `langchain_pg_embedding` |
| **LangGraph** | ≥1.0.0,<1.1.0 | Graphe d'agent ReAct |
| **LangGraph Checkpoint CosmosDB** | ≥0.2.5 | Persistance de l'état du graphe dans CosmosDB |
| **LangSmith** | ≥0.1.125,<1.0.0 | Traçabilité, évaluation, datasets |
| **OpenAI SDK** | ≥1.58.1,<2 | Client OpenAI direct |
| **openEvals** | ≥0.1.3,<0.2 | LLM-as-judge pour l'évaluation RAG |
| **LangChain Text Splitters** | (via langchain) | `RecursiveCharacterTextSplitter` + tiktoken |

### API / Web

| Bibliothèque | Version | Usage |
|---|---|---|
| **FastAPI** | <0.128.1 | Framework REST API |
| **Uvicorn** | ≥0.40,<0.41 | Serveur ASGI |
| **httpx** | ≥0.28.0,<0.29 | Client HTTP async |
| **fastapi-error-manager** | ≥2.1.2,<3 | Gestion centralisée des erreurs |
| **Pydantic** | ≥2.0.0,<3 | Validation des données |
| **Pydantic-settings** | ≥2.1.0,<3 | Configuration depuis variables d'env |

### Observabilité

| Bibliothèque | Usage |
|---|---|
| **aiolly[azure]** | Bibliothèque interne SE : logging, tracing, métriques |
| **OpenTelemetry SDK** | Framework d'observabilité |
| `opentelemetry-instrumentation-fastapi` | Auto-instrumentation FastAPI |
| `opentelemetry-instrumentation-langchain` | Auto-instrumentation LangChain |
| **Dynatrace** | Backend d'observabilité (via OTLP) |
| **Loguru** | Logging structuré |

### Base de données / ORM

| Bibliothèque | Usage |
|---|---|
| **SQLAlchemy** | ORM et gestion des moteurs PostgreSQL |
| **psycopg (v3)** | Driver PostgreSQL avec support async/pool |
| **azure-cosmos** | Client Azure Cosmos DB |
| **pgvector** | Extension PostgreSQL pour les vecteurs |
| **Index HNSW** | Algorithme ANN pour la recherche vectorielle |

### Traitement de documents

| Bibliothèque | Usage |
|---|---|
| **pypdf** | Parsing de fichiers PDF |
| **python-magic** | Détection du type MIME des fichiers |
| **langchain_text_splitters** | Chunking des documents |

### DevOps / Qualité

| Outil | Usage |
|---|---|
| **Nox** | Automatisation des sessions CI/CD |
| **uv** | Gestionnaire de paquets Python |
| **Ruff** | Linter et formateur Python |
| **mypy** | Vérification des types statiques |
| **Hadolint** | Linter de Dockerfiles |
| **pytest** | Framework de tests |
| **coverage** | Mesure de la couverture de code |
| **pytest-mock** | Mocking dans les tests |
| **pytest-retry** | Relances automatiques |
| **pytest-order** | Ordonnancement des tests |
| **freezegun** | Gel du temps pour les tests |
| **Gitleaks** | Détection de secrets dans le code |
| **Coverity** | Analyse statique de sécurité |
| **Hatchling** | Build backend Python |
| **uv-dynamic-versioning** | Versioning dynamique depuis Git |
| **pre-commit** | Hooks de pré-commit |
| **Click** | CLI Python |
| **tenacity** | Retry avec backoff |

### Sécurité

- Authentification passwordless Azure AD via `DefaultAzureCredential`
- Secrets résolus depuis Azure Key Vault (syntaxe `@Microsoft.KeyVault(SecretUri=...)`)
- En-têtes HTTP de sécurité (HSTS, CSP, X-Frame-Options, etc.)
- Utilisateur non-root dans le conteneur
- Secrets BuildKit pour les identifiants PyPI (pas de secrets dans les couches Docker)
- `SecretStr` Pydantic pour les clés API (jamais loguées)
- Gitleaks pour la détection de fuites de secrets

---

## 6. Environnements de déploiement

| Environnement | Abréviation | Accès | Déclencheur |
|---|---|---|---|
| Development | dev | Automatique | Push `develop` ou tag beta |
| Quality Assurance | qa | Automatique | Tag QA |
| Private Preview | prv | ADM account | Tag PRV |
| Production | prd | ADM account | Manuel uniquement |

Chaque environnement possède :
- Son propre Azure Resource Group (`rg-{use_case_name}-{env}-01`)
- Deux Function Apps distinctes (processing + orchestrator)
- Son propre ACR (`acr{use_case_shortname}{env}01`)
- Ses propres ressources CosmosDB, AI Search, PostgreSQL

---

## 7. Modèles architecturaux identifiés

1. **Singleton avec initialisation différée** : `ConversationalCore`, `LangSmith Client`, `PGVectorManager._cached_engine`, métriques OpenTelemetry.
2. **Dependency Injection FastAPI** : `ConversationalCoreBuilder.conversational_core()` injecté dans tous les routeurs.
3. **Fan-out / Fan-in** : parallélisation du chargement et du traitement des documents dans les Durable Functions.
4. **Ingestion événementielle** : trigger ADF sur blob PDF → pipeline automatique.
5. **ReAct Agent** : boucle Reason → Act → Observe via LangGraph pour la génération augmentée.
6. **Checkpointing distribué** : CosmosDB comme backend de persistance de l'état LangGraph.
7. **Multi-vector-store** : abstraction permettant de basculer entre AI Search et PGVector via variable d'environnement.
8. **LLM-as-judge** : évaluation automatique de la qualité RAG sans étiquettes humaines.
9. **Template Cookiecutter** : génération de projet paramétrable avec variables de configuration.

---

## 8. Contraintes et exigences techniques

| Contrainte | Valeur |
|---|---|
| Python | 3.11 strictement (≥3.11, <3.12) |
| Couverture de tests | ≥ 79% (fail_under=79) |
| Longueur de ligne Python | ≤ 120 caractères |
| Imports | Absolus uniquement (ban-relative-imports) |
| Authentification | Azure AD (passwordless) en priorité |
| Secrets | Jamais en dur, toujours via Key Vault |
| Tracing LLM | Désactivé en production (`TRACELOOP_TRACE_CONTENT`) |
| Versioning | SemVer depuis tags Git |
| Build | Reproductible via `uv.lock` |
| Docker | Principe moindre privilège (non-root) |

---

## Conclusion

Le dossier `{{cookiecutter.repository_name}}` est un **archétype industriel complet** pour le déploiement de systèmes RAG sur Azure. Il couvre l'intégralité du cycle de vie d'un projet IA : ingestion de documents (via ADF, Durable Functions, ADLS), vectorisation (AI Search ou pgvector), génération augmentée (LangGraph ReAct + Azure OpenAI), exposition REST (FastAPI), observabilité (Dynatrace via OpenTelemetry), évaluation (LangSmith + openevals), et déploiement (GitHub Actions multi-environnements, Docker, ACR). La base de code applique strictement les bonnes pratiques de sécurité (passwordless, secrets Key Vault, en-têtes HTTP, analyse Coverity/Gitleaks) et de qualité logicielle (Ruff, mypy, Hadolint, pytest avec couverture, nox comme point d'entrée unique CI/CD).

**État :** Cahier des charges exhaustif rédigé (6/6)

L'analyse couvre l'intégralité du dossier `{{cookiecutter.repository_name}}` avec plus de 6 400 mots, structurée en 8 grandes sections :

1. **Vue d'ensemble** du projet RAG Azure Schneider Electric
2. **Structure complète** de tous les fichiers et dossiers
3. **Architecture technique** (deux Function Apps, paradigme RAG)
4. **Inventaire détaillé** de toutes les fonctionnalités (pipeline d'ingestion, agent ReAct, API REST, vector stores, évaluation, observabilité, ADF, scripts d'admin, CI/CD, tests, Docker)
5. **Technologies exhaustives** : plus de 40 bibliothèques Python, plus de 15 services Azure, outils DevOps
6. **Environnements** de déploiement (dev/qa/prv/prd)
7. **Modèles architecturaux** identifiés (singleton, fan-out/fan-in, ReAct, LLM-as-judge…)
8. **Contraintes et exigences** techniques
