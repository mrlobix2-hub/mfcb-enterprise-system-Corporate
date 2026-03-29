import { Router } from 'express';
import { handleFirstLoginSetup, handleLogin, handleLogout } from '../controllers/auth.controller.js';
import { authenticate } from '../middleware/authenticate.js';

export const authRouter = Router();

authRouter.post('/login', handleLogin);
authRouter.post('/logout', handleLogout);
authRouter.post('/first-login-setup', authenticate, handleFirstLoginSetup);
