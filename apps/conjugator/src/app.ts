import cors from "cors";
import express from "express";
import router from "./api/router.js";
import { errorHandler, notFoundHandler } from '@vcc/api-builder';

/** App Express montada por separado del listen, para poder testearla con supertest. */
export function createApp() {
  const app = express();
  app.use(cors());
  app.use(express.json({ limit: "5mb" }));

  app.use(router);

  // Cadena global: rutas desconocidas → 404; cualquier error → errorHandler
  app.use(notFoundHandler);
  app.use(errorHandler);

  return app;
}

export const app = createApp();
