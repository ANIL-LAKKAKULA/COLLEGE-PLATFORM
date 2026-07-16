# Build roadmap — PAR milestones

We build incrementally, but track progress across the *whole system* at each
checkpoint rather than finishing one service before starting the next. Every
PAR includes some work for every service and the Gateway — the amount of
work is realistically uneven (e.g. Notification is nearly empty at 25%
because it has nothing to consume yet), but nothing is fully idle.

Within each cell, items are **core** (committed, must ship) unless tagged
**[stretch]** — stretch items are real, planned work, but the first things
deferred if time runs short near 100%, not core functionality.

Pagination, filtering, and searching are cross-cutting: applied to every
endpoint that lists a resource, across every service — not just Enrollment's
catalog. Each service's row below calls out where it lands for that service.

- [x] **Phase 0** — repo scaffolding, docs, and initial `docker-compose` layout
---

## 25% PAR — Foundation

| Service | Scope |
|---|---|
| **Identity** | RBAC schema + seed migration (6 roles, permissions, `RolePermission`), `POST /users` (hierarchy-checked), assign/revoke role, login issuing RS256 JWT w/ roles+permissions claims, `GET /auth/me`, basic audit (login, create-user, role changes) |
| **Enrollment** | Models/migrations (Branch, Section, AcademicYear, Semester, Course, Student, Faculty), JWT verification wired to Identity's JWKS, basic Branch/Section/Course CRUD |
| **Grading** | Scaffold only — Assessment/Marks models, no business logic yet (depends on Enrollment data existing first) |
| **Notification** | Scaffold + health check only — nothing to consume yet |
| **API Gateway** | Basic routing to Identity + Enrollment, no auth logic yet |
| **Infra** | Docker Compose: Identity + Enrollment DBs/containers; CI skeleton (lint + test) |

## 50% PAR — Core Business Logic

| Service | Scope |
|---|---|
| **Identity** | Self-profile view/update, change-password, refresh token rotation + blacklist (Redis introduced here), forgot/reset password, failed-login + password-change audit history |
| **Enrollment** | Full Student/Faculty CRUD (hierarchy-checked), Assign/Remove HOD, concurrency-safe Course Enrollment (seat limits, `select_for_update`), Faculty/Student Allocation, event publishing (producer only), Attendance (mark/view) |
| **Grading** | Assessment CRUD (mid/internal/final exams, assignments), Enter/Update Marks, ownership-based authorization ("faculty grades only their own course") |
| **Notification** | RabbitMQ consumer skeleton — logs consumed events to console, no real delivery yet |
| **API Gateway** | JWT validation, current-user extraction, token forwarding, correlation ID generation/propagation, request logging |
| **Infra** | Redis + RabbitMQ containers added to Compose; Grading container added |

## 75% PAR — Production Readiness

| Service | Scope |
|---|---|
| **Identity** | Paginated user search/filter (`GET /users`), structured logging integrated, full test coverage push |
| **Enrollment** | Attendance Percentage calculation, Student Promotion, catalog/student/faculty search + filter + sort + pagination, structured logging, standardized exception handling, API versioning, full unit+integration test suite |
| **Grading** | Publish/Lock Marks, Grade/GPA/CGPA calculation, Student & Semester Results (paginated), `GradePublished` event wired to RabbitMQ, full test suite |
| **Notification** | Real delivery (SMTP or simulated) for Welcome/Password-Reset/Result-Published, retry/backoff, idempotent processing, email templates |
| **API Gateway** | Rate limiting, CORS, security headers, health-check aggregation across all services |
| **Infra** | CI/CD builds Docker images, coverage targets enforced; full `docker compose up` brings up the entire stack |

## 100% PAR — Enterprise Polish

| Service | Scope |
|---|---|
| **Identity** | Login-history endpoint (paginated), health/metrics endpoints, final OpenAPI docs polish |
| **Enrollment** | Caching **[stretch — only if a measured bottleneck justifies it]**, final docs |
| **Grading** | Academic History **[stretch]**, Transcripts **[stretch]**, Analytics: subject stats / pass % / top performers / performance reports, all paginated **[stretch]** |
| **Notification** | In-app notifications: user/broadcast/announcements **[stretch]**, dead-letter queue handling, delivery-failure monitoring, notification history (paginated) |
| **API Gateway** | Response caching **[stretch]**, API versioning **[stretch]**, metrics endpoint, final security/config review for deployment |
| **Infra** | Deployment guide, architecture/sequence/ER diagrams, final README, security scan step in CI |

---

Each unit of work still follows: Design → Discuss → Implement → Test →
Refactor → Commit → Push → Code review.
