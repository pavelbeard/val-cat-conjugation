import React from "react";

export default function VerbsListLoading() {
  return (
    <div className="flex flex-col gap-2 mx-2 [&>div:first-child]:rounded-b-2xl! [&>div:not(:first-child)]:rounded-2xl!">
      {Array.of(1, 2, 3, 4, 5, 6, 7).map((item) => (
        <div
          className="h-20 flex flex-col animate-pulse bg-gray-300 dark:bg-gray-600 w-full"
          key={item}
        >
          <div className="bg-gray-200 dark:bg-gray-700 mt-2 mb-1 mx-4 h-8 w-3/4 rounded-lg"></div>
          <div className="bg-gray-200/85 dark:bg-gray-700/85 h-4 my-1 mx-4 w-1/2 rounded-lg"></div>
        </div>
      ))}
    </div>
  );
}
