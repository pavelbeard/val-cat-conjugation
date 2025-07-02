"use client";

import getVerb from "@/actions/get-verb";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollBar } from "@/components/ui/scroll-area";
import { Conjugation, VerbOut, Modes } from "@/lib/types/verbs";
import { ScrollArea } from "@radix-ui/react-scroll-area";
import { useQuery } from "@tanstack/react-query";
import { ChevronLeft, PlusIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import { use } from "react";

type Params = Promise<{ _id: string }>;


const temp: Conjugation[] = [
  {
    pronoun: "jo",
    variation: [
      { word: "parlo", dialect: "cent." },
      { word: "parle", dialect: "val." },
      { word: "parl", dialect: "bal." },
    ],
    translation: "hablo",
  },
  {
    pronoun: "tu",
    variation: "parles",
    translation: "hablas",
  },
  {
    pronoun: "ell/(-a)/vostè",
    variation: "parla",
    translation: "habla",
  },
  {
    pronoun: "nosaltres",
    variation: [
      { word: "parlem", dialect: "cent." },
      { word: "parlam", dialect: "bal." },
    ],
    translation: "hablamos",
  },
  {
    pronoun: "vosaltres",
    variation: "parleu",
    translation: "habláis",
  },
  {
    pronoun: "ells/(-es)/vostès",
    variation: "parlen",
    translation: "hablan",
  },
];

const Mode = ({ pronoun, variation, translation }: Conjugation) => {
  return (
    <li className="flex items-start gap-2">
      <div className="flex-none flex flex-col w-32">
        {typeof variation === "string" ? (
          <span className="font-semibold">{variation}</span>
        ) : (
          <div className="flex-nowrap flex items-center gap-1">
            {variation.map((v, i) => (
              <div
                className="inline-flex flex-col items-start gap-1"
                key={v.word}
              >
                <span className="font-semibold">
                  {v.word}
                  {i < variation.length - 1 ? ", " : ""}
                </span>
                <span className="text-gray-500 text-xs">
                  {v.dialect ? `(${v.dialect})` : ""}
                </span>
              </div>
            ))}
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
    queryFn: () => getVerb({ _id }) as Promise<VerbOut>,
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
              <CardTitle>Indicatiu</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="flex flex-col gap-2">
                {temp.map((mode) => (
                  <Mode key={mode.pronoun} {...mode} />
                ))}
              </ul>
            </CardContent>
            {/* Add more verb details here */}
          </Card>
          <Card className="w-84 shrink-0">
            <CardHeader>
              <CardTitle>Subjuntiu</CardTitle>
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
