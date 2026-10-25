# Timisoara Digital Map

> **Working title:** Timisoara Digital Map - an AI-assisted, event-driven map of the city.
>
> **Project status:** Concept / early development. The features and architecture below describe the intended system; they should not be interpreted as implemented until the corresponding code and tests exist.

A civic mapping platform that builds a continuously updated, community-informed picture of Timisoara. People can submit observations from places around the city, attach descriptions and photos, and help document things happening in the urban environment. The platform uses AI-assisted matching to identify observations that may refer to the same real-world event, groups related reports into a canonical event, and visualizes spatial patterns through an interactive 2D map and filtered heatmaps.

The goal is not to recreate every building or simulate the physical city. It is to create a useful **digital layer of what people observe happening in the city**, while preserving uncertainty, evidence, and the difference between a submitted observation and a verified event.

## Contents

- [Vision](#vision)
- [Problem](#problem)
- [Core concepts](#core-concepts)
- [Main features](#main-features)
- [AI and computer vision](#ai-and-computer-vision)
- [2D map and spatial visualization](#2d-map-and-spatial-visualization)
- [Architecture](#architecture)
- [Technology stack](#technology-stack)
- [Data model](#data-model)
- [Research and evaluation](#research-and-evaluation)
- [Planned API](#planned-api)
- [Repository structure](#repository-structure)
- [Local development](#local-development)
- [Roadmap](#roadmap)
- [Trust, privacy, and limitations](#trust-privacy-and-limitations)
- [Documentation and references](#documentation-and-references)

## Vision

Cities generate a constant stream of local information: damaged infrastructure, overflowing bins, blocked sidewalks, temporary closures, public-space problems, environmental observations, community activities, and other events. That information is often scattered across social media, message groups, forms, and individual reports. Similar reports can be difficult to connect, and the overall spatial pattern is hard to see.

**Timisoara Digital Map aims to connect these isolated observations into a coherent, searchable view of the city.** A resident should be able to open a map, explore known events, submit a new observation with its location, and understand whether others have reported something similar. Over time, aggregated and carefully qualified data can help residents, researchers, community groups, and potentially city stakeholders understand where particular kinds of events are being reported and how those reports change.

### Product principles

1. **Observation first.** A user-submitted report is evidence that someone observed something; it is not automatically proof that the underlying claim is true.
2. **One event, multiple observations.** Several people may independently report the same real-world issue. These reports should be linked rather than displayed as unrelated duplicates.
3. **AI assists; it does not declare truth.** Models can suggest categories and candidate matches. Verification and moderation remain explicit parts of the workflow.
4. **Make uncertainty visible.** The interface should distinguish new, unreviewed, community-supported, and moderator-reviewed information.
5. **A heatmap is not a danger map.** Heatmaps show the concentration of reports under selected filters. They do not automatically indicate severity, risk, or the full state of the city.
6. **Start with Timisoara, design for extension.** The first release focuses on a manageable set of categories and one city, while keeping the core data model reusable elsewhere.

## Problem

A conventional map is good at showing streets, buildings, and points of interest, but it does not necessarily show current, community-reported events. A basic reporting application can collect information, but may accumulate duplicates and make city-wide patterns difficult to understand.

This project combines three capabilities:

- **Structured citizen observations** with a location, timestamp, description, optional image, category, and status.
- **Event resolution** that connects reports likely to refer to the same real-world occurrence.
- **Spatial analysis and visualization** that makes event locations and reporting patterns explorable over time.

Potential categories include:

- Infrastructure: potholes, damaged sidewalks, broken streetlights.
- Mobility: blocked paths, cycling hazards, temporary road obstructions.
- Environment: overflowing bins, localized flooding, visible pollution observations.
- Public spaces: damaged equipment, accessibility barriers, temporary closures.
- Community: local events and other useful, non-emergency activities.

The initial implementation should select a small, well-defined subset instead of attempting to classify every possible kind of urban event from day one.

## Core concepts

### Observation

An **observation** is one contribution made by a user. It preserves the original report, including its description, coordinates, creation time, optional photo, model suggestions, and review status. An observation should not be silently rewritten just because it is linked to another report.

### Canonical event

An **event** represents the current best-known record of a real-world occurrence. It may contain a summarized description, estimated location, category, active status, verification level, and links to one or more observations.

For example, three people may report the same pothole from slightly different positions and at different times. The system can propose linking all three observations to one canonical event while retaining each original report as evidence.

### Event resolution

**Event resolution** is the process of deciding whether a new observation matches an existing event or should start a new one. It combines spatial, temporal, textual, and visual evidence. This is the central AI-assisted feature and the principal candidate for the thesis research contribution.

### Verification status

A report can be unreviewed, community-supported, moderator-reviewed, resolved, or archived, depending on the final workflow. A high model similarity score alone must not be treated as verification. Multiple reports can increase confidence, but the system should account for report independence, evidence quality, recency, and possible coordinated abuse.

## Main features

### 1. Interactive city map

- Explore the Timisoara map by panning and zooming.
- Display canonical events as map features rather than showing every raw observation as an independent event.
- Filter by category, time range, status, and verification level.
- Open an event to inspect its summary, location, status, and linked observations.
- Use marker clustering at wider zoom levels to prevent visual clutter.

### 2. User reporting

- Submit a report with a title or short description, category, location, and optional image.
- Select the location on the map or use device location when permission is granted.
- Review the report before submitting it.
- Receive a clear indication that a report is pending review or has been linked to an existing event.
- Add further observations to support an event without requiring users to create duplicate event records manually.

### 3. AI-assisted duplicate detection

When a new observation arrives, the backend can find nearby candidate events using spatial and temporal filters, then rank the candidates based on available evidence such as text similarity, image similarity, and category compatibility. The result is a recommendation, not an unquestionable decision.

Possible outcomes:

- **Likely match:** suggest linking the observation to an existing event, subject to the chosen confidence and moderation policy.
- **Uncertain match:** queue the candidates for manual review.
- **No credible match:** create a new provisional event or leave the observation awaiting review.

### 4. Heatmaps and city insights

- Show where reports are concentrated for a selected category and time period.
- Compare reporting patterns over different periods.
- Provide counts and trends by map area or administrative neighborhood where suitable boundary data is available.
- Make filters and legends explicit so users understand what is included in the visualization.

A heatmap and marker clustering solve different problems. **Clustering** groups nearby markers to keep the map readable; a **heatmap** visualizes spatial concentration across a broader area.

### 5. Moderation dashboard

A web dashboard will allow authorized moderators to review new observations, inspect suggested matches, confirm or reject event links, change event status, handle suspected spam, and inspect a basic audit history. Moderator actions should be recorded so decisions can be explained and evaluated later.

## AI and computer vision

AI should solve a real product problem: reports that describe the same event often use different wording, photos, and locations. A rules-only system based only on geographical distance is easy to implement, but can miss reports from different sides of an incident or incorrectly merge separate nearby events. The project will investigate whether text and image representations improve matching quality.

### Proposed AI pipeline

1. **Input validation:** validate the report and check uploaded files before model inference.
2. **Optional category suggestion:** a pretrained image-classification model can suggest a broad category from the photo. The user or moderator can correct it.
3. **Text representation:** encode the description into a semantic embedding so differently worded reports can still be compared.
4. **Image representation:** use a vision model, potentially a CLIP-style image encoder, to obtain an embedding describing visual content. A separate classifier may be evaluated for a narrow set of supported categories.
5. **Candidate retrieval:** use PostGIS to find geographically and temporally plausible events before running more expensive comparisons.
6. **Candidate ranking:** combine spatial distance, time compatibility, text similarity, image similarity, and category compatibility into a score or ranking model.
7. **Decision policy:** suggest a match, request moderator review, or keep the observation separate according to calibrated thresholds and the verification workflow.
8. **Logging and evaluation:** store relevant model outputs, model version, match decision, and later human review outcome for offline analysis. Avoid retaining unnecessary personal information.

### Recommended model strategy

Start with **pretrained models and embeddings**, not training a large vision model from scratch. PyTorch and Hugging Face Transformers can support model inference and controlled experiments. The exact checkpoint should be selected after reviewing its task suitability, license, computational requirements, and performance on the project's own data.

A practical experiment plan is:

- **Baseline A - geographic rules:** candidate events within a selected radius and time window.
- **Baseline B - geography + time + category:** a stronger non-neural rule-based method.
- **Model C - geography + text embeddings:** evaluate whether descriptions improve matching.
- **Model D - geography + text + image embeddings:** evaluate whether image information improves matching further.

Image classification is a supporting capability, not the sole definition of the project. A photograph cannot reliably establish every property of an event, and visual similarity alone can merge separate occurrences. Model output must be treated as evidence with uncertainty, not as proof.

### Thesis research question

> **How much can text and image similarity improve the precision and recall of duplicate-event matching compared with a spatiotemporal rule-based baseline?**

The experiment should measure both successful matches and harmful mistakes. A false merge can hide two genuinely distinct events inside one record; a missed duplicate can leave multiple records for the same occurrence.

## 2D map and spatial visualization

The project needs an **interactive 2D map engine**, not a full simulation engine. The map supplies the geographic canvas and renders roads, map features, event markers, clusters, and heatmap layers. The backend and spatial database supply the event data and perform geographic filtering and aggregation.

### Proposed map technologies

- **MapLibre GL JS** for the browser-based map. It renders interactive maps from vector tiles and supports data-driven styling, marker layers, clusters, and heatmap layers.
- **OpenStreetMap-compatible basemap data** through a suitable tile provider or a properly configured service. The selected source must meet its usage terms and attribution requirements; the project should not assume public demo tiles are suitable for production traffic.
- **PostgreSQL + PostGIS** for storing coordinates and running spatial queries, such as finding nearby events or aggregating results inside a viewport.
- **GeoJSON** as a straightforward interchange format for delivering point and other geographic features to the map.
- **A mobile map component** for the React Native reporting app. The final component should be chosen after validating Expo/native compatibility and its fit for the required map interactions. Map rendering on mobile does not have to use the exact same library as the web dashboard.

### Map views

1. **Events view:** one marker for each canonical event, with filters and a detail panel.
2. **Clustered view:** nearby markers are grouped at lower zoom levels; zooming in reveals individual events.
3. **Heatmap view:** visualizes report/event concentration for the active filters.
4. **Insights view:** presents aggregate counts and trends over time, ideally alongside a clear explanation of the data coverage.

### Is this a city simulation?

Not in the first version. The system creates an event-driven **digital representation** of the city over a geographic basemap; it does not simulate vehicle physics, pedestrian movement, city infrastructure behavior, or the future state of Timisoara. Those would require different data and dedicated simulation models and are explicitly outside the MVP.

## Architecture

The recommended approach is a **modular monolith with a separate AI worker**, rather than a large microservices architecture. This keeps deployment and debugging manageable for an individual thesis project while allowing inference tasks to run asynchronously.

```text
┌────────────────────────┐        ┌────────────────────────┐
│ Mobile app             │        │ Web map + admin panel  │
│ Expo / React Native    │        │ React / Next.js        │
└───────────┬────────────┘        └───────────┬────────────┘
            │ HTTPS / JSON / uploads          │
            └────────────────┬────────────────┘
                             ▼
                    ┌─────────────────┐
                    │ FastAPI backend │
                    │ auth, reports,  │
                    │ events, review  │
                    └───────┬─────────┘
                            │
             ┌──────────────┼────────────────┐
             ▼              ▼                ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │ PostgreSQL   │ │ Object store │ │ Redis queue  │
     │ PostGIS +    │ │ S3 / MinIO   │ │ background   │
     │ pgvector     │ │ images       │ │ jobs         │
     └──────────────┘ └──────────────┘ └──────┬───────┘
                                             ▼
                                    ┌──────────────────┐
                                    │ Python AI worker │
                                    │ vision, embeddings│
                                    │ candidate ranking │
                                    └──────────────────┘
```

### Request flow: submitting an observation

1. The client sends report fields and an optional photo to FastAPI.
2. The API validates the request, stores the original observation, and places image-processing/matching work on the queue if asynchronous processing is required.
3. The worker creates model outputs and searches for plausible event matches.
4. The matching service records its candidates and recommendations.
5. The event workflow applies the configured decision policy: auto-link only when explicitly permitted by tested thresholds, otherwise request confirmation or moderation.
6. The web and mobile clients retrieve the updated observation/event status.

### Responsibility boundaries

- **Frontend:** screens, map controls, filters, report composition, status display, and admin workflows.
- **FastAPI:** authentication, validation, permissions, report/event operations, and API contracts.
- **PostGIS:** geographic storage, indexing, and spatial candidate filtering.
- **AI worker:** model inference, embedding generation, candidate scoring, and scheduled reprocessing if needed.
- **Object storage:** uploaded photos and derived assets, separated from relational metadata.
- **Redis + job queue:** optional asynchronous processing so slower model inference does not block ordinary API requests.

## Technology stack

| Layer | Recommended technology | Why it fits |
|---|---|---|
| Web interface | React + Next.js + TypeScript | Map explorer, filters, event details, moderation and insights dashboard. |
| Mobile client | React Native + Expo + TypeScript | Cross-platform reporting flow, camera/file upload, and optional device location. |
| API | Python + FastAPI + Pydantic | Typed REST endpoints, request validation, and straightforward integration with Python AI libraries. |
| Main database | PostgreSQL | Reliable storage for users, observations, events, audit history, and moderation records. |
| Geospatial database features | PostGIS | Spatial types, indexes, distance searches, and geographic filtering/aggregation. |
| Embedding storage/search | pgvector | Store and compare text/image vectors within PostgreSQL before a separate vector database is justified. |
| Map rendering | MapLibre GL JS on web; mobile map library selected after compatibility testing | Interactive 2D map, styled feature layers, clusters, and heatmaps. |
| AI / computer vision | PyTorch + Hugging Face Transformers; evaluate CLIP-style image embeddings and an appropriate classifier | Reuse pretrained models and benchmark them against simple baselines. |
| Background work | Redis + Celery or RQ | Queue model inference and other slow jobs outside the request/response path. Choose one queue framework for the MVP. |
| Image storage | S3-compatible object storage, such as MinIO locally | Keep images out of database rows and support access controls. |
| Development environment | Docker Compose | Reproducible local dependencies for the database, queue, and storage. |
| Testing | pytest; frontend unit tests; Playwright for critical browser flows | Verify business rules, matching behavior, and key user workflows. |
| CI | GitHub Actions | Run linting, tests, and build checks on changes. |

### Why React and FastAPI?

React supports component-based interfaces and is a good fit for an interactive map, report forms, event panels, filters, and administration screens. Next.js provides the web application structure, while React Native with Expo reuses the React and TypeScript development model for a mobile reporting client.

FastAPI keeps the API in Python, where the computer-vision and machine-learning ecosystem is directly available. It also encourages explicit request/response schemas, which helps keep the mobile app, web app, and backend aligned.

### Why PostGIS and pgvector?

The project has two different search requirements:

- **Geospatial search:** retrieve events within a radius or map viewport. PostGIS handles this kind of geographic query.
- **Semantic search:** find descriptions or images that are similar even if they are not exact matches. Vector embeddings and pgvector can help retrieve semantically similar candidates.

These technologies complement one another. The recommended workflow is to reduce the candidate set geographically first, then rank the remaining candidates with semantic and temporal evidence.

## Data model

The schema will evolve during implementation, but the initial model should include:

| Entity | Purpose | Example fields |
|---|---|---|
| `users` | Accounts and roles | `id`, `display_name`, `role`, `created_at` |
| `observations` | Original user-submitted reports | `id`, `user_id`, `description`, `category_id`, `location`, `observed_at`, `created_at`, `image_key`, `review_status` |
| `events` | Canonical record of a real-world occurrence | `id`, `title`, `summary`, `category_id`, `estimated_location`, `status`, `verification_level`, `first_seen_at`, `last_seen_at` |
| `event_observations` | Links observations to candidate/confirmed events | `event_id`, `observation_id`, `match_score`, `link_status`, `reviewed_by`, `created_at` |
| `event_status_history` | History of event state changes | `event_id`, `old_status`, `new_status`, `actor_id`, `reason`, `created_at` |
| `moderation_actions` | Audit of moderator decisions | `id`, `moderator_id`, `target_type`, `target_id`, `action`, `reason`, `created_at` |
| `model_runs` (optional) | Traceable AI output | `id`, `observation_id`, `model_name`, `model_version`, `result_summary`, `created_at` |

Use geographic database types for coordinates rather than treating latitude and longitude as ordinary text. Keep an observation's original location and text separate from the canonical event's estimated location and summary. This preserves evidence and allows the event record to be updated without erasing the original reports.

## Research and evaluation

A strong thesis should evaluate the matching system, not only demonstrate that the map works. The dataset and evaluation protocol should be planned early, because model quality cannot be measured credibly without labeled examples.

### Dataset plan

- Create a small, documented dataset of observations and pairs judged to be **same event** or **different events**.
- Use a transparent annotation guide and, where possible, have ambiguous cases reviewed by more than one person.
- Avoid including private information or publishing photos without appropriate permission.
- If real local data is unavailable, start with clearly labeled synthetic or manually constructed cases, then describe their limitations honestly.
- Split data by underlying event (and, where practical, by time/area) so photos or reports from the same event do not leak between training and test sets.

### Baselines and metrics

Compare geographic-only matching with increasingly rich approaches, for example geography + time, geography + text, and geography + text + image. Evaluate:

- **Precision:** how often proposed matches are correct.
- **Recall:** how many true duplicates are found.
- **F1-score:** a combined measure of precision and recall.
- **False-merge rate:** distinct real-world events incorrectly combined.
- **Missed-duplicate rate:** duplicate observations that remain unlinked.
- **Precision@k / Recall@k:** whether the correct event appears near the top of the candidate ranking.
- **Latency:** time required to retrieve and rank candidates under representative conditions.

Include an error analysis with examples of confusing cases: similar-looking objects at different locations, repeat incidents at the same site, vague descriptions, old photos, and events that move or change over time. Report performance per category when the dataset supports it. Do not present results from a small or synthetic dataset as proof that the system is reliable city-wide.

## Planned API

These are proposed endpoint names, not a promise that the routes already exist. Use a versioned prefix such as `/api/v1` and document final schemas in the FastAPI-generated OpenAPI docs.

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/v1/observations` | Submit an observation and optional image. |
| `GET` | `/api/v1/observations/{observation_id}` | Retrieve one observation and its processing status. |
| `GET` | `/api/v1/events` | Query canonical events, with viewport, category, status, and time filters. |
| `GET` | `/api/v1/events/{event_id}` | Retrieve event details and linked observations. |
| `POST` | `/api/v1/events/{event_id}/observations` | Submit supporting evidence or link an observation through the authorized workflow. |
| `GET` | `/api/v1/analytics/heatmap` | Return filtered geographic data for heatmap rendering. |
| `GET` | `/api/v1/analytics/summary` | Return aggregate counts/trends for the selected area and time range. |
| `GET` | `/api/v1/admin/review-queue` | Retrieve observations and proposed matches awaiting review. |
| `POST` | `/api/v1/admin/match-decisions` | Confirm, reject, or defer a proposed match with an audit record. |

Protect write and moderation routes with authentication and role-based authorization. Validate map bounds and time filters, paginate large responses, and return only data needed by the client.

## Repository structure

A monorepo is convenient while the project is being developed. The folders below are a proposed structure and can be adjusted as the implementation evolves.

```text
.
├── apps/
│   ├── web/                  # Next.js map explorer and admin dashboard
│   └── mobile/               # Expo / React Native reporting app
├── services/
│   ├── api/                  # FastAPI application and domain logic
│   └── ai-worker/            # Python vision, embeddings, and matching pipeline
├── packages/
│   └── shared-types/         # Shared API types/schemas where practical
├── infra/
│   ├── docker/               # Local service configuration
│   └── compose.yaml          # Local database, queue, and object storage
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   └── evaluation-protocol.md
├── experiments/              # Reproducible matching experiments and analysis
├── .env.example
├── .gitignore
└── README.md
```

Do not commit actual `.env` files, credentials, private user data, uploaded photos, or large datasets containing personal information. Commit dataset documentation, anonymized examples, and reproducible scripts instead.

## Local development

The commands below describe the intended setup. They may need small adjustments as the repository scaffold and exact package choices are created.

### Prerequisites

- Git
- Node.js and the package manager selected for the frontend
- Python 3.12+ (select and pin the exact supported version when dependencies are set up)
- Docker and Docker Compose

### 1. Clone and configure

```bash
git clone <repository-url>
cd <repository-directory>
cp .env.example .env
```

Fill the environment values locally. Never commit the populated `.env` file.

### 2. Start local infrastructure

Once `infra/compose.yaml` has been added, start the database, Redis, and object storage services:

```bash
docker compose -f infra/compose.yaml up -d
```

Apply database migrations, including the required PostGIS and (if used) pgvector extensions. The exact migration command will depend on the migration tool chosen for the API.

### 3. Run the API

After the FastAPI service has been scaffolded and its dependencies installed, a typical development command is:

```bash
cd services/api
uvicorn app.main:app --reload
```

FastAPI exposes interactive API documentation at `/docs` by default when the development server is running.

### 4. Run the AI worker

Install the worker's Python dependencies and start the selected queue worker using the command defined by its configuration. Keep model downloads and inference configuration separate from API request handling.

### 5. Run the web and mobile apps

Install dependencies in `apps/web` and `apps/mobile`, then start the corresponding Next.js and Expo development servers. Add the exact package-manager commands once the frontend workspaces are initialized.

### Configuration variables

The following names are a suggested starting point for `.env.example`; final names should match the implemented settings.

```dotenv
APP_ENV=development
API_PREFIX=/api/v1
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/citymap
REDIS_URL=redis://localhost:6379/0
OBJECT_STORAGE_ENDPOINT=http://localhost:9000
OBJECT_STORAGE_BUCKET=observations
OBJECT_STORAGE_ACCESS_KEY=change-me
OBJECT_STORAGE_SECRET_KEY=change-me
MODEL_DEVICE=cpu
MODEL_CACHE_DIR=.model-cache
WEB_BASE_URL=http://localhost:3000
```

Use generated secrets and local-only credentials. Do not put private server secrets in frontend environment variables; browser-visible variables are not secrets.

## Roadmap

A realistic first release can be developed in phases. Reassess scope at the end of each phase rather than trying to implement every category and model at once.

| Phase | Deliverable |
|---|---|
| 1. Foundations | Requirements, category definitions, privacy approach, architecture, data model, evaluation protocol, and initial labeled examples. |
| 2. Spatial backend | FastAPI project, PostgreSQL/PostGIS, authentication, observation submission, and event querying. |
| 3. Map experience | Web map, event markers, filters, event detail panel, and marker clustering. |
| 4. Reporting workflow | Mobile report form, location selection, image upload, and clear processing/status states. |
| 5. Review and event model | Canonical event workflow, linked observations, moderator dashboard, and audit history. |
| 6. AI matching baseline | Geographic/temporal candidate retrieval and simple rule-based ranking. Measure this before adding models. |
| 7. Vision and semantic matching | Generate text/image embeddings, introduce candidate ranking, and compare variants against the baseline. |
| 8. Heatmaps and insights | Category/time filters, map heatmap, aggregate counts, and interpretation guidance. |
| 9. Evaluation and hardening | Labeled test set, error analysis, API/client tests, security checks, usability feedback, and reproducible results. |
| 10. Final demonstration | Deployed or reproducible demo, documentation, limitations, and thesis results. |

### MVP scope

The minimum defensible release should include:

- A 2D map focused on Timisoara.
- A small set of supported event categories.
- Submitting observations with a location, description, and optional photo.
- Canonical events with linked observations.
- AI-assisted duplicate candidates, with uncertain cases sent to review.
- Category/time-filtered map layers and a heatmap.
- A basic web moderation workflow.
- A reproducible comparison of matching methods.

### Explicitly out of scope for the first version

- A full 3D recreation of Timisoara.
- Live traffic ingestion or a dynamic traffic simulator.
- Predictive urban planning or autonomous decisions.
- Guaranteed real-time integration with municipal systems.
- Automatic verification of truth from a photo.
- Nationwide scale, complex reputation scores, or a large microservices deployment.

## Trust, privacy, and limitations

- **Moderation:** rate-limit submissions, provide report/removal workflows, and audit moderator decisions.
- **Uncertainty:** distinguish unreviewed observations from reviewed events. Do not equate model confidence or report volume with factual truth.
- **Privacy:** collect only information needed for the service, restrict access to uploaded media, and establish retention/deletion rules. Consider removing unnecessary image metadata before storage.
- **Security:** validate and limit uploads, verify file types, enforce authorization on moderation actions, protect secrets, and log security-relevant events without logging sensitive content unnecessarily.
- **Coverage bias:** some areas and groups may submit more reports than others. A quiet area on the map does not imply that no issue exists there.
- **Category boundaries:** visual models can confuse categories and struggle with low-quality, dark, obstructed, or out-of-context photos. Always allow human correction.
- **Map and tile licensing:** comply with the terms, attribution rules, and usage limits of any basemap or geocoding provider.
- **Emergency safety:** the platform is not an emergency dispatch service. The UI should direct users to official emergency channels for immediate danger.

The platform should describe its output as a **map of available observations and inferred event groupings**, not as a complete or authoritative representation of every condition in the city.

## Documentation and references

- [React documentation](https://react.dev/) - UI components and the React programming model.
- [React: Creating an app](https://react.dev/learn/creating-a-react-app) - framework guidance, including Expo for native apps.
- [Expo documentation](https://docs.expo.dev/) - React Native application tooling and development workflow.
- [FastAPI documentation](https://fastapi.tiangolo.com/) - Python API development and request validation.
- [MapLibre GL JS documentation](https://maplibre.org/maplibre-gl-js/docs/) - interactive browser maps.
- [MapLibre heatmap example](https://maplibre.org/maplibre-gl-js/docs/examples/create-a-heatmap-layer/) - heatmap rendering.
- [MapLibre cluster example](https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/) - marker clustering.
- [Hugging Face Transformers: image classification](https://huggingface.co/docs/transformers/tasks/image_classification) - pretrained and fine-tuned image classification workflows.
- [pgvector](https://github.com/pgvector/pgvector) - vector similarity search in PostgreSQL.
- [PostGIS documentation](https://postgis.net/documentation/) - geographic data types and spatial operations.

---

**Summary:** Timisoara Digital Map combines a community observation workflow, a spatially aware event database, AI-assisted duplicate detection, and an interactive 2D map. The map makes observations understandable; the AI helps connect related reports; and the verification workflow keeps the system honest about what is known, what is inferred, and what still needs review.
