import Link from "next/link";
import {
  NavigationMenu,
  NavigationMenuLink,
  NavigationMenuList,
} from "./ui/navigation-menu";
import { cn } from "@/lib/utils";

const components: { title: string; href: string; description: string }[] = [
  {
    title: "Verbs",
    href: "/verbs",
    description: "Description for component 1",
  },
  {
    title: "Decks",
    href: "/decks",
    description: "Description for component 2",
  },
  {
    title: "Settings",
    href: "/settings",
    description: "Description for component 3",
  },
];

export default function Footer({ className }: { className?: string }) {
  return (
    <footer className={cn("place-self-center w-full", className)}>
      <NavigationMenu className="place-self-center shadow-none!">
        <NavigationMenuList>
          {components.map((component) => (
            <NavigationMenuLink
              asChild
              className="md:text-lg lg:text-xl text-gray-800 hover:text-blue-600 transition-colors"
              key={component.href}
              href={component.href}
            >
              <Link href={component.href}>{component.title}</Link>
            </NavigationMenuLink>
          ))}
        </NavigationMenuList>
      </NavigationMenu>
    </footer>
  );
}
