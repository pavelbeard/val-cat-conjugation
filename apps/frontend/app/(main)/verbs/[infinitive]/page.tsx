"use client";

import VerbCard from "@/components/verbs/verb-card";
import VerbCardLoading from "@/components/verbs/verb-card-loading";
import { Suspense, use } from "react";

type Params = Promise<{ infinitive: string }>;

export default function VerbPage({ params }: { params: Params }) {
  const { infinitive } = use(params);

  return (
    <Suspense fallback={<VerbCardLoading />}>
      <VerbCard infinitive={infinitive} />
    </Suspense>
  );
}
