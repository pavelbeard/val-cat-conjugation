"use client";

export default function VerbCardLoading() {
  return (
    <div className="flex flex-1 flex-col gap-4 p-4 bg-white animate-pulse">
      <header className="h-24 p-4 bg-gray-200 animate-pulse"></header>
      <div className="flex flex-1 items-center justify-center flex-col gap-2">
        <h1 className="text-lg font-semibold text-gray-400 animate-pulse">
          Loading verb...
        </h1>
      </div>
      <footer className="h-16 p-4 bg-gray-200 animate-pulse"></footer>
    </div>
  );
}
