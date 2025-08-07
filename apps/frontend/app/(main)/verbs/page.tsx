import { Metadata } from "next";
import VerbsPageClient from "./client";

// This is the server component for generating metadata and other server-side logic
export const metadata: Metadata = {
  title: "Verbs",
  description: "Busca i conjuga els verbs en català",
};

export default function VerbsPage() {
  return <VerbsPageClient />; // Use the client component for the verbs page
}
