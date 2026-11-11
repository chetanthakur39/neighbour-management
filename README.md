# Neighbour Management

A neighbourhood operations dashboard with a React frontend, a Spring Boot API, and a separate Python chatbot service.

## Project layout

- `neighbour-management-frontend/` — React and Vite web app.
- `neighbour-management-backend/` — Java 21, Spring Boot, and MySQL REST API.
- `neighbour-ai/` — PyTorch intent model, command router, and HTTP chat API.

## Requirements

- Node.js and npm
- Java 21 and Maven
- Python 3.12 or another version supported by PyTorch
- MySQL

## Local setup

### Backend and database

Create a MySQL database named `neighbour_management`. Configure these environment variables before starting the backend:

- `DB_URL` — JDBC URL; defaults to the local MySQL URL in `application.properties`.
- `DB_USERNAME` — database user; defaults to `root`.
- `DB_PASSWORD` — database password; set it locally. Credentials are not stored in this repository.
- `APP_CORS_ALLOWED_ORIGINS` — allowed browser origin for the automation endpoint; defaults to `http://localhost:5173`.
- `PORT` — optional server port; defaults to `8080`.

From `neighbour-management-backend/`, run:

```sh
mvn spring-boot:run
```

### Python chatbot

From `neighbour-ai/`, create and activate a virtual environment, install dependencies, and start the API:

```sh
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m model.api_server
```

The chat API listens on port `8000` by default. Set `PORT` to override it. Set `NEIGHBOUR_API_BASE_URL` if the Spring API is not at `http://localhost:8080/api`.

### Frontend

Copy `neighbour-management-frontend/.env.example` to `neighbour-management-frontend/.env.local`, update the service URLs if needed, then:

```sh
cd neighbour-management-frontend
npm ci
npm run dev
```

Create the production bundle with `npm run build`.

## Environment variables

Vite variables are compiled into the browser bundle and must contain public service URLs only. Do not put database passwords, API keys, or other secrets in `VITE_*` variables.

- `VITE_API_BASE_URL` — Spring API base URL, including `/api`.
- `VITE_AI_CHAT_URL` — Python chat endpoint, including `/chat`.
- `NEIGHBOUR_API_BASE_URL` — Spring API base URL used by the chatbot.
- `DB_URL`, `DB_USERNAME`, `DB_PASSWORD`, `APP_CORS_ALLOWED_ORIGINS`, `PORT` — backend connection and runtime settings.

## Vercel deployment

Vercel can host the Vite frontend. Set the project's **Root Directory** to `neighbour-management-frontend`, the build command to `npm run build`, and the output directory to `dist`. Add `VITE_API_BASE_URL` and `VITE_AI_CHAT_URL` in the Vercel project's environment settings.

The Spring Boot API, MySQL database, and PyTorch chatbot are separate services and need reachable hosting of their own. Point the two Vite URLs at those deployed services and allow the Vercel origin in the backend CORS configuration. The Python model server is not deployed by the frontend's Vercel build.

## Notes

- The frontend and services default to localhost for local development.
- Virtual environments, dependencies, build output, and local environment files are excluded from Git.
- The trained checkpoint is `neighbour-ai/model/intent_model.pth`.
- The chatbot training and evaluation JSON data files were unavailable from OneDrive during this copy. They are not needed for model inference.