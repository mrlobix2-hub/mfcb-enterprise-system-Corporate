# Railway Notes

Recommended deployment is **two app services + one PostgreSQL service**:

- Service 1: PostgreSQL
- Service 2: API
- Service 3: Web

## Recommended service setup

### API service
- Root directory: repository root
- Install command: `npm install`
- Build command: `npm run build:db && npm run build:api`
- Start command: `npm run start:api`
- Healthcheck path: `/health`

### Web service
- Root directory: repository root
- Install command: `npm install`
- Build command: `npm run build:web`
- Start command: `npm run start:web`
- Set `NEXT_PUBLIC_API_URL` to your deployed API URL followed by `/api`

Do **not** point Railway directly at `apps/api` or `apps/web` when using this workspace layout, because the Prisma schema and shared workspace context live at the repository root.
