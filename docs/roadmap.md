# Build roadmap

This project is being developed step by step. I only add infrastructure when a
phase actually needs it, instead of building everything at once.

- [x] **Phase 0** — repo scaffolding, docs, and initial `docker-compose` layout
- [ ] **Phase 1** — Identity service (FastAPI): register, login, RS256 JWT
  issuance, JWKS endpoint
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
