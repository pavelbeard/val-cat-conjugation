import { Suspense } from "react";
import Loading from "./loading";
import { Metadata } from "next";
import VerbCard from "./client";

type Props = {
  params: Promise<{ infinitive: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { infinitive } = await params;

  return {
    title: `Verbs | ${infinitive}`,
    description: `Conjugació del verb ${infinitive} en català`,
  };
}

export default async function VerbPage({ params }: Props) {
  const { infinitive } = await params;

  return (
    <Suspense fallback={<Loading />}>
      <VerbCard infinitive={infinitive} />
    </Suspense>
  );
}
