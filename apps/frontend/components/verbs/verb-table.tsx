"use client";

import React, { Fragment, JSX } from "react";
import { ScrollArea } from "@radix-ui/react-scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import {
  Database__ConjugationForm,
  Database__MoodBlock,
  Database__TenseBlock,
  Database__VerbOutput,
} from "@/lib/types/verbs";
import { ScrollBar } from "../ui/scroll-area";
import { zip } from "@/lib/utils/zip";
import { cn } from "@/lib/utils";
import "@/lib/utils/capitalize";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../ui/table";
import { useSettings } from "@/lib/hooks/use-settings";

const marginStyle = { marginBlock: "0.25lh" };

const COLORS: { [key: string]: { [key: string]: string } } = {
  indicatiu: {
    present: "bg-red-600 dark:bg-red-700",
    perfet: "bg-violet-600 dark:bg-violet-700",
    imperfet: "bg-blue-600 dark:bg-blue-700",
    plusquamperfet: "bg-sky-600 dark:bg-sky-700",
    passat_simple: "bg-orange-600 dark:bg-orange-700",
    passat_perifràstic: "bg-orange-600 dark:bg-orange-700",
    passat_anterior: "bg-orange-600 dark:bg-orange-700",
    passat_anterior_perifràstic: "bg-orange-600 dark:bg-orange-700",
    futur: "bg-purple-600 dark:bg-purple-700",
    futur_perfet: "bg-purple-600 dark:bg-purple-700",
    condicional: "bg-cyan-600 dark:bg-cyan-700",
    condicional_perfet: "bg-cyan-600 dark:bg-cyan-700",
  },
  subjuntiu: {
    present: "bg-red-700/90 dark:bg-red-900",
    perfet: "bg-violet-700/90 dark:bg-violet-900",
    imperfet: "bg-blue-700/90 dark:bg-blue-900",
    plusquamperfet: "bg-sky-700/90 dark:bg-sky-900",
  },
  imperatiu: {
    present: "bg-green-600 dark:bg-green-700",
  },
  formes_no_personals: {
    infinitiu: "bg-slate-500/80 dark:bg-slate-700",
    infinitiu_compost: "bg-slate-500/80 dark:bg-slate-700",
    gerundi: "bg-slate-500/80 dark:bg-slate-700",
    gerundi_compost: "bg-slate-500/80 dark:bg-slate-700",
    participi: "bg-slate-500/80 dark:bg-slate-700",
  },
} as const;

function renderTranslation(translation?: string): JSX.Element | null {
  if (!translation) return null;
  const items = translation.split(",").map((item) => item.trim());

  return (
    <div
      className="flex gap-0.5 text-xs text-gray-100 w-36"
      style={marginStyle}
    >
      {items.map((item, index) => (
        <span key={index}>
          {item}
          {index < items.length - 1 ? ", " : ""}
        </span>
      ))}
    </div>
  );
}

function ConjugationCard({
  conjugation,
}: {
  conjugation: Database__ConjugationForm;
}) {
  const { settings } = useSettings();

  const {
    pronoun,
    forms,
    variation_types: variationTypes,
    translation,
  } = conjugation;

  const central: string[] = [];
  const valencian: string[] = [];
  const balearic: string[] = [];
  const ortPre2017: string[] = [];

  if (variationTypes) {
    variationTypes.forEach((type, index) => {
      switch (type?.replace(/\(/g, "")?.replace(/\)/g, "")) {
        case "cent.":
          central.push(forms[index]);
          break;
        case "val.":
          valencian.push(forms[index]);
          break;
        case "bal.":
          balearic.push(forms[index]);
          break;
        case "ort. pre-2017":
          ortPre2017.push(forms[index]);
          break;
        case "val., bal.":
          valencian.push(forms[index]);
          balearic.push(forms[index]);
          break;
        default:
          central.push(forms[index]);
          break;
      }
    });
  } else {
    central.push(...forms);
  }

  return (
    <>
      {/* PRONOUN */}
      <TableCell>
        <div className="flex flex-col gap-0.5">
          {pronoun.replaceAll("_", " ")}
          {renderTranslation(translation)}
        </div>
      </TableCell>
      {/* CENTRAL */}
      <TableCell>
        <ul className="flex flex-col gap-0.5">
          {central.map((form, index) => (
            <li key={index}>{form}</li>
          ))}
        </ul>
      </TableCell>
      {/* VALENCIAN */}
      {settings.show_valencian && (
        <TableCell>
          <ul className="flex flex-col gap-0.5">
            {valencian.map((form, index) => (
              <li key={index}>{form}</li>
            ))}
          </ul>
        </TableCell>
      )}
      {/* BALEARIC */}
      {settings.show_balearic && (
        <TableCell>
          <ul className="flex flex-col gap-0.5">
            {balearic.map((form, index) => (
              <li key={index}>{form}</li>
            ))}
          </ul>
        </TableCell>
      )}
      {/* ORT. PRE-2017 */}
      {settings.show_opt_pre2017 && (
        <TableCell>
          <ul className="flex flex-col gap-0.5">
            {ortPre2017.map((form, index) => (
              <li key={index}>{form}</li>
            ))}
          </ul>
        </TableCell>
      )}
    </>
  );
}

function TenseCard({
  mood,
  tenseBlock,
}: {
  mood: string;
  tenseBlock: Database__TenseBlock;
}) {
  const { settings } = useSettings();

  return (
    <Card
      aria-label={`tense-card:${tenseBlock?.tense}`}
      className={cn(
        "flex-shrink-0 py-2! gap-2! w-xl",
        COLORS[mood.toLowerCase().replaceAll(" ", "_")]?.[tenseBlock?.tense]
      )}
    >
      <CardHeader className="px-4!">
        <CardTitle className="text-white font-bold [&>div>span]:text-sm lg:[&>div>span]:text-md">
          <div className="flex flex-col items-start gap-2">
            <span className="font-bold text-white">
              {`${mood !== "Formes no personals" ? mood : ""}`.toUpperCase()}
            </span>
            <span className="font-bold text-white">
              {tenseBlock?.tense?.replaceAll("_", " ").toUpperCase()}
            </span>
          </div>
        </CardTitle>
      </CardHeader>

      <CardContent className="px-2!">
        <Table>
          <TableHeader>
            <TableRow className="[&>th]:text-white [&>th]:font-bold [&>th]:text-xs lg:[&>th]:text-sm">
              <TableHead className="w-32"></TableHead>
              <TableHead>Cent.</TableHead>
              {settings.show_valencian && <TableHead>Val.</TableHead>}
              {settings.show_balearic && <TableHead>Bal.</TableHead>}
              {settings.show_opt_pre2017 && (
                <TableHead>Ort. Pre-2017</TableHead>
              )}
            </TableRow>
          </TableHeader>
          <TableBody>
            {tenseBlock?.conjugation.map((conjugation, index) => (
              <TableRow className="[&>td]:text-white" key={index}>
                <ConjugationCard conjugation={conjugation} />
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}

export default function VerbTable({ data }: { data: Database__VerbOutput }) {
  const firstFourhTenses = zip(
    data?.moods?.[0]?.tenses?.slice(0, 4) as Database__TenseBlock[],
    data?.moods?.[1]?.tenses as Database__TenseBlock[]
  ) as [Database__TenseBlock, Database__TenseBlock][];

  const theRestOfTenses = data?.moods?.[0]?.tenses?.slice(
    4
  ) as Database__TenseBlock[];

  const imperativeAndFormsNoPersonals = data?.moods?.slice(
    2
  ) as Database__MoodBlock[];

  return (
    <ScrollArea
      className={cn(
        "flex-1 rounded-3xl h-full overflow-y-auto overflow-x-hidden place-self-center",
        "w-90 sm:w-96 md:w-[800px] lg:w-[1000px] xl:w-full dark:bg-zinc-800 p-4 text-white"
      )}
    >
      <div className="flex flex-col gap-4">
        {firstFourhTenses?.map(([indicatiu, subjuntiu], i) => (
          <ScrollArea key={i} className="w-full overflow-x-auto">
            <section
              className="flex gap-4 w-max"
              aria-label={`mood-block:${i}`}
            >
              <TenseCard mood="indicatiu" tenseBlock={indicatiu} />
              {subjuntiu?.tense && (
                <TenseCard mood="subjuntiu" tenseBlock={subjuntiu} />
              )}
            </section>
          </ScrollArea>
        ))}
        {theRestOfTenses?.map((tenseBlock, i) => (
          <ScrollArea
            key={`${tenseBlock.tense}-${i}`}
            className="w-full overflow-x-auto"
          >
            <TenseCard mood="indicatiu" tenseBlock={tenseBlock} />
          </ScrollArea>
        ))}
        {imperativeAndFormsNoPersonals?.map((moodBlock, i) => (
          <Fragment key={i}>
            {moodBlock.tenses.map((tenseBlock) => (
              <ScrollArea
                key={`${moodBlock.mood}-${tenseBlock.tense}`}
                className="w-full overflow-x-auto"
              >
                <TenseCard mood={moodBlock.mood} tenseBlock={tenseBlock} />
              </ScrollArea>
            ))}
          </Fragment>
        ))}
      </div>
      <ScrollBar orientation="vertical" />
    </ScrollArea>
  );
}
