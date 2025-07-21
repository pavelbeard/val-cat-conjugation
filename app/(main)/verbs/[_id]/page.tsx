"use client";

import getVerb from "@/actions/get-verb";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollBar } from "@/components/ui/scroll-area";
import VerbCard from "@/components/verbs/verb-card";
import {
  Database__ConjugationForm,
  Database__VerbOutput,
  Modes,
} from "@/lib/types/verbs";
import { ScrollArea } from "@radix-ui/react-scroll-area";
import { useQuery } from "@tanstack/react-query";
import { ChevronLeft, PlusIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import { use } from "react";

type Params = Promise<{ _id: string }>;

const temp: Database__ConjugationForm[] = [
  {
    pronoun: "jo",
    forms: ["parlo", "parle", "parl"],
    variation_types: ["cent.", "val.", "bal."],
    translation: "hablo",
  },
  {
    pronoun: "tu",
    forms: ["parles"],
    variation_types: null,
    translation: "hablas",
  },
  {
    pronoun: "ell/(-a)/vostè",
    forms: ["parla"],
    variation_types: null,
    translation: "habla",
  },
  {
    pronoun: "nosaltres",
    forms: ["parlem", "parlam"],
    variation_types: ["cent.", "bal."],
    translation: "hablamos",
  },
  {
    pronoun: "vosaltres",
    forms: ["parleu"],
    variation_types: null,
    translation: "habláis",
  },
  {
    pronoun: "ells/(-es)/vostès",
    forms: ["parlen"],
    variation_types: null,
    translation: "hablan",
  },
];

const Mode = ({
  pronoun,
  forms,
  variation_types,
  translation,
}: Database__ConjugationForm) => {
  return (
    <li className="flex items-start gap-2">
      <div className="flex-none flex flex-col w-32">
        {typeof variation_types === "string" ? (
          <span className="font-semibold">{variation_types}</span>
        ) : (
          <div className="flex-nowrap flex items-center gap-1">
            <div className="inline-flex flex-col items-start gap-1">
              <div className="flex items-center gap-1">
                {forms &&
                  forms.map((f, i) => (
                    <span key={i} className="font-semibold">
                      {f}
                    </span>
                  ))}
              </div>
              <div className="flex items-center gap-1">
                {variation_types &&
                  variation_types.map((v, i) => (
                    <span className="text-sm" key={i}>
                      {v}
                      {i < variation_types.length - 1 ? ", " : ""}
                    </span>
                  ))}
              </div>
            </div>
          </div>
        )}
        <span className="text-gray-500 text-xs">{translation}</span>
      </div>
      <span className="flex-1 text-xs p-1">{pronoun}</span>
    </li>
  );
};

export default function VerbPage({ params }: { params: Params }) {
  const router = useRouter();
  const { _id } = use(params);
  const { data: verb } = useQuery({
    queryKey: ["verb", _id],
    queryFn: () => getVerb({ _id }) as Promise<Database__VerbOutput>,
    staleTime: 1000 * 60 * 60 * 24, // 1 day
    refetchOnWindowFocus: false,
  });

  if (!verb) return null;

  return (
    <div className="flex flex-col gap-4 p-4">
      {/* Controls */}
      <div className="flex items-center justify-between">
        <Button
          onClick={() => {
            router.back();
          }}
          variant="secondary"
          size="icon"
          className="flex-none size-8 bg-amber-300"
        >
          <ChevronLeft />
        </Button>

        <Button
          variant="secondary"
          size="icon"
          className="flex-none size-8 rounded-lg bg-zinc-500"
        >
          <PlusIcon />
        </Button>
      </div>
      {/* Infinitiu */}
      <div className="flex flex-col items-center gap-2">
        <h1 className="text-xl font-bold">{verb.infinitive}</h1>
        <p className="text-lg text-gray-500">{verb.translation}</p>
      </div>
      {/* Present d'indicatiu/de subjuntiu */}
      <ScrollArea className="w-96 overflow-x-auto">
        <div className="flex w-max space-x-4">
          <Card className="w-84 shrink-0">
            <CardHeader>
              <CardTitle>
                {verb.moods?.at(0)?.mood.toLocaleUpperCase()}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Card className="w-full">
                <CardHeader>
                  <CardTitle>Present</CardTitle>
                </CardHeader>
                <CardContent className="px-1!">
                  <VerbCard verb={verb} />
                </CardContent>
              </Card>
              <ul className="flex flex-col gap-2">
                {/* {temp.map((mode) => (
                  <Mode key={mode.pronoun} {...mode} />
                ))} */}
              </ul>
            </CardContent>
            {/* Add more verb details here */}
          </Card>
          <Card className="w-84 shrink-0">
            <CardHeader>
              <CardTitle>
                {verb.moods?.at(1)?.mood.toLocaleUpperCase()}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>{verb.infinitive}</p>
            </CardContent>
            {/* Add more verb details here */}
          </Card>
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </div>
  );
}
