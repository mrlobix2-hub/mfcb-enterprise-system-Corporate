import { prisma } from '../config/prisma.js';
import { env } from '../config/env.js';
import { compareSecret, hashSecret, signAccessToken, signRefreshToken } from '../utils/auth.js';
import { createAuditLog } from '../utils/audit.js';

export async function login(username: string, password: string, ipAddress?: string) {
  const user = await prisma.user.findUnique({ where: { username } });
  if (!user) {
    throw new Error('Invalid credentials');
  }

  if (user.lockedUntil && user.lockedUntil > new Date()) {
    throw new Error('Account temporarily locked');
  }

  const validPassword = await compareSecret(password, user.passwordHash);
  if (!validPassword) {
    const failedAttempts = user.failedLoginAttempts + 1;
    const lockUser = failedAttempts >= env.MAX_LOGIN_ATTEMPTS;

    await prisma.user.update({
      where: { id: user.id },
      data: {
        failedLoginAttempts: lockUser ? 0 : failedAttempts,
        lockedUntil: lockUser ? new Date(Date.now() + env.ACCOUNT_LOCK_MINUTES * 60 * 1000) : null,
      },
    });

    await createAuditLog({ userId: user.id, ipAddress, action: 'AUTH_LOGIN_FAILED' });
    throw new Error(lockUser ? 'Account locked for repeated failed attempts' : 'Invalid credentials');
  }

  await prisma.user.update({
    where: { id: user.id },
    data: {
      failedLoginAttempts: 0,
      lockedUntil: null,
      lastActivityAt: new Date(),
    },
  });

  await createAuditLog({ userId: user.id, ipAddress, action: 'AUTH_LOGIN_SUCCESS' });

  return {
    user: {
      id: user.id,
      username: user.username,
      role: user.role,
      mustChangePassword: user.mustChangePassword,
      recoveryEmail: user.recoveryEmail,
      securityQuestion: user.securityQuestion,
    },
    accessToken: signAccessToken({ userId: user.id, role: user.role }),
    refreshToken: signRefreshToken({ userId: user.id, role: user.role }),
  };
}

export async function completeFirstLoginSetup(userId: string, payload: {
  newPassword: string;
  recoveryEmail: string;
  securityQuestion: string;
  securityAnswer: string;
}) {
  const passwordHash = await hashSecret(payload.newPassword);
  const securityAnswerHash = await hashSecret(payload.securityAnswer);

  return prisma.user.update({
    where: { id: userId },
    data: {
      passwordHash,
      recoveryEmail: payload.recoveryEmail,
      securityQuestion: payload.securityQuestion,
      securityAnswerHash,
      mustChangePassword: false,
      lastActivityAt: new Date(),
    },
  });
}
