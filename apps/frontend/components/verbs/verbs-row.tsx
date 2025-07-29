"use client";

import { Database__VerbOutput } from "@/lib/types/verbs";
import { Separator } from "../ui/separator";
import Link from "next/link";

export default function VerbsRow({ verb }: { verb: Database__VerbOutput }) {
  return (
    <Link href={`/verbs/${verb.infinitive}`} className="p-4 bg-white">
      <h1 className="text-lg font-semibold text-black">{verb.infinitive}</h1>
      <p className="text-gray-400">{verb.translation}</p>
      <Separator className="bg-gray-400" />
    </Link>
  );
}
