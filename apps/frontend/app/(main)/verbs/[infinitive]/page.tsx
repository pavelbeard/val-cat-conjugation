"use client";

import VerbCard from "@/components/verbs/verb-card";
import { Suspense, use } from "react";
import Loading from "./loading";

type Params = Promise<{ infinitive: string }>;

export default function VerbPage({ params }: { params: Params }) {
  const { infinitive } = use(params);

  return (
    <Suspense fallback={<Loading />}>
      <VerbCard infinitive={infinitive} />
    </Suspense>
  );
}
