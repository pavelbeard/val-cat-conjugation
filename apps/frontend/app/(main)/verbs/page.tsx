"use client";

import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import VerbsLettersSearch from "@/components/verbs/verbs-letters-search";
import VerbsList from "@/components/verbs/verbs-list";
import VerbsSearch from "@/components/verbs/verbs-search";

export default function SearchPage() {
  return (
    <div className="flex flex-1 flex-col overflow-hidden">
      <VerbsSearch className="flex-none p-4 bg-black" />

      <div className="flex flex-1 overflow-hidden">
        <ScrollArea className="flex-1 overflow-y-auto bg-white w-full h-full p-4">
          <VerbsList />

          <ScrollBar />
        </ScrollArea>

        <VerbsLettersSearch />
      </div>
    </div>
  );
}
