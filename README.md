# Neighbour Management

A neighbourhood operations dashboard with a React frontend, a Spring Boot API, and a separate Python chatbot service.

## Project layout

- 
eighbour-management-frontend/` — React 19 and Vite web app.
- 
eighbour-management-backend/` — Java 21, Spring Boot, and MySQL REST API.
- 
eighbour-ai/` — PyTorch intent model, command router, and HTTP chat API.

## Requirements

- Node.js and npm
- Java 21
- Python 3.12 or a compatible Python version supported by PyTorch
- MySQL

## Local setup

### 1. Database and backend

Create a MySQL database named 
eighbour_management`. Configure these environment variables before starting the backend:

- `DB_URL` — JDBC connection URL (defaults to the local MySQL URL in `application.properties`).
- `DB_USERNAME` — database user (defaults to `root`).
- `DB_PASSWORD` — database password. Set this locally; credentials are not stored in the repository.
- `PORT` — optional server port (defaults to `8080`).

From 
eighbour-management-backend/`, run `mvn spring-boot:run` with Maven installed.

### 2. Python chatbot

From 
eighbour-ai/`, create and activate a virtual environment, install dependencies, then start the service:

```sh
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m model.api_server
```

The chat service listens on port `8000` by default. Set `PORT` to override it. Set `NEIGHBOUR_API_BASE_URL` to the Spring API URL if the services run on different machines.

### 3. React frontend

Copy 
eighbour-management-frontend/.env.example` to 
eighbour-management-frontend/.env.local`, adjust the URLs if needed, then:

```sh
cd neighbour-management-frontend
npm install
npm run dev
```

Create a production bundle with 
pm run build`.

## Environment variables

Vite variables are compiled into the browser bundle and must contain public service URLs only. Never put database passwords, API keys, or other secrets in `VITE_*` variables.

- `VITE_API_BASE_URL` — Spring API base URL, including `/api`.
- `VITE_AI_CHAT_URL` — Python chat endpoint, including `/chat`.
- `NEIGHBOUR_API_BASE_URL` — Spring API base URL used by the Python chatbot.
- `DB_URL`, `DB_USERNAME`, `DB_PASSWORD`, `PORT` — backend connection and runtime settings.
- `APP_CORS_ALLOWED_ORIGINS` — allowed browser origin for the automation endpoint (defaults to the local Vite origin).

## Vercel deployment

Vercel can host the Vite frontend. Set the project's **Root Directory** to 
eighbour-management-frontend`, use the 
pm run build` command, and the `dist` output directory. Add `VITE_API_BASE_URL` and `VITE_AI_CHAT_URL` in the Vercel project environment settings.

The Spring Boot API, MySQL database, and PyTorch chatbot are separate services and need reachable hosting of their own. Point the two Vite URLs at those deployed services and configure the backend's CORS policy to allow the Vercel site. The Python model server uses PyTorch and is not deployed by the frontend's Vercel build.

## Notes

- The frontend and services default to localhost for local development.
- Virtual environments, dependency folders, build output, and local environment files are excluded from Git.
- The trained model checkpoint is part of `neighbour-ai/model/intent_model.pth`.
- The training and evaluation JSON data files were cloud-only placeholders during this copy and are not included; they are not needed for chatbot inference.
