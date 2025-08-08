"use client";
import {
  QueryClient,
  QueryClientProvider as Query,
} from "@tanstack/react-query";
import { ThemeProvider } from "next-themes";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

const queryClient = new QueryClient();

export default function HocProvider({
  children,
}: {
  children: Readonly<React.ReactNode>;
}) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <Query client={queryClient}>
        {children}
        <ReactQueryDevtools initialIsOpen={false} />
      </Query>
    </ThemeProvider>
  );
}
