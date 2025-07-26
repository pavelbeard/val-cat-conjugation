import { Database__VerbOutput } from "@/lib/types/verbs";
import { ApiClient } from "@/lib/utils/api-client";
import { createUrl } from "@/lib/utils/create-url";
import { withErrorHandler } from "@/lib/utils/with-error-handler";

const traslateVerb = async (verb: string): Promise<Database__VerbOutput> => {
  const response = await ApiClient.post<Database__VerbOutput>(
    createUrl("verbs"),
    {
      infinitive: verb,
    }
  );

  return response;
};

export default withErrorHandler(traslateVerb);
