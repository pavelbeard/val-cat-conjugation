import Link from "next/link";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from "./ui/navigation-menu";

const components: { title: string; href: string; description: string }[] = [
  {
    title: "Component 1",
    href: "/component-1",
    description: "Description for component 1",
  },
  {
    title: "Component 2",
    href: "/component-2",
    description: "Description for component 2",
  },
  {
    title: "Component 3",
    href: "/component-3",
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
