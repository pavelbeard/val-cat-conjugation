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
    </header>
  );
}
