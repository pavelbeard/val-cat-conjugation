"use client";

import { Database__VerbOutput } from "@/lib/types/verbs";
import { Separator } from "../ui/separator";
import Link from "next/link";

export default function VerbsRow({ verb }: { verb: Database__VerbOutput }) {
  return (
    <Link href={`/verbs/${verb._id}`} className="p-4">
      <h1 className="text-lg font-semibold">{verb.infinitive}</h1>
      <p>{verb.translation}</p>
      <Separator className="bg-blue-500" />
    </Link>
  );
}
