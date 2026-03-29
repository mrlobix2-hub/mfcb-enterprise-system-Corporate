import { Request, Response } from 'express';
import { z } from 'zod';
import { prisma } from '../config/prisma.js';
import { createAuditLog } from '../utils/audit.js';

const createPersonSchema = z.object({
  fullName: z.string().min(2),
  alias: z.string().optional(),
  fatherName: z.string().optional(),
  cnic: z.string().optional(),
  phoneNumbers: z.array(z.string()).default([]),
  city: z.string().optional(),
  country: z.string().optional(),
  riskLevel: z.enum(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']).default('LOW'),
  riskScore: z.number().min(0).max(100).default(0),
  disputeCategory: z.enum(['FINANCIAL', 'LEGAL', 'PERSONAL', 'REPUTATION']).optional(),
  tags: z.array(z.string()).default([]),
});

export async function listPersons(_req: Request, res: Response) {
  const persons = await prisma.person.findMany({ orderBy: { createdAt: 'desc' }, take: 100 });
  return res.json(persons);
}

export async function createPerson(req: Request, res: Response) {
  const payload = createPersonSchema.parse(req.body);
  const count = await prisma.person.count();
  const recordId = `SIV-PR-${String(count + 1).padStart(6, '0')}`;

  const person = await prisma.person.create({
    data: {
      ...payload,
      recordId,
    },
  });

  await createAuditLog({
    userId: req.auth?.userId,
    ipAddress: req.ip,
    action: 'PERSON_CREATED',
    entityType: 'Person',
    entityId: person.id,
  });

  return res.status(201).json(person);
}
