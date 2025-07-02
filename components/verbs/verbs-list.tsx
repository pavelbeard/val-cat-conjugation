"use client";

import { VerbOut } from "@/lib/types/verbs";
import { use } from "react";
import VerbsRow from "./verbs-row";

export default function VerbsList({
  verbsPromise,
}: {
  verbsPromise: Promise<VerbOut[]>;
}) {
  const verbs = use(verbsPromise);
  return verbs.map((verb) => <VerbsRow key={verb._id} verb={verb} />);
}
