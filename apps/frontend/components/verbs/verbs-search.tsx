"use client";

import React, { useEffect, useState } from "react";
import { Input } from "../ui/input";
import { useDebounce } from "@/lib/hooks/use-debounce";
import { cn } from "@/lib/utils";

export default function VerbsSearch({ className }: { className?: string }) {
  const [searchTerm, setSearchTerm] = useState("");
  const value = useDebounce(searchTerm, 300);

  useEffect(() => {
    // This effect can be used to trigger a search or filter action
    console.log("Searching for:", value);
  }, [value]);

  return (
    <div
      aria-label="search container"
      className={cn("flex items-center", className)}
    >
      <Input
        className="mx-1 w-full max-w-md bg-amber-300 focus:ring-amber-600/80 text-black!"
        type="text"
        placeholder="Search for verbs..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
    </div>
  );
}
