import { Router } from 'express';
import { createPerson, listPersons } from '../controllers/person.controller.js';

export const personRouter = Router();

personRouter.get('/', listPersons);
personRouter.post('/', createPerson);
