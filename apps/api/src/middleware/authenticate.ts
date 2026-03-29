import { NextFunction, Request, Response } from 'express';
import jwt from 'jsonwebtoken';
import { env } from '../config/env.js';

export function authenticate(req: Request, res: Response, next: NextFunction) {
  const bearer = req.headers.authorization?.startsWith('Bearer ')
    ? req.headers.authorization.replace('Bearer ', '')
    : undefined;
  const token = req.cookies?.siv_access || bearer;

  if (!token) {
    return res.status(401).json({ message: 'Authentication required' });
  }

  try {
    const decoded = jwt.verify(token, env.JWT_ACCESS_SECRET) as { userId: string; role: string };
    req.auth = decoded;
    return next();
  } catch {
    return res.status(401).json({ message: 'Invalid or expired token' });
  }
}
