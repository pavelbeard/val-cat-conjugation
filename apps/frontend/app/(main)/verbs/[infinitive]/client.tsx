"use client";

import VerbTable from "@/components/verbs/verb-table";
import VerbTableLoading from "@/components/verbs/verb-table-loading";
import useVerbTranslate from "@/lib/hooks/use-verb-translate";
import { queryOptionsGetVerbByInfinitive } from "@/lib/quieries/verbs";
import { useSuspenseQuery } from "@tanstack/react-query";
import { notFound } from "next/navigation";

export default function VerbCard({ infinitive }: { infinitive: string }) {
  const { data: verb } = useSuspenseQuery(
    queryOptionsGetVerbByInfinitive(infinitive)
  );

  const { isTranslating, isError } = useVerbTranslate({ verb });

  if (isError) {
    notFound();
  }

  return (
    <>
      {/* Infinitiu */}
      <div className="flex flex-col items-center gap-2">
        <h1 className="text-sm lg:text-xl font-bold">{verb.infinitive}</h1>
        <p className="text-xs lg:text-lg text-gray-500">{verb.translation}</p>
      </div>
      {/* Verb Card */}
      {isTranslating ? (
        <VerbTableLoading />
      ) : (
        <div className="flex-1 lg:mx-auto overflow-hidden">
          <VerbTable data={verb} />
        </div>
      )}
      <footer className="p-2 text-xs w-full text-gray-500">
        Advertencia: traducciones están creadas por un modelo de IA y pueden no
        ser precisas.
        <br />
        Materiales de referencia:{" "}
        <a
          className="text-blue-500 font-bold"
          target="_blank"
          href={`https://www.softcatala.org/conjugador-de-verbs/verb/${verb.infinitive.replace("-se", "").replace("-se'n", "")}`}
        >
          Softcatala
        </a>
        ,{" "}
        <a
          className="text-blue-500 font-bold"
          target="_blank"
          href={`https://www.diccionari.cat/catala-castella/${verb.infinitive}`}
        >
          Diccionari.cat
        </a>
      </footer>
    </>
  );
}
