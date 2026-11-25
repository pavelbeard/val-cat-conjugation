import express from "express";
import adminRouter from "./admin/admin.router.js";
import verbsRouter from "./verbs/verbs.router.js";

/**
 * Router raíz de la API: monta los routers de cada dominio.
 * Cada ruta de dominio sigue el patrón: mw.validator(validator.x) → mw.controller(controller.x)
 * (y mw.auth antes en las de escritura del admin).
 */
const router = express.Router();

router.get("/api/health", (_req, res) => res.json({ status: "ok" }));

router.use("/api/verbs", verbsRouter);
router.use("/api/admin", adminRouter);

export default router;
