import React from 'react'
import SettingsPageClient from './client'
import { Metadata } from 'next';

// This page is the settings page for the application and for metadata generation
export const metadata: Metadata = {
  title: "Verbs | Ajusts",
  description: "Ajusta la configuració de l'aplicació",
};

export default function SettingsPage() {
  return <SettingsPageClient />
}
