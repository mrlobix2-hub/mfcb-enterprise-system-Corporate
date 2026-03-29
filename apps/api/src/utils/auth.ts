import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { env } from '../config/env.js';

export async function hashSecret(value: string): Promise<string> {
  return bcrypt.hash(value, 12);
}

export async function compareSecret(value: string, hash: string): Promise<boolean> {
  return bcrypt.compare(value, hash);
}

export function signAccessToken(payload: { userId: string; role: string }) {
  return jwt.sign(payload, env.JWT_ACCESS_SECRET, { expiresIn: env.JWT_ACCESS_EXPIRES_IN });
}

export function signRefreshToken(payload: { userId: string; role: string }) {
  return jwt.sign(payload, env.JWT_REFRESH_SECRET, { expiresIn: env.JWT_REFRESH_EXPIRES_IN });
}
