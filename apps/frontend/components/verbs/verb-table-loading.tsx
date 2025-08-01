import React from "react";
import { Card } from "../ui/card";

export default function VerbTableLoading() {
  return (
    <Card className="w-full h-full bg-blue-gray animate-pulse px-6 dark:bg-zinc-800 dark:text-white">
      <div className="flex h-full flex-col gap-4 items-center justify-center">
        <p className="text-lg text-gray-500">Esparando la traducción...</p>
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-gray-300 mt-4"></div>
        <p className="text-lg text-gray-500">Esto puede tardar unos segundos</p>
      </div>
    </Card>
  );
}
