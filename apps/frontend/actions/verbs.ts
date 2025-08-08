import {
  Database__VerbOutput,
  Database__VerbOutput__ByForm,
  Database__VerbOutput__ByLetter,
} from "@/lib/types/verbs";
import { ApiClient } from "@/lib/utils/api-client";
import { createUrl } from "@/lib/utils/create-url";

export function _normalizeForm(form: string): string {
  // Normalize the form to remove accents
  return form.normalize("NFKD").replace(/[\u0300-\u036f]/g, "");
}

const _traslateVerb = async (verb: string): Promise<Database__VerbOutput> => {
  const response = await ApiClient.post<Database__VerbOutput>(
    createUrl("verbs"),
    {
      infinitive: _normalizeForm(verb),
    }
  );

  return response;
};

export const translateVerb = _traslateVerb;

const _getVerb = async ({ infinitive }: { infinitive: string }) => {
  const response = await ApiClient.get<Database__VerbOutput>(
    createUrl("verbs", _normalizeForm(infinitive)) // Normalize the infinitive to remove accents
  );
  return response;
};

export const getVerb = _getVerb;

const _getVerbsByForm = async (form: string) => {
  const response = await ApiClient.get<Database__VerbOutput__ByForm[]>(
    createUrl("verbs", `?form=${_normalizeForm(form)}`) // Normalize the form to remove accents
  );
  return response;
};

export const getVerbsByForm = _getVerbsByForm;

const _getVerbsWithFirstLetter = async () => {
  const response = await ApiClient.get<Database__VerbOutput__ByLetter[]>(
    createUrl("verbs", "?letter=true")
  );
  return response;
};

export const getVerbsWithFirstLetter = _getVerbsWithFirstLetter;

const _getVerbs = async () => {
  const response = await ApiClient.get<Database__VerbOutput[]>(
    createUrl("verbs")
  );
  return response;
};

export const getVerbs = _getVerbs;

export const getTopVerbs = async () => {
  const response = await ApiClient.get<Database__VerbOutput[]>(
    createUrl("verbs", `?top=true`)
  );
  return response;
};

export const updateClicks = async (form: string) => {
  const response = await ApiClient.patch<Database__VerbOutput>(
    createUrl("verbs", _normalizeForm(form)),
    {
      clicks: 1,
    }
  );
  return response;
};
