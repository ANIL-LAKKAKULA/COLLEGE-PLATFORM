# Notification Service (FastAPI)

**Status:** Planned — Phase 4

**Owns:** consuming events from RabbitMQ and sending emails or notifications
for things like new enrollments, grade publications, or password changes.

The notification service is intentionally decoupled from the core services.
It will listen for events and act on them, rather than being called directly
for business operations.

I’ll define the event contract and service shape during Phase 4.
