"use client";

import { useSuspenseQuery } from "@tanstack/react-query";
import { queryOptionsGetVerbsByForm } from "@/lib/quieries/verbs";
import VerbsRowByForm from "./verbs-row-by-form";
import { useSearchStore } from "@/lib/store/use-search-store";

export default function VerbsListTopVerbs() {
  const query = useSearchStore((state) => state.query);
  const { data: allData } = useSuspenseQuery(queryOptionsGetVerbsByForm(query));

  if (allData.length === 0) {
    return (
      <div className="text-center text-gray-500">
        No han encontrado verbos por su petición.
      </div>
    );
  }

  return allData?.map((verb, i) => <VerbsRowByForm key={i} verb={verb} />);

  return (
    <div className="flex flex-col gap-2 mx-1">
      {allData?.map((verb, i) => (
        <VerbsRowByForm key={i} verb={verb} />
      ))}
    </div>
  );
}
