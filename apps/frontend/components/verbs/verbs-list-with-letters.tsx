"use client";

import VerbsRow from "./verbs-row";
import { useSuspenseQuery } from "@tanstack/react-query";
import { queryOptionsGetVerbsWithFirstLetter } from "@/lib/quieries/verbs";
import { cn } from "@/lib/utils";
import { Database__VerbOutput__ByLetter } from "@/lib/types/verbs";

function VerbRowWithLetter({ item }: { item: Database__VerbOutput__ByLetter }) {
  return (
    <>
      <h2
        className={cn(
          "sticky top-0 z-20",
          "p-4 mx-2 text-lg font-bold uppercase",
          "bg-violet-500 dark:bg-violet-800 text-white rounded-b-2xl rounded-tr-2xl",
          "shadow-lg shadow-violet-500/50 dark:shadow-violet-800/50"
        )}
      >
        {item._id}
      </h2>
      {item.verbs.map((verb) => (
        <VerbsRow key={verb.infinitive} verb={verb} />
      ))}
    </>
  );
}

export default function VerbsListWithLetters() {
  const { data: allData } = useSuspenseQuery(
    queryOptionsGetVerbsWithFirstLetter()
  );

  return allData.map((item) => (
    <section
      className="flex flex-col gap-2"
      key={item._id}
      id={`section-${item._id}`}
    >
      <VerbRowWithLetter item={item} />
    </section>
  ));
}
