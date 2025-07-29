"use client";

import useVerbTranslate from "@/lib/hooks/use-verb-translate";
import { queryOptionsGetVerbByInfinitive } from "@/lib/quieries/verbs";
import { useSuspenseQuery } from "@tanstack/react-query";
import VerbTable from "./verb-table";
import VerbTableLoading from "./verb-table-loading";

export default function VerbCard({ infinitive }: { infinitive: string }) {
  const { data: verb } = useSuspenseQuery(
    queryOptionsGetVerbByInfinitive(infinitive)
  );

  const { isTranslating } = useVerbTranslate({ verb });
  const createdAt = new Date(verb.created_at).toLocaleDateString();

  return (
    <>
      {/* Infinitiu */}
      <div className="flex flex-col items-center gap-2">
        <h1 className="text-xl font-bold">{verb.infinitive}</h1>
        <p className="text-lg text-gray-500">{verb.translation}</p>
      </div>
      {/* Verb Card */}
      <div className="flex-1 lg:mx-auto overflow-hidden">
        {isTranslating ? <VerbTableLoading /> : <VerbTable data={verb} />}
      </div>
      <footer className="flex-none mt-4 text-sm text-gray-500">
        <p>Source: {"Gemini 2.5 flash"}</p>
        <p>Created at: {createdAt}</p>
        <p>
          Advertencia: traducciones están creadas por un modelo de IA y pueden
          no ser precisas.
        </p>
      </footer>
    </>
  );
}
