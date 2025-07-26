import Link from "next/link";
import {
  NavigationMenu,
  NavigationMenuLink,
  NavigationMenuList,
} from "./ui/navigation-menu";

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

export default function Footer() {
  return (
    <NavigationMenu className="flex-none place-self-center">
      <NavigationMenuList className="flex items-center gap-4 md:gap-8 lg:gap-12 py-2">
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
  );
}
