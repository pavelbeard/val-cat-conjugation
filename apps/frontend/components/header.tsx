"use client";

import { usePathname } from "next/navigation";

export default function Header() {
  const pathname = usePathname();

  const verbName = new RegExp("/verbs/([^/]+)");
  const pageName = new RegExp("/(\\w+)(?:/|$)");
  const verbMatch = pathname.match(verbName);
  const pageMatch = pathname.match(pageName);

  if (verbMatch) return null;

  return (
    <header className="flex-none flex items-center justify-center p-4 gap-4">
      <h1 className="text-lg font-semibold">
        {pageMatch && pageMatch[1].toLocaleUpperCase()}
      </h1>
    </header>
  );
}
