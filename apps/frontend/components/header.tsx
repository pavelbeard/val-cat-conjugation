"use client";

import { cn } from "@/lib/utils";
import { usePathname } from "next/navigation";

export default function Header({ className }: { className?: string }) {
  const pathname = usePathname();

  const verbName = new RegExp("/verbs/([^/]+)");
  const pageName = new RegExp("/(\\w+)(?:/|$)");
  const verbMatch = pathname.match(verbName);
  const pageMatch = pathname.match(pageName);

  if (verbMatch) return null;

  return (
    <header className={cn(className)}>
      <h1 className="text-lg font-semibold">
        {pageMatch && pageMatch[1].toLocaleUpperCase()}
      </h1>
    </header>
  );
}
