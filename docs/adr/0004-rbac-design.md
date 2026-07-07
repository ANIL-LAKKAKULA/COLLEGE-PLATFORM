# ADR 0004: Data-driven RBAC with fixed, migration-seeded roles/permissions

## Status
Accepted

## Context
The platform needs role-based access control across 6 roles (Admin,
StudentAdmin, FacultyAdmin, Faculty, Student, HOD) with a creation hierarchy
(Admin creates StudentAdmin/FacultyAdmin; StudentAdmin creates Student;
FacultyAdmin creates Faculty) and support for a user holding multiple roles
at once (e.g. a Faculty member promoted to HOD).

## Decision
Full data-driven RBAC schema:

```
Role (id, name)                     -- fixed set, seeded via migration
Permission (id, name)               -- fixed set, seeded via migration
UserRole (user_id, role_id, assigned_by, assigned_at, revoked_by, revoked_at)
RolePermission (role_id, permission_id)
```

- `User` has **no** `role` column — all role membership lives in `UserRole`,
  supporting multiple simultaneous roles per user.
- Revoking a role is a soft-delete (`revoked_at` set), not a row deletion —
  preserves a full history of who granted/revoked what, and when.
- A user must always have at least one active (non-revoked) role; the
  service layer rejects a revocation that would bring the count to zero and
  suggests disabling the account (`is_active=False`) instead.
- The creation hierarchy and "who can grant HOD" rule are expressed as **data**
  in `RolePermission` (e.g. `ADMIN` holds `create_student_admin`,
  `create_faculty_admin`, `grant_hod`; `STUDENT_ADMIN` holds `create_student`;
  `FACULTY_ADMIN` holds `create_faculty`) rather than as a hardcoded
  role-name map in application code.
- At login, the service flattens the user's roles → permissions into the JWT
  payload (`roles: [...]`, `permissions: [...]`), so every downstream
  authorization check reads directly off the verified token — zero DB calls,
  preserving the stateless-JWT property from ADR 0002.

## Roles and Permissions are fixed (seeded), not dynamically creatable via API

There is no `POST /roles` or `POST /permissions` endpoint. New roles/
permissions are added via migration when a new capability genuinely needs
them (e.g. introducing a future Library service with a `LIBRARIAN` role).

### Why this doesn't limit future scalability
Adding a new microservice already means writing and deploying code; adding
a small seed migration for its role(s)/permission(s) at that point is
negligible extra cost, fully git-tracked and reviewable like any other
change. A runtime CRUD API for roles/permissions only pays for itself in a
genuinely different scenario — a multi-tenant product where different
customers need custom roles *without any code deploy at all*. That isn't
this project's situation: one college, one fixed org chart.

### Alternatives considered
- **Hardcoded role-name checks in code** (`require_roles(["ADMIN"])`, no
  `Permission`/`RolePermission` tables at all): simpler, and fully sufficient
  if capabilities never needed to be decoupled from role names. Rejected in
  favor of the fuller schema specifically because of the HOD case: a user
  needing to hold two roles simultaneously (Faculty + HOD) is naturally
  modeled by a `UserRole` junction table, and once that table exists,
  extending it to full `Permission`/`RolePermission` was a small additional
  step with a stronger interview story (data-driven RBAC, not just
  role-string comparisons).
- **Fully dynamic Role/Permission CRUD via API**: considered and rejected —
  see reasoning above. Revisit if a genuine multi-tenant/custom-role
  requirement emerges.

## Consequences
- Changing a role's permission set (e.g. adding `view_all_grades` to HOD)
  requires a migration, not an API call. Acceptable given roles are fixed.
- An already-issued JWT won't reflect a permission change until it expires
  and the user logs in again — the same limitation already accepted for
  roles/revocation in ADR 0002, so this is consistent, not a new weakness.
