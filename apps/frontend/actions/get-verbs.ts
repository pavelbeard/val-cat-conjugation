import { Database__VerbOutput } from "@/lib/types/verbs";
import { ApiClient } from "@/lib/utils/api-client";
import { createUrl } from "@/lib/utils/create-url";
import { withErrorHandler } from "@/lib/utils/with-error-handler";

const getVerbs = async () => {
  const response = await ApiClient.get<Database__VerbOutput[]>(
    createUrl("verbs")
  );
  return response;
};

export default withErrorHandler(getVerbs);
