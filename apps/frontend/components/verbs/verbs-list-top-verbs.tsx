"use client";

import { useSuspenseQuery } from "@tanstack/react-query";
import { queryOptionsGetVerbsByForm } from "@/lib/quieries/verbs";
import VerbsRowByForm from "./verbs-row-by-form";
import { useSearchParams } from "next/navigation";

export default function VerbsListTopVerbs() {
  const query = useSearchParams().get("form") || "";
  const { data: allData } = useSuspenseQuery(queryOptionsGetVerbsByForm(query));

  if (allData.length === 0) {
    return (
      <div className="text-center text-gray-500">
        No han encontrado verbos por su petición.
      </div>
    );
  }

  return allData?.map((verb, i) => <VerbsRowByForm key={i} verb={verb} />);
}
