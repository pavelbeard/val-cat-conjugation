"use client";

import { Database__VerbOutput__ByForm } from "@/lib/types/verbs";
import { Separator } from "../ui/separator";
import Link from "next/link";

export default function VerbsRowByForm({
  verb,
}: {
  verb: Database__VerbOutput__ByForm;
}) {
  return (
    <Link href={`/verbs/${verb.infinitive}`} className="p-4 bg-white dark:bg-black">
      <div aria-label="form of verb and pronoun" className="flex items-center">
        <h1 className="text-lg font-semibold text-black dark:text-white">{verb.verb}</h1>
        <p className="text-gray-400">&nbsp;({verb.pronoun})</p>
      </div>
      <div aria-details="translation" className="text-gray-400">
        {verb.translation}
      </div>
      <div aria-details="tense, mood, infinitive" className="text-gray-400">
        Temps verbal: {verb.tense?.replaceAll(/_/g, " ")} | Mode verbal: {verb.mood} | Infinitiu:{" "}
        {verb.infinitive}
      </div>
      <Separator className="bg-gray-400" />
    </Link>
  );
}
