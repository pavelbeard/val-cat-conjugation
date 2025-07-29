import VerbCardHeader from "@/components/verbs/verb-card-header";
import React from "react";

export default function VerbLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-1 flex-col gap-4 p-4 overflow-hidden">
      <VerbCardHeader />
      {children}
    </div>
  );
}
