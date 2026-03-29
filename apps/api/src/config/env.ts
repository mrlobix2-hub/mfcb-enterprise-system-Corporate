import dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config({ path: '../../.env' });
dotenv.config();

const schema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().default(4000),
  DATABASE_URL: z.string().min(1),
  JWT_ACCESS_SECRET: z.string().min(10),
  JWT_REFRESH_SECRET: z.string().min(10),
  JWT_ACCESS_EXPIRES_IN: z.string().default('15m'),
  JWT_REFRESH_EXPIRES_IN: z.string().default('7d'),
  SESSION_INACTIVITY_MINUTES: z.coerce.number().default(10),
  ACCOUNT_LOCK_MINUTES: z.coerce.number().default(15),
  MAX_LOGIN_ATTEMPTS: z.coerce.number().default(5),
  APP_BASE_URL: z.string().default('http://localhost:3000'),
});

export const env = schema.parse(process.env);
