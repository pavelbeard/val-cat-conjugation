"use client";
import {
  QueryClient,
  QueryClientProvider as Query,
} from "@tanstack/react-query";
import { ThemeProvider } from "next-themes";

const queryClient = new QueryClient();

export default function HocProvider({
  children,
}: {
  children: Readonly<React.ReactNode>;
}) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <Query client={queryClient}>{children}</Query>
    </ThemeProvider>
  );
}
