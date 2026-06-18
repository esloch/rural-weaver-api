# Deployment

Target VPS:

```text
188.245.39.97
```

Deployment path:

```text
/opt/services/rural-weaver-api
```

Initial strategy:

```bash
git clone git@github.com:esloch/rural-weaver-api.git
cd rural-weaver-api
cp .env.example .env
docker compose up -d --build
```

Add Nginx reverse proxy after API health is stable.
