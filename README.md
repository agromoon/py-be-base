## Baseline python backend project

### Commands

- **Sync:** `uv sync` · test deps: `uv sync --extra test` · full dev: `uv sync --all-extras`
- **Run app:** `uv run python -m baseline.main` → http://localhost:8000
- **Health:** `curl -s http://localhost:8000/health` · **Ready (DB):** `curl -s http://localhost:8000/ready`
- **Migrations:** `uv run python -m baseline.main migrate`
- **Tests:** `uv run pytest` · with coverage: `uv run pytest --cov`
- **Lint / format / types:** `uv run ruff check .` · `uv run ruff format .` · `uv run mypy src`
- **Pre-commit:** `uv run pre-commit install` · run all: `uv run pre-commit run --all-files`
- **Docker:** `docker build -t baseline .` · `docker run -p 8000:8000 baseline`
- **Docker Compose:** `docker compose up --build` (app + Postgres) · stop: `docker compose down`

### Agents (minimal)

- Tech stack, project structure, code style, things to avoid → see AGENTS.md

### Project structure (standard)

```
src/<package>/
├── api/              HTTP entry: routers, route handlers. Depends on services + schemas.
├── services/         Business logic; orchestrates repositories and domain rules.
├── repositories/     Data access; one impl per entity (add protocol/ABC when multiple impls).
├── models/           ORM entities only (SQLAlchemy). One module per entity.
├── schemas/          Request/response DTOs (Pydantic). Keeps API contract separate from DB shape.
├── middleware/       Cross-cutting: auth, logging, error handling (add when needed).
└── config.py         App settings (or config/ package when split).
```

- **Naming:** Resource-based. `api/users.py`, `UserService`, `UserRepository`, `User` (model), `UserCreate`/`UserRead`/`UserUpdate` (schemas).
- **Flow:** api → services → repositories; models for DB, schemas for in/out.

#### 1. api/ (HTTP entry)
Routers and route handlers; adapt HTTP/JSON to services and schemas.
- *Names:* `users.py` (router), route fns or `UserController` if you want a facade.
- *Patterns:* Proxy (forward to services), Adapter (request → DTOs/commands).

#### 2. services/ (Business logic)
Orchestrate repositories and domain rules.
- *Names:* `UserService`, `OrderProcessor`, `EnrollUserUseCase`.
- *Patterns:* Facade, Strategy (e.g. payment impls), Template Method.

#### 3. repositories/ (Data access)
Abstract DB access; one impl per entity unless you need multiple (then add protocol/ABC).
- *Names:* `UserRepository`, `ProductDao`, `OrderMapper`.
- *Patterns:* Repository, Data Mapper.

#### 4. models/ (ORM entities)
SQLAlchemy entities only; DB shape. No Pydantic here.
- *Names:* `User`, `Invoice`, `Transaction`.
- *Patterns:* Domain model (data + optional behavior).

#### 5. schemas/ (DTOs)
Pydantic request/response; API contract separate from DB.
- *Names:* `UserCreate`, `UserRead`, `UserUpdate`, `UserBase`.
- *Patterns:* DTO, validation at boundary.

#### 6. middleware/ (Cross-cutting)
Auth, logging, error handling. Add when needed.
- *Names:* `AuthGuard`, `LoggingMiddleware`, `ErrorHandler`.
- *Patterns:* Chain of Responsibility, Decorator.

#### 7. config
App settings. Single `config.py` or `config/` package when split.
