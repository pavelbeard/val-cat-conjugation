import Footer from "@/components/footer";
import Header from "@/components/header";
import React from "react";

export default function MainLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <section className="flex flex-col h-screen">
      <Header />
      <main className="flex-1 overflow-hidden">{children}</main>
      <Footer />
    </section>
  );
}
