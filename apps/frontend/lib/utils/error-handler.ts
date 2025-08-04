import { notFound } from "next/navigation";
import { AppError } from "./app-error";

export const withErrorHandler = <T>(
  handler: (...args: any[]) => Promise<T>
): ((...args: any[]) => Promise<T>) => {
  return async (...args: any[]): Promise<T> => {
    try {
      // Call the handler function and await its result
      const result = await handler(...args);

      // Check if the result is a API Call (Response) object
      if (result instanceof Response) {
        if (!result.ok) {
          switch (result.status) {
            case 400:
              throw new AppError("BAD_REQUEST", result.statusText);
            case 404:
              notFound();
            case 429:
              throw new AppError("TOO_MANY_REQUESTS", result.statusText);
            default:
              throw new AppError("SERVER", result.statusText);
          }
        }

        return result as unknown as T;
      }

      // If the result is not a Response (server action or something else) object, return it as is
      return result as T;
    } catch (error) {
      if (error instanceof AppError) {
        throw error;
      }

      throw new AppError("SERVER", "An unexpected error occurred");
    }
  };
};
