"use client";

import { Button } from "@/components/ui/button";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import VerbsLettersSearch from "@/components/verbs/verbs-letters-search";
import VerbsListTopVerbs from "@/components/verbs/verbs-list-top-verbs";
import VerbsListWithLetters from "@/components/verbs/verbs-list-with-letters";
import VerbsSearch from "@/components/verbs/verbs-search";
import { cn } from "@/lib/utils";
import { Suspense } from "react";
import Loading from "./loading";
import { useVerbSearch } from "@/lib/hooks/use-verb-search";

// This page is the main entry point for the verbs section

export default function VerbsPageClient() {
  const { tab, setTab } = useVerbSearch();

  // FOR TOP VERBS WE SHOULD ADD A CLICK-METER TO TRACK CLICKS ON TOP VERBS
  // AND USE IT TO SORT THEM IN THE FUTURE
  // FOR NOW WE JUST SHOW THEM IN A SEPARATE TAB

  return (
    <>
      <div className="flex flex-col">
        <VerbsSearch
          className="flex-none p-4 mx-3"
          onClick={() => setTab("top_verbs")}
        />
        <div className="flex w-full px-7">
          <Button
            onClick={() => setTab("top_verbs")}
            className={cn(
              "rounded-none! rounded-tl-md! border-b! border-b-gray-400! dark:border-b-gray-600!",
              tab === "top_verbs" && "bg-violet-700 font-bold"
            )}
          >
            Top Verbs
          </Button>
          <Button
            onClick={() => setTab("verbs")}
            className={cn(
              "rounded-none! rounded-tr-md! border-b! border-b-gray-400! dark:border-b-gray-600!",
              tab === "verbs" && "bg-violet-700 font-bold"
            )}
          >
            Verbs
          </Button>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        <ScrollArea className="flex-1 overflow-y-auto bg-white dark:bg-black w-full h-full px-5">
          <Suspense fallback={<Loading />}>
            {tab === "top_verbs" ? (
              <VerbsListTopVerbs />
            ) : (
              <VerbsListWithLetters />
            )}
          </Suspense>
          <ScrollBar />
        </ScrollArea>
        {tab === "verbs" && <VerbsLettersSearch />}
      </div>
    </>
  );
}
