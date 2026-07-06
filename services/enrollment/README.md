# Enrollment Service (Django REST Framework)

**Status:** Not started — Planned in future

**Owns:** students, course catalog, enrollments, prerequisites, and capacity
rules.

This service is a good fit for Django REST Framework because the domain is
relational and has a lot of business rules. DRF and Django ORM make it easier
to model relationships safely and keep validation organized.

## Planned structure
```
enrollment/
├── config/               # Django project settings
├── apps/
│   └── enrollment/
│       ├── models/       # database models
│       ├── serializers/  # input/output validation
│       ├── services/     # business rules and workflows
│       ├── selectors/    # read-only query helpers
│       ├── api/          # endpoints, viewsets, routers
│       └── tests/
├── core/                 # shared auth middleware (JWT verification via
│                           Identity's JWKS endpoint), response formatting
├── Dockerfile
├── requirements.txt
└── .env.example
```

The plan is for enrollment to verify JWTs locally with Identity's public key
through JWKS, so it does not need a network call for every request.
