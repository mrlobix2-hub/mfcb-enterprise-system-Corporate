# Sentinel Intelligence Vault (SIV)

Secure Personal Legal Intelligence & Dispute Record Management System.

This repository is a production-oriented monorepo scaffold for the system specification provided by the user. It includes a secure architecture, bilingual UI groundwork, Prisma schema, Express API, Next.js 14 frontend, audit logging hooks, and Railway-ready deployment files.

## Stack

- Frontend: Next.js 14, React, TypeScript, Tailwind CSS
- Backend: Node.js, Express, TypeScript
- Database: PostgreSQL + Prisma
- Authentication: JWT + secure session cookies
- Storage: S3-compatible private object storage
- Deployment: GitHub + Railway

## Repository Layout

```text
apps/
  web/      Next.js application
  api/      Express API
packages/
  database/ Prisma schema + seed
infra/
  railway/  Railway deployment notes
  docker/   Dockerfiles
```

## Security Highlights

- bcrypt password hashing
- JWT access/refresh flow
- httpOnly secure cookies
- CSRF token endpoint + middleware hooks
- Helmet security headers
- Rate-limited login + account lockout after 5 failed attempts for 15 minutes
- Session inactivity timeout default 10 minutes
- Zod validation
- Prisma ORM to prevent SQL injection
- XSS-conscious rendering and request validation
- Audit log model and service hooks
- No public registration
- Admin-only access model
- Forced password change on first login
- Recovery email and security question setup
- Soft delete / recycle bin data model

## Quick Start

### 1) Install dependencies

```bash
npm install
```

### 2) Configure environment

```bash
cp .env.example .env
```

Fill in database, JWT, and storage credentials.

### 3) Generate Prisma client and migrate

```bash
npm run db:generate
npm run db:migrate
npm run db:seed
```

### 4) Run locally

```bash
npm run dev
```

- Web: http://localhost:3000
- API: http://localhost:4000/health

## Default Admin

Seed creates:

- Username: `admin_siv`
- Temporary password: `SIV@SecureStart2026#`

On first login, user must change password and set recovery email + security question.

## Railway Deployment

Use **three Railway services**: PostgreSQL, API, and Web.

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
- Set `NEXT_PUBLIC_API_URL` to deployed API URL + `/api`

Do not set the service root directly to `apps/api` or `apps/web` for this workspace layout.

## GitHub Push

```bash
git init
git add .
git commit -m "Initial SIV enterprise scaffold"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Notes

This scaffold is intentionally modular and secure-by-default. Before live use, you should complete:

- storage encryption / object lock policies
- email alerts integration
- PDF report generation templates
- background jobs for reminders
- test coverage and penetration testing
- production secrets rotation

## Compliance / Language Rules

UI and domain terms avoid accusatory language. Use terms such as:

- Subject individual
- Dispute party
- Concerned individual

The system is strictly for private documentation and legal record organization.
