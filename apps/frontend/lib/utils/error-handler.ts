import { notFound } from "next/navigation";
import { AppError } from "./app-error";

export const withErrorHandler = (
  handler: (...args: any[]) => Promise<Response>
): ((...args: any[]) => Promise<Response>) => {
  return async (...args: any[]) => {
    try {
      const response = await handler(...args);

      if (!response.ok) {
        switch (response.status) {
          case 400:
            throw new AppError("BAD_REQUEST", response.statusText);
          case 404:
            notFound();
          default:
            throw new AppError("SERVER", response.statusText);
        }
      }

      return response as Response;
    } catch (error) {
      if (error instanceof AppError) {
        throw error;
      } else {
        throw new AppError("SERVER", "An unexpected error occurred");
      }
    }
  };
};
