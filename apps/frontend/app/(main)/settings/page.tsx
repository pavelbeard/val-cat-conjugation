import React, { Suspense } from "react";
import SettingsPageClient from "./client";
import { Metadata } from "next";
import Loading from "./loading";

export const dynamic = "force-dynamic"; // Force dynamic rendering for this page

// This page is the settings page for the application and for metadata generation
export const metadata: Metadata = {
  title: "Verbs | Ajusts",
  description: "Ajusta la configuració de l'aplicació",
};

export default function SettingsPage() {
  return (
    <Suspense fallback={<Loading />}>
      <SettingsPageClient />
    </Suspense>
  );
}
