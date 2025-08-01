"use client";

import { Button } from "@/components/ui/button";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import VerbsLettersSearch from "@/components/verbs/verbs-letters-search";
import VerbsListTopVerbs from "@/components/verbs/verbs-list-top-verbs";
import VerbsListWithLetters from "@/components/verbs/verbs-list-with-letters";
import VerbsSearch from "@/components/verbs/verbs-search";
import { cn } from "@/lib/utils";
import { useState } from "react";

export default function SearchPage() {
  const [tab, setTab] = useState<"top_verbs" | "verbs">("verbs");

  // FOR TOP VERBS WE SHOULD ADD A CLICK-METER TO TRACK CLICKS ON TOP VERBS
  // AND USE IT TO SORT THEM IN THE FUTURE
  // FOR NOW WE JUST SHOW THEM IN A SEPARATE TAB

  return (
    <div className="flex flex-1 flex-col overflow-hidden">
      <div className="flex flex-col">
        <VerbsSearch
          className="flex-none p-4"
          onClick={() => setTab("top_verbs")}
        />
        <div className="flex w-full gap-2 px-4 pb-4">
          <Button
            onClick={() => setTab("top_verbs")}
            className={cn(tab === "top_verbs" && "bg-violet-700 font-bold")}
          >
            Top Verbs
          </Button>
          <Button
            onClick={() => setTab("verbs")}
            className={cn(tab === "verbs" && "bg-violet-700 font-bold")}
          >
            Verbs
          </Button>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        <ScrollArea className="flex-1 overflow-y-auto bg-white dark:bg-black w-full h-full p-4">
          {tab === "top_verbs" ? (
            <VerbsListTopVerbs />
          ) : (
            <VerbsListWithLetters />
          )}
          <ScrollBar />
        </ScrollArea>
        {tab === "verbs" && <VerbsLettersSearch />}
      </div>
    </div>
  );
}
