"use client";

import React, { useEffect, useState } from "react";
import { Input } from "../ui/input";
import { useDebounce } from "@/lib/hooks/use-debounce";
import { cn } from "@/lib/utils";
import { useSearchStore } from "@/lib/store/use-search-store";

export default function VerbsSearch({
  className,
  onClick,
}: {
  className?: string;
  onClick?: () => void;
}) {
  const [searchTerm, setSearchTerm] = useState("");
  const value = useDebounce(searchTerm, 800);
  const setQuery = useSearchStore((state) => state.setQuery);

  useEffect(() => {
    // This effect can be used to trigger a search or filter action
    setQuery(value);
  }, [value]);

  return (
    <div
      aria-label="search container"
      className={cn("flex items-center", className)}
    >
      <Input
        aria-label="search input"
        className="mx-1 w-full max-w-md bg-amber-300 focus:ring-amber-600/80 text-black!"
        type="text"
        placeholder="Search for verbs..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        onClick={onClick}
      />
    </div>
  );
}
