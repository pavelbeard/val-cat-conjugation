import type { AppRequest } from '@vcc/api-builder';
import { HttpError } from '@vcc/api-builder';
import { adminBll } from "./admin.bll.js";

/**
 * Controller del admin: funciones async planas que reciben el request ya tratado
 * ({ params, query, body, headers, auth, axios }) y devuelven el resultado.
 * mw.controller envía la respuesta (create → 201 vía opts, remove → 204 si devuelve undefined).
 */
export async function list(_request: AppRequest) {
  return adminBll.listVerbs();
}

export async function create(request: AppRequest) {
  const { body } = request;
  const result = await adminBll.createVerb(body);
  return result;
}

export async function update(request: AppRequest) {
  const { infinitive } = request.params;
  const { body } = request;
  const result = await adminBll.updateVerb(infinitive, body);
  return result;
}

export async function remove(request: AppRequest) {
  const { params } = request;
  const { infinitive } = params;
  const result = await adminBll.deleteVerb(infinitive);
  if (result instanceof HttpError) return result; // 404 si no existe
  // éxito → undefined → 204 No Content
}

export const adminController = { list, create, update, remove };
