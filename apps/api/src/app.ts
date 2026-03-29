import cookieParser from 'cookie-parser';
import cors from 'cors';
import csurf from 'csurf';
import express from 'express';
import helmet from 'helmet';
import morgan from 'morgan';
import rateLimit from 'express-rate-limit';
import { env } from './config/env.js';
import { authRouter } from './routes/auth.routes.js';
import { dashboardRouter } from './routes/dashboard.routes.js';
import { personRouter } from './routes/person.routes.js';
import { adminOnly } from './middleware/admin-only.js';
import { authenticate } from './middleware/authenticate.js';
import { activityTimeout } from './middleware/activity-timeout.js';
import { errorHandler } from './middleware/error-handler.js';

export const app = express();

app.use(helmet());
app.use(cors({ origin: env.APP_BASE_URL, credentials: true }));
app.use(morgan('combined'));
app.use(cookieParser());
app.use(express.json({ limit: '10mb' }));

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'siv-api' });
});

app.get('/api/csrf-token', csurf({ cookie: true }), (req, res) => {
  // @ts-expect-error csurf attaches csrfToken at runtime
  res.json({ csrfToken: req.csrfToken() });
});

app.use('/api/auth', rateLimit({ windowMs: 15 * 60 * 1000, max: 30 }), authRouter);
app.use('/api/dashboard', authenticate, activityTimeout, adminOnly, dashboardRouter);
app.use('/api/persons', authenticate, activityTimeout, adminOnly, personRouter);

app.use(errorHandler);
