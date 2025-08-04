import Footer from "@/components/footer";
import Header from "@/components/header";
import React from "react";

export default function MainLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <section className="h-screen flex flex-col">
      <Header className="flex-none bg-white dark:bg-black px-4 py-2 shadow z-10" />
      <div className="flex-1 overflow-hidden flex flex-col">{children}</div>
      <Footer className="flex-none bg-white dark:bg-black px-4 py-2 shadow z-10" />
    </section>
  );
}
