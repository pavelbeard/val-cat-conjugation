"use client";

import { useVerbSearch } from "@/lib/hooks/use-verb-search";
import { Input } from "../ui/input";
import { cn } from "@/lib/utils";

export default function VerbsSearch({
  className,
  onClick,
}: {
  className?: string;
  onClick?: () => void;
}) {
  const { form, setForm } = useVerbSearch();

  return (
    <div
      aria-label="search container"
      className={cn("flex items-center", className)}
    >
      <Input
        aria-label="search input"
        className="w-full max-w-md bg-gray-300 text-black dark:text-white"
        type="text"
        placeholder="Buscar verbs..."
        value={form}
        onChange={(e) => setForm(e.target.value)}
        onClick={onClick}
      />
    </div>
  );
}
