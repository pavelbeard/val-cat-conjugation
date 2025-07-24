import Link from "next/link";
import {
  NavigationMenu,
  NavigationMenuItem,
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
    <NavigationMenu className="flex-none">
      <NavigationMenuList>
        {components.map((component) => (
          <NavigationMenuLink
            asChild
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
