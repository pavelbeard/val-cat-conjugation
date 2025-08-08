"use client";

import { Database__VerbOutput } from "@/lib/types/verbs";
import { Separator } from "../ui/separator";
import Link from "next/link";
import useVerbClick from "@/lib/hooks/use-verb-click";
import { _normalizeForm } from "@/actions/verbs";

export default function VerbsRowTopVerbs({
  verb,
}: {
  verb: Database__VerbOutput;
}) {
  const { handleVerbClick } = useVerbClick(verb.infinitive);

  return (
    <div className="p-4 mx-2">
      <Link
        href={`/verbs/${_normalizeForm(verb.infinitive)}`}
        className="bg-white dark:bg-black"
        onClick={handleVerbClick}
      >
        <div
          aria-label="form of verb and pronoun"
          className="flex items-center"
        >
          <h1 className="text-lg font-semibold text-black dark:text-white">
            {verb.infinitive}
          </h1>
        </div>
        <div aria-details="translation" className="text-gray-400">
          {verb.translation}
        </div>
        <Separator className="bg-gray-400" />
      </Link>
    </div>
  );
}
