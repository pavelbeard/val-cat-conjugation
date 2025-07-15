import React from "react";
import { ScrollArea, ScrollBar } from "../ui/scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Database__VerbOutput } from "@/lib/types/verbs";

export default function VerbCard({
  verb,
}: {
  verb: Database__VerbOutput;
  handleClose: () => void;
}) {
  return (
    <div className="flex flex-col gap-4 p-4">
      {/* infinitiu */}
      <Card className="w-64">
        <CardHeader>
          <CardTitle>Infinitiu</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg font-semibold">{verb.infinitive}</p>
          <p>{verb.translation}</p>
        </CardContent>
        {/* Add more infinitive details here */}
      </Card>
      {/* Present d'indicatiu/de subjuntiu */}
      <ScrollArea className="w-96 overflow-x-auto">
        <div className="flex w-max space-x-4">
          <Card className="w-64 shrink-0">
            <CardHeader>
              <CardTitle>Indicatiu</CardTitle>
            </CardHeader>
            <CardContent>
              <p>{verb.infinitive}</p>
            </CardContent>
            {/* Add more verb details here */}
          </Card>
          <Card className="w-64 shrink-0">
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
