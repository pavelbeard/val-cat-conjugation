import type { AppRequest } from '@vcc/api-builder';
import { verbsBll } from "./verbs.bll.js";

export async function search(request: AppRequest) {
  const { query } = request;
  const result = await verbsBll.search(query);
  return result;
}

export async function get(request: AppRequest) {
  const result = await verbsBll.getVerb(request.params.infinitive);
  return result;
}

export const verbsController = { search, get };
