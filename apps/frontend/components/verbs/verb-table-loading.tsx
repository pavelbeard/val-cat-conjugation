import React from "react";
import { Card } from "../ui/card";

export default function VerbTableLoading() {
  return (
    <div className="flex h-full flex-col gap-4 p-4">
      <Card className="w-full h-48 bg-blue-gray animate-pulse">
        <div className="flex h-full flex-col gap-4 items-center justify-center">
          <p className="text-lg text-gray-500">Esparando la traducción...</p>
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-gray-300 mt-4"></div>
          <p className="text-lg text-gray-500">
            Esto puede tardar unos segundos
          </p>
        </div>
      </Card>
      <div className="flex gap-4 items-center relative">
        <Card className="w-[357px] h-[374px] bg-blue-300 animate-pulse"></Card>
        <Card className="w-[598px] h-[374px] bg-blue-300 animate-pulse"></Card>
      </div>
    </div>
  );
}
