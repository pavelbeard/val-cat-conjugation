"use client";

import { useQuery } from "@tanstack/react-query";
import { queryOptionsGetVerbsByForm } from "@/lib/quieries/verbs";
import VerbsListLoading from "./verbs-list-loading";
import VerbsRowByForm from "./verbs-row-by-form";
import { useSearchStore } from "@/lib/store/use-search-store";

export default function VerbsListTopVerbs() {
  const query = useSearchStore((state) => state.query);
  const { data: allData, isLoading } = useQuery(
    queryOptionsGetVerbsByForm(query)
  );

  if (isLoading) {
    return <VerbsListLoading />;
  }

  if (!allData) {
    return <div className="text-center text-gray-500">No verbs found</div>;
  }

  return (
    <div className="flex flex-col gap-2 mx-1">
      {allData?.map((verb, i) => (
        <VerbsRowByForm key={i} verb={verb} />
      ))}
    </div>
  );
}
