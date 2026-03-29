import bcrypt from 'bcrypt';
import { PrismaClient, UserRole } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  const username = process.env.DEFAULT_ADMIN_USERNAME || 'admin_siv';
  const rawPassword = process.env.DEFAULT_ADMIN_PASSWORD || 'SIV@SecureStart2026#';
  const passwordHash = await bcrypt.hash(rawPassword, 12);

  await prisma.user.upsert({
    where: { username },
    update: {
      passwordHash,
      role: UserRole.ADMIN,
      mustChangePassword: true,
    },
    create: {
      username,
      passwordHash,
      role: UserRole.ADMIN,
      mustChangePassword: true,
    },
  });

  console.log(`Seeded default admin: ${username}`);
}

main()
  .catch((error) => {
    console.error(error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
