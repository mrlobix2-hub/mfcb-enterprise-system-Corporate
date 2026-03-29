import { NextFunction, Request, Response } from 'express';

export function adminOnly(req: Request, res: Response, next: NextFunction) {
  if (req.auth?.role !== 'ADMIN') {
    return res.status(403).json({ message: 'Admin access required' });
  }
  return next();
}
