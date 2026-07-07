# Identity Service (FastAPI)

**Status:** 🚧 In progress — Phase 1, Milestone 1

**Owns:** users, authentication, JWT issuance (RS256), data-driven RBAC
(roles: Admin, StudentAdmin, FacultyAdmin, Faculty, Student, HOD), audit log.

## Why FastAPI
Auth is I/O-light and latency-critical — every other service depends on
tokens this service issues. FastAPI's async support and minimal overhead fit
a thin, high-traffic service better than DRF's heavier batteries (admin
panel, ORM-heavy serializers), which this service doesn't need.

## Design decisions (see ADRs at repo root for full reasoning)
- No public self-registration — accounts are provisioned via a fixed
  creation hierarchy. See `docs/adr/0003-admin-provisioned-accounts.md`.
- RS256 asymmetric JWT, verified locally by every other service — no DB
  lookup required. See `docs/adr/0002-jwt-strategy.md`.
- Data-driven RBAC: `Role`/`Permission` are fixed, seeded via migration;
  membership lives in `UserRole` (supports multiple roles per user, e.g.
  Faculty + HOD); permissions are flattened into the JWT at login. See
  `docs/adr/0004-rbac-design.md`.

## Data model

```
User            id, email, hashed_password, full_name, phone_number,
                date_of_birth, is_active, created_at, updated_at,
                last_login_at
                (no role column — see UserRole)

Role            id, name        -- fixed: ADMIN, STUDENT_ADMIN,
                                    FACULTY_ADMIN, FACULTY, STUDENT, HOD

Permission      id, name        -- fixed, seeded via migration

UserRole        user_id, role_id, assigned_by, assigned_at,
                revoked_by, revoked_at
                -- soft-deleted (revoked_at) to preserve history;
                -- a user must always have >= 1 active role

RolePermission  role_id, permission_id
```

## Modules (this is how the codebase itself is organized — not just endpoints)

| Module | Responsibility |
|---|---|
| `auth/` | Login, logout, refresh, change/forgot/reset password, `GET /auth/me` |
| `users/` | User lifecycle: create, view, update, disable/enable, list |
| `roles/` | Assign/revoke roles on a user, view a user's roles |
| `permissions/` | Internal only for now — no CRUD API (fixed/seeded, see ADR 0004) |
| `authorization/` | Not endpoint-facing — `require_permission()` dependency used by other modules to protect routes |
| `audit/` | Write-path called from other modules on sensitive actions; read endpoints `GET /audit-logs`, `GET /audit-logs/users/{id}` |

## Milestone plan for this service

- **Milestone 1 (current):** seed migration, `User`/`Role`/`Permission`/
  `UserRole`/`RolePermission` models, `POST /users` (hierarchy-checked),
  role assign/revoke, `POST /auth/login` (JWT with roles+permissions),
  `GET /auth/me`, `require_permission()`, audit logging + read endpoints
- **Milestone 2:** change-password, self-profile view/update, paginated
  user listing, disable/enable, login history
- **Milestone 3:** logout, refresh token rotation (Redis introduced here),
  forgot/reset password, search/filter, soft delete

## Planned folder structure

```
identity/
├── app/
│   ├── api/                # route handlers, grouped by module above
│   ├── core/                # config, security (RSA key loading/signing)
│   ├── models/               # SQLAlchemy models
│   ├── schemas/               # Pydantic request/response schemas
│   ├── services/               # business logic + authorization checks,
│   │                             wrapped in transactions
│   └── selectors/               # read-only queries (e.g. flatten
│                                   permissions for JWT at login)
├── tests/
├── keys/                     # RSA key pair (gitignored — generated locally)
├── Dockerfile
├── requirements.txt
└── .env.example
```

See `../../docs/skills-map.md` for the full skills breakdown across all services.
