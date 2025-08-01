"use client";

import VerbsRow from "./verbs-row";
import { useQuery } from "@tanstack/react-query";
import { queryOptionsGetVerbsWithFirstLetter } from "@/lib/quieries/verbs";
import VerbsListLoading from "./verbs-list-loading";

export default function VerbsListWithLetters() {
  const { data: allData } = useQuery(queryOptionsGetVerbsWithFirstLetter());

  if (!allData) {
    return <VerbsListLoading />;
  }

  return (
    <div className="flex flex-col gap-2 mx-1">
      {allData.map((item) => (
        <section
          className="flex flex-col gap-2"
          key={item._id}
          id={`section-${item._id}`}
        >
          <h2 className="sticky top-0 z-20 p-4 text-lg font-bold uppercase bg-purple-500 dark:bg-purple-800 text-white">
            {item._id}
          </h2>
          {item.verbs.map((verb) => (
            <VerbsRow key={verb.infinitive} verb={verb} />
          ))}
        </section>
      ))}
    </div>
  );
}
