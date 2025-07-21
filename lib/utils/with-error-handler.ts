import { AppError } from "./app-error";

export function withErrorHandler(handler: (...args: any[]) => Promise<any>) {
  return async (...args: any[]) => {
    try {
      return await handler(...args);
    } catch (error) {
      if (error instanceof AppError) {
        throw error; // Re-throw AppError to be handled by the caller
      }
      console.error("Unexpected error:", error);
      throw new AppError("SERVER", "Internal Server Error");
    }
  };
}
