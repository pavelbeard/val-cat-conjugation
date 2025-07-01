import { headers } from "next/headers";

export default async function Header() {
  const header = await headers();
  const xCurrPath = header.get("x-curr-path");
  const pathname = xCurrPath !== "/" ? xCurrPath?.replace(/\//, "") : "";

  return <header className="flex-none">Header {pathname}</header>;
}
