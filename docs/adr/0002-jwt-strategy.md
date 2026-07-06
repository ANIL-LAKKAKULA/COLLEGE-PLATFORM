# ADR 0002: Asymmetric JWT (RS256) for cross-service auth

## Status
Accepted

## Context
The downstream services need to know who is calling them and what permissions
the caller has. I don’t want every request to require a network call back to
the Identity service.

## Decision
The Identity service will sign tokens with RS256. Other services verify those
tokens locally using the public key from the JWKS endpoint
(`/.well-known/jwks.json`). That means token verification is local and stateless.

## Why this makes sense
- Local verification keeps services independent. If Identity is unreachable,
  already-issued tokens still work.
- Only Identity holds the private signing key. The rest of the system only
  sees the public key, so they can verify tokens but can’t mint them.
- It avoids the risk of HS256 where any service with the secret could forge a
  token.

## Alternatives considered
- **Shared secret (HS256)**: easier to implement, but it weakens security if any
  service is compromised.
- **Verification endpoint**: central token validation would allow instant
  revocation, but it also makes every request depend on Identity and adds
  latency.

## Consequences
The downside is that pure JWTs are not instantly revocable. That’s acceptable
for the MVP, and we’ll add a refresh-token blacklist and shorter-lived access
tokens in future.
