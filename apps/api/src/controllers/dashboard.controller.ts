import { Request, Response } from 'express';
import { prisma } from '../config/prisma.js';

export async function getDashboardStats(_req: Request, res: Response) {
  const [
    totalPersons,
    activeCases,
    highRiskPersons,
    recentActivity,
  ] = await Promise.all([
    prisma.person.count({ where: { deletedAt: null } }),
    prisma.legalCase.count({ where: { status: { in: ['OPEN', 'INVESTIGATION', 'COURT'] } } }),
    prisma.person.count({ where: { riskLevel: { in: ['HIGH', 'CRITICAL'] }, deletedAt: null } }),
    prisma.auditLog.findMany({ orderBy: { createdAt: 'desc' }, take: 10 }),
  ]);

  return res.json({
    totalPersons,
    activeDisputes: activeCases,
    activeLegalCases: activeCases,
    highRiskPersons,
    upcomingLegalDates: 0,
    totalFinancialExposure: 0,
    recentActivity,
  });
}
