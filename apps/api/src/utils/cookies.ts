import { Response } from 'express';

const commonCookieOptions = {
  httpOnly: true,
  sameSite: 'lax' as const,
  secure: process.env.NODE_ENV === 'production',
  path: '/',
};

export function setAuthCookies(res: Response, accessToken: string, refreshToken: string) {
  res.cookie('siv_access', accessToken, { ...commonCookieOptions, maxAge: 15 * 60 * 1000 });
  res.cookie('siv_refresh', refreshToken, { ...commonCookieOptions, maxAge: 7 * 24 * 60 * 60 * 1000 });
}

export function clearAuthCookies(res: Response) {
  res.clearCookie('siv_access', { path: '/' });
  res.clearCookie('siv_refresh', { path: '/' });
}
