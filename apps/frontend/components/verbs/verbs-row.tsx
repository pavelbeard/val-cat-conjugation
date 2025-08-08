"use client";

import { Database__VerbOutput } from "@/lib/types/verbs";
import { Separator } from "../ui/separator";
import Link from "next/link";
import { _normalizeForm } from "@/actions/verbs";

export default function VerbsRow({ verb }: { verb: Database__VerbOutput }) {
  return (
    <Link
      href={`/verbs/${_normalizeForm(verb.infinitive)}`}
      className="p-4 bg-white dark:bg-black"
    >
      <h1 className="text-lg font-semibold text-black dark:text-white">
        {verb.infinitive}
      </h1>
      <p className="text-gray-400 dark:text-gray-300">{verb.translation}</p>
      <Separator className="bg-gray-400 dark:bg-gray-600" />
    </Link>
  );
}
