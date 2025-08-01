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

  return (
    <>
      {/* Infinitiu */}
      <div className="flex flex-col items-center gap-2">
        <h1 className="text-sm lg:text-xl font-bold">{verb.infinitive}</h1>
        <p className="text-xs lg:text-lg text-gray-500">{verb.translation}</p>
      </div>
      {/* Verb Card */}
      <div className="flex-1 lg:mx-auto overflow-hidden">
        {isTranslating ? <VerbTableLoading /> : <VerbTable data={verb} />}
      </div>
      <footer className="p-2 text-xs w-full text-gray-500">
        Advertencia: traducciones están creadas por un modelo de IA y pueden no
        ser precisas.
      </footer>
    </>
  );
}
