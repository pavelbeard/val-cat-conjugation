import { ScrollArea } from "@radix-ui/react-scroll-area";
import React from "react";
import { Card } from "../ui/card";

const getData = async () => {
  const response = await fetch("http://localhost:3000/api/json");
  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }
  return response.json();
};

export default async function VerbTable() {
  const data = await getData();

  return (
    <ScrollArea className="w-96 overflow-x-auto">
      <Card>
        <pre>{JSON.stringify(data)}</pre>
      </Card>
    </ScrollArea>
  );
}
