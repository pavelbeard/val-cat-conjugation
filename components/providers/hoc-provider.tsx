"use client";
import {
  QueryClient,
  QueryClientProvider as Query,
} from "@tanstack/react-query";

const queryClient = new QueryClient();

export default function HocProvider({
  children,
}: {
  children: Readonly<React.ReactNode>;
}) {
  return <Query client={queryClient}>{children}</Query>;
}
