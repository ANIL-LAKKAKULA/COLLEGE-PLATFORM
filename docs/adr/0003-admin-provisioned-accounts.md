# ADR 0003: Admin-provisioned accounts, no self-registration

## Status
Accepted (supersedes the original self-registration design)

## Context
The original design assumed public self-registration (`POST /auth/register`),
modeled after consumer apps. On reflection, a college doesn't work that way:
students and faculty already exist in the institution before they ever touch
the portal — accounts should be provisioned, not self-served.

## Decision
No public registration endpoint exists. Instead:

- The single Admin account is created **once, manually**, outside the API
  (a seed/management command) — there is no bootstrapping endpoint for it,
  since no authority exists yet to authorize creating the first admin.
- Every other account is created via `POST /users`, protected by a
  hierarchy-checked permission (see ADR 0004): Admin creates
  StudentAdmin/FacultyAdmin, StudentAdmin creates Student, FacultyAdmin
  creates Faculty.
- New accounts are given a default password derived from date of birth
  (e.g. `Dob@15011999`), which satisfies the password policy so the account
  is immediately usable.
- Email verification is **not implemented** — since every email address is
  entered by an authorized admin/administrator rather than self-reported by
  an untrusted registrant, there's no unverified-input scenario left to
  guard against.

## Reasoning
- Matches how real institutional systems provision accounts (Google
  Workspace for Education, enterprise SSO, university portals) — IT/admin
  provisions; users don't self-serve.
- Removes an entire class of registration-abuse concerns (spam signups,
  fake emails, mass-assignment of `role` from client input) that a public
  endpoint would otherwise need defending against.

## Known limitations (deliberate, not oversights)
- The DOB-based default password is not truly secret — anyone who knows a
  user's date of birth can guess it. This is an accepted trade-off for
  project scope, not a production recommendation. A real system would
  either email a random token+link (which needs working email infra — see
  Phase 3) or require an out-of-band verification step at provisioning time.
- There is no server-side enforcement forcing a password change after first
  login. The `POST /auth/change-password` endpoint is available, but using
  it is left to client/UX policy, not the API. This is a conscious scope
  decision: the API's job is to expose the capability, not dictate its use.
  A production system would likely track "time since last password change"
  as a security metric even without hard enforcement.
