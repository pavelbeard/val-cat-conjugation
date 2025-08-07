"use client";

import { useSuspenseQueries } from "@tanstack/react-query";
import {
  queryOptionsGetTopVerbs,
  queryOptionsGetVerbsByForm,
} from "@/lib/quieries/verbs";
import VerbsRowByForm from "./verbs-row-by-form";
import { useSearchParams } from "next/navigation";
import VerbsRowTopVerbs from "./verbs-row-top-verbs";

export default function VerbsListTopVerbs() {
  const query = useSearchParams().get("form") || "";
  const shouldUseFormQuery = query?.length >= 2;
  const queries = useSuspenseQueries({
    queries: [
      queryOptionsGetTopVerbs(),
      queryOptionsGetVerbsByForm(query),
    ],
  });

  const topVerbsData = queries[0].data;
  const formVerbsData = queries[1].data;

  if (!shouldUseFormQuery && topVerbsData?.length > 0) {
    return topVerbsData?.map((verb, i) => (
      <VerbsRowTopVerbs key={i} verb={verb} />
    ));
  } else if (shouldUseFormQuery && formVerbsData?.length > 0) {
    return formVerbsData?.map((verb, i) => (
      <VerbsRowByForm key={i} verb={verb} />
    ));
  } else {
    return (
      <div className="text-center text-gray-500">
        No han encontrado verbos por su petición.
      </div>
    );
  }
}
