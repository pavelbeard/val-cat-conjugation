import { Database__TenseBlock } from "@/lib/types/verbs";
import React from "react";

export default function VerbMood({
  mood,
  tenses,
}: {
  mood: string;
  tenses: Database__TenseBlock[];
}) {
  return (
    <div>
      <h3>{mood}</h3>
      <ul>
        {tenses.map((block, index) => (
          <li key={index}>{block.tense}</li>
        ))}
      </ul>
    </div>
  );
}
