# ADR 0001: Monorepo over multi-repo

## Status
Accepted

## Context
This is a one-person project. The goal is to show clean service boundaries and
reasonable architecture, not to recreate a large organization with many
repos.

## Decision
Keep everything in one repo. The services still live under separate folders
and will each have their own Dockerfile, database, and runtime independence.

## Reasoning
- The key lesson is service isolation, not repo layout. Separate folders and
  separate deploy units are enough for this project.
- A single repo makes the project easier to maintain and review when working
  solo.
- A monorepo allows one place for shared documentation, diagrams, and local
  compose wiring.
- This is a valid production pattern too; monorepos are common in large
  engineering orgs.

## Trade-offs
- I’m not modeling full cross-repo versioning or separate repo CI triggers.
  That’s okay for this project phase.
- It’s less like a true multi-team setup, but it keeps the focus on service
  design and behavior.

## Alternatives considered
- **Multi-repo**: good for real teams, but too much overhead here. It would
  add complexity around repo coordination, documentation, and onboarding for
  no meaningful benefit in this work.
