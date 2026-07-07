# College Management Platform

A small college platform backend built as a phase-based microservices proof of
concept. Right now the repo is mostly scaffolding and planning, not a finished
system.

See `docs/roadmap.md` for the phase plan and `docs/adr/` for why key decisions
were made.

## Services

| Service | Framework | Owns | Status |
|---|---|---|---|
| Identity | FastAPI | Users, auth, JWT issuance | Pending |
| Enrollment | Django REST Framework | Students, courses, enrollments | Pending |
| Grading | Django REST Framework | Assignments, grades | Pending |
| Notification | FastAPI | Async event notifications | Pending |

## Architecture

The idea is a gateway in front of several backend services. The gateway will
route requests to the right service, and services will keep their own data
and responsibilities.

The current plan avoids cross-service synchronous calls except for token
validation with a public key. Later phases add async messaging for events like
course enrollment or grade publication.

## Repo structure

This repo is a monorepo by design. It makes the project easier to manage now,
and it still keeps the services logically separate.

```
college-platform/
├── docker-compose.yml       # local dev compose file
├── services/
│   ├── identity/            # FastAPI auth service
│   ├── enrollment/          # DRF course/enrollment service
│   ├── grading/             # DRF grading service
│   └── notification/        # FastAPI notification service
├── gateway/                 # API gateway / routing layer
└── docs/
    ├── roadmap.md
    └── adr/                 # Architecture Decision Records
```

## Local development

The repo currently only contains structure and documentation. The actual
services are planned, but not implemented yet.

## Status

🚧 Phase 1 — designing the Identity Service's first API (`POST /auth/register`).
