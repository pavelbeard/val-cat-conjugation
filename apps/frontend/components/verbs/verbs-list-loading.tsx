import React from "react";

export default function VerbsListLoading() {
  return (
    <div className="flex flex-col gap-2">
      {Array.of(1, 2, 3, 4, 5, 6, 7).map((item) => (
        <div
          className="h-20 flex flex-col animate-pulse bg-gray-300 w-full rounded-xl"
          key={item}
        >
          <div className="bg-gray-200 mt-2 mb-1 mx-4 h-8 w-3/4 rounded-lg"></div>
          <div className="bg-gray-200/85 h-4 my-1 mx-4 w-1/2 rounded-lg"></div>
        </div>
      ))}
    </div>
  );
}
