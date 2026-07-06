# API Gateway (Nginx)

**Status:** Pending — planned for future

The gateway will be the single entry point for client traffic. It should:

- route requests to the correct backend service
- add correlation IDs for tracing
- handle basic logging and health checks
- eventually do rate limiting if needed

Right now the gateway is just a placeholder. I’ll wire it up once the
services are meaningful and the routing requirements are clear.
