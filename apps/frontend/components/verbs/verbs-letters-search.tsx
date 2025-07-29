"use client";

import { useRouter } from "next/navigation";

const LETTERS = "abcdefghijklmnopqrstuvwxyz".split("");

export default function VerbsLettersSearch() {
  const router = useRouter();
  const proceedToLetter = (letter: string) => {
    router.push(`/verbs#section-${letter}`);
  };

  return (
    <aside className="w-6 m-2 rounded-full bg-gray-100 z-50">
      <ul className="flex flex-col items-center justify-center h-full gap-0.5 ">
        {LETTERS.map((letter) => (
          <li
            key={letter}
            className="text-xs font-semibold"
            onClick={() => proceedToLetter(letter)}
          >
            {letter.toUpperCase()}
          </li>
        ))}
      </ul>
    </aside>
  );
}
