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
      <Header className="flex-none bg-white px-4 py-2 shadow z-10" />
      {children}
      <Footer className="flex-none bg-white px-4 py-2 shadow z-10" />
    </section>
  );
}
