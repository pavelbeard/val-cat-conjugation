import { Router } from "express";
import { mw } from '@vcc/api-builder';
import { adminController } from "./admin.controller.js";
import { adminValidator } from "./admin.validator.js";

/**
 * Rutas del dominio admin (montadas en /api/admin desde src/router.ts).
 * La escritura (POST/PUT/DELETE) pasa por mw.auth (Bearer ADMIN_TOKEN).
 */
const router = Router();

router.get("/verbs", mw.controller(adminController.list));
router.post(
  "/verbs",
  mw.auth,
  mw.validator(adminValidator.create),
  mw.controller(adminController.create, { status: 201 })
);
router.put(
  "/verbs/:infinitive",
  mw.auth,
  mw.validator(adminValidator.update),
  mw.controller(adminController.update)
);
router.delete(
  "/verbs/:infinitive",
  mw.auth,
  mw.validator(adminValidator.remove),
  mw.controller(adminController.remove)
);

export default router;
