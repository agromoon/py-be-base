## Baseline python backend project

### Development

- **Tests only:** `uv sync --extra test` then `uv run pytest`
- **Full dev (tests + lint/format/type-check):** `uv sync --all-extras`

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
