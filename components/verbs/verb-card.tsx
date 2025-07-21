import { Database__VerbOutput } from "@/lib/types/verbs";
import React from "react";

export default function VerbCard({ verb }: { verb: Database__VerbOutput }) {
  return <div>{JSON.stringify(verb)}</div>;
}
