import { AppError } from "@/lib/app-error";
import { API_V1_ENDPOINT, BACKEND_URL } from "@/lib/constants";
import { VerbOut } from "@/lib/types/verbs";
import { withErrorHandler } from "@/lib/with-error-handler";

const getVerb = async ({ _id }: { _id: string }) => {
  const response = await fetch(
    `${BACKEND_URL}${API_V1_ENDPOINT}/verbs/${_id}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  if (!response.ok) {
    throw new AppError("BAD_REQUEST", "Failed to fetch verbs");
  }

  return response.json() as Promise<VerbOut>;
};

export default withErrorHandler(getVerb);
