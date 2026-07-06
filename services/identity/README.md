# Identity Service (FastAPI)

**Status:** Not started — Phase 1

**Owns:** user accounts, authentication, JWT issuance, and role claims
(Admin/Faculty/Student).

FastAPI is a good fit here because authentication is relatively lightweight
and performance-sensitive. This service mainly issues tokens and validates
credentials, so it does not need the heavier Django stack.

## Planned structure
```
identity/
├── app/
│   ├── api/            # route handlers
│   ├── core/           # config, security, JWT signing
│   ├── models/         #  models
│   ├── schemas/        # Pydantic request/response schemas
│   ├── services/      # business logic for auth flows
│   └── selectors/     # query helpers
├── tests/
├── keys/             # RSA key pair (gitignored)
├── Dockerfile
├── requirements.txt
└── .env.example
```

This service will use RS256 JWTs and publish the public key via JWKS. See
`docs/adr/0002-jwt-strategy.md` for the rationale.
