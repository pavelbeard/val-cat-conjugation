"use client";

import { Card, CardContent, CardFooter, CardHeader } from "../ui/card";

export default function VerbCardLoading() {
  return (
    <Card className="flex flex-1 flex-col gap-4 p-4 bg-white animate-pulse">
      <CardHeader className="h-24 p-4 bg-gray-200 rounded-lg animate-pulse"></CardHeader>
      <CardContent className="flex flex-1 items-center justify-center flex-col gap-2">
        <h1 className="text-lg font-semibold text-gray-400 animate-pulse">
          Descargando verbo...
        </h1>
      </CardContent>
      <CardFooter className="h-16 p-4 bg-gray-200 rounded-lg animate-pulse"></CardFooter>
    </Card>
  );
}
