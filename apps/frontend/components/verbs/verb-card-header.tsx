"use client";

import { useRouter } from "next/navigation";
import { Button } from "../ui/button";
import { ChevronLeft, PlusIcon } from "lucide-react";

export default function VerbCardHeader() {
  const router = useRouter();

  return (
    <header className="flex items-center justify-between">
      <Button
        onClick={() => {
          router.back();
        }}
        variant="secondary"
        size="icon"
        className="flex-none size-8 bg-violet-300 dark:bg-violet-600 rounded-lg"
      >
        <ChevronLeft className="stroke-black dark:stroke-white" />
      </Button>

      <Button
        variant="secondary"
        size="icon"
        className="flex-none size-8 rounded-lg bg-zinc-300 dark:bg-zinc-600"
      >
        <PlusIcon className="stroke-black dark:stroke-white" />
      </Button>
    </header>
  );
}
