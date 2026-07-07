# Build roadmap

This project is being developed step by step. I only add infrastructure when a
phase actually needs it, instead of building everything at once.

- [x] **Phase 0** — repo scaffolding, docs, and initial `docker-compose` layout
- [ ] **Phase 1 (in progress)** — Identity Service (FastAPI)

  **Milestone 1 — Foundation: hierarchy, RBAC, audit**
  - [ ] Seed migration: 6 roles (`ADMIN`, `STUDENT_ADMIN`, `FACULTY_ADMIN`,
        `FACULTY`, `STUDENT`, `HOD`), permissions, `RolePermission` mappings
  - [ ] `User`, `Role`, `Permission`, `UserRole`, `RolePermission` models
  - [ ] `POST /users` — hierarchy-checked creation (service layer validates
        creator's permission against requested role)
  - [ ] `POST /users/{id}/roles` (assign), `PATCH /users/{id}/roles/{role_id}/revoke`,
        `GET /users/{id}/roles`
  - [ ] "At least one active role" invariant enforced in service layer
  - [ ] `POST /auth/login` — RS256 JWT with `roles` + flattened `permissions`
        claims, RSA key generation, `GET /.well-known/jwks.json`
  - [ ] `GET /auth/me`
  - [ ] `authorization/`: `require_permission()` FastAPI dependency
  - [ ] `audit/`: `AuditLog` model + write-path for `CREATE_USER`,
        `ASSIGN_ROLE`, `REVOKE_ROLE`, `LOGIN`; `GET /audit-logs`,
        `GET /audit-logs/users/{id}`
  - [ ] Unit + API tests for all of the above

  **Milestone 2 — Self-service & profile management**
  - [ ] `POST /auth/change-password` (+ audit `CHANGE_PASSWORD`)
  - [ ] `GET /users/{id}`, `PATCH /users/{id}` (self-update: full_name,
        phone_number only — email immutable)
  - [ ] `GET /users` (paginated), disable/enable (+ audit)
  - [ ] `GET /auth/me/login-history`

  **Milestone 3 — Hardening**
  - [ ] `POST /auth/logout`, `POST /auth/refresh` with refresh-token rotation
        (Redis introduced here — TTL-based rotation/blacklist store)
  - [ ] Forgot/reset password (reset token logged to console for now — real
        email delivery arrives in Phase 3)
  - [ ] `users/`: search/filter, soft delete (optional)
- [ ] **Phase 2** — Enrollment service (DRF): students, courses, enrollments,
  local JWT verification using JWKS
- [ ] **Phase 3** — Harden Identity: email verification, password reset,
      refresh token rotation + blacklist (Redis introduced here)
- [ ] **Phase 4** — Event-driven wiring: RabbitMQ, Notification Service
      (FastAPI) as a consumer
- [ ] **Phase 5** — Grading Service (DRF), publishes `GradePublished` events
- [ ] **Phase 6** — API Gateway (Nginx): routing, correlation IDs, structured
      logging, health checks
- [ ] **Phase 7** — CI/CD (GitHub Actions per service), coverage targets,
      deployment guide, final README + diagrams

Each phase follows: Design → Discuss → Implement → Test → Refactor → Commit →
Push → Code review.
