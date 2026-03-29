import { NextFunction, Request, Response } from 'express';
import { env } from '../config/env.js';
import { prisma } from '../config/prisma.js';

export async function activityTimeout(req: Request, res: Response, next: NextFunction) {
  if (!req.auth?.userId) return next();

  const user = await prisma.user.findUnique({ where: { id: req.auth.userId } });
  if (!user) return res.status(401).json({ message: 'User not found' });

  if (user.lastActivityAt) {
    const idleMs = Date.now() - user.lastActivityAt.getTime();
    if (idleMs > env.SESSION_INACTIVITY_MINUTES * 60 * 1000) {
      return res.status(440).json({ message: 'Session expired due to inactivity' });
    }
  }

  await prisma.user.update({
    where: { id: req.auth.userId },
    data: { lastActivityAt: new Date() },
  });

  return next();
}
