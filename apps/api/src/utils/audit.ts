import { prisma } from '../config/prisma.js';

export async function createAuditLog(input: {
  userId?: string;
  ipAddress?: string;
  action: string;
  entityType?: string;
  entityId?: string;
  metadata?: unknown;
}) {
  return prisma.auditLog.create({
    data: input,
  });
}
