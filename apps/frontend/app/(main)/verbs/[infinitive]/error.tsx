"use client";

import { AppError } from "@/lib/utils/app-error";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  if (error instanceof AppError) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4">
        <h1 className="text-2xl font-bold text-red-600">{error.name}</h1>
        <p className="text-xl text-black dark:text-white">{error.message}</p>
        <button
          onClick={() => reset()}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          Try Again
        </button>
      </div>
    );
  }

  return <div>{error.message}</div>;
}
