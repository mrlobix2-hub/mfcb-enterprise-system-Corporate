import { Request, Response } from 'express';
import { z } from 'zod';
import { login, completeFirstLoginSetup } from '../services/auth.service.js';
import { clearAuthCookies, setAuthCookies } from '../utils/cookies.js';

const loginSchema = z.object({
  username: z.string().min(3),
  password: z.string().min(8),
});

const firstLoginSchema = z.object({
  newPassword: z.string().min(12),
  recoveryEmail: z.string().email(),
  securityQuestion: z.string().min(5),
  securityAnswer: z.string().min(2),
});

export async function handleLogin(req: Request, res: Response) {
  const payload = loginSchema.parse(req.body);
  const result = await login(payload.username, payload.password, req.ip);
  setAuthCookies(res, result.accessToken, result.refreshToken);
  return res.json({ message: 'Authenticated', user: result.user });
}

export async function handleLogout(_req: Request, res: Response) {
  clearAuthCookies(res);
  return res.json({ message: 'Logged out' });
}

export async function handleFirstLoginSetup(req: Request, res: Response) {
  if (!req.auth?.userId) {
    return res.status(401).json({ message: 'Authentication required' });
  }

  const payload = firstLoginSchema.parse(req.body);
  await completeFirstLoginSetup(req.auth.userId, payload);
  return res.json({ message: 'First login setup completed' });
}
