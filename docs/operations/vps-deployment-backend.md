# Backend VPS Deployment Guide

Recommended backend path:

```text
/opt/services/tejido-rural-org/rural-weaver-api
```

Build and restart:

```bash
cd /opt/services/tejido-rural-org/rural-weaver-api
docker compose up -d --build
```

Migrations:

```bash
docker compose exec api alembic current
docker compose exec api alembic upgrade head
```

Logs:

```bash
docker compose logs api --tail=100 -f
```

Frontend production origins must be allowed in CORS:

```text
https://tejidorural.com
https://www.tejidorural.com
```
