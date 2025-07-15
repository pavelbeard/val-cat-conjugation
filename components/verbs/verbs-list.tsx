"use client";

import { Database__VerbOutput } from "@/lib/types/verbs";
import { use } from "react";
import VerbsRow from "./verbs-row";

export default function VerbsList({
  verbsPromise,
}: {
  verbsPromise: Promise<Database__VerbOutput[]>;
}) {
  const verbs = use(verbsPromise);
  return verbs.map((verb) => <VerbsRow key={verb._id} verb={verb} />);
}
