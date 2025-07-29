"use client";

import { Button } from "@/components/ui/button";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import VerbsLettersSearch from "@/components/verbs/verbs-letters-search";
import VerbsListTopVerbs from "@/components/verbs/verbs-list-top-verbs";
import VerbsListWithLetters from "@/components/verbs/verbs-list-with-letters";
import VerbsSearch from "@/components/verbs/verbs-search";
import { useState } from "react";

export default function SearchPage() {
  const [tab, setTab] = useState<"top_verbs" | "verbs">("verbs");

  // FOR TOP VERBS WE SHOULD ADD A CLICK-METER TO TRACK CLICKS ON TOP VERBS
  // AND USE IT TO SORT THEM IN THE FUTURE
  // FOR NOW WE JUST SHOW THEM IN A SEPARATE TAB

  return (
    <div className="flex flex-1 flex-col overflow-hidden">
      <div className="flex flex-col bg-black">
        <VerbsSearch
          className="flex-none p-4"
          onClick={() => setTab("top_verbs")}
        />
        <div className="flex w-full gap-2 px-4 pb-4">
          <Button
            onClick={() => setTab("top_verbs")}
            className={tab === "top_verbs" ? "bg-gray-400" : ""}
          >
            Top Verbs
          </Button>
          <Button
            onClick={() => setTab("verbs")}
            className={tab === "verbs" ? "bg-gray-400" : ""}
          >
            Verbs
          </Button>
        </div>
      </div>

      {tab === "top_verbs" ? (
        <div className="flex flex-1 overflow-hidden">
          <ScrollArea className="flex-1 overflow-y-auto bg-white w-full h-full p-4">
            <VerbsListTopVerbs />

            <ScrollBar />
          </ScrollArea>
        </div>
      ) : (
        <div className="flex flex-1 overflow-hidden">
          <ScrollArea className="flex-1 overflow-y-auto bg-white w-full h-full p-4">
            <VerbsListWithLetters />

            <VerbsLettersSearch />

            <ScrollBar />
          </ScrollArea>
        </div>
      )}
    </div>
  );
}
