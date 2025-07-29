import {
  Database__VerbOutput,
  Database__VerbOutput__ByForm,
  Database__VerbOutput__ByLetter,
} from "@/lib/types/verbs";
import { ApiClient } from "@/lib/utils/api-client";
import { createUrl } from "@/lib/utils/create-url";
import { withErrorHandler } from "@/lib/utils/with-error-handler";

const _traslateVerb = async (verb: string): Promise<Database__VerbOutput> => {
  const response = await ApiClient.post<Database__VerbOutput>(
    createUrl("verbs"),
    {
      infinitive: verb,
    }
  );

  return response;
};

export const translateVerb = withErrorHandler(_traslateVerb);

const _getVerb = async ({ infinitive }: { infinitive: string }) => {
  const response = await ApiClient.get<Database__VerbOutput>(
    createUrl("verbs", infinitive)
  );
  return response;
};

export const getVerb = withErrorHandler(_getVerb);

const _getVerbsByForm = async (form: string) => {
  const response = await ApiClient.get<Database__VerbOutput__ByForm[]>(
    createUrl("verbs_by-form", form)
  );
  return response;
};

export const getVerbsByForm = withErrorHandler(_getVerbsByForm);

const _getVerbsWithFirstLetter = async () => {
  const response = await ApiClient.get<Database__VerbOutput__ByLetter[]>(
    createUrl("verbs_first-letter")
  );
  return response;
};

export const getVerbsWithFirstLetter = withErrorHandler(
  _getVerbsWithFirstLetter
);

const _getVerbs = async () => {
  const response = await ApiClient.get<Database__VerbOutput[]>(
    createUrl("verbs")
  );
  return response;
};

export const getVerbs = withErrorHandler(_getVerbs);
