"use client";

import Link from "next/link";
import {
  NavigationMenu,
  NavigationMenuLink,
  NavigationMenuList,
} from "./ui/navigation-menu";
import { cn } from "@/lib/utils";
import { LaptopIcon, MoonIcon, SunIcon } from "lucide-react";
import { useTheme } from "next-themes";
import RadioThemeItem from "./ui/radio-theme-item";

const components: { title: string; href: string; description: string }[] = [
  {
    title: "Verbs",
    href: "/verbs",
    description: "La taula de verbs",
  },
  {
    title: "Traductor",
    href: "/translator",
    description: "La eina de traducció de verbs",
  },
  {
    title: "Ajustes",
    href: "/settings",
    description: "Els ajustes de l'aplicació",
  },
];

export default function Footer({ className }: { className?: string }) {
  const currentTheme = useTheme();
  const btnStyle = `
    bg-transparent 
    text-gray-400 
    hover:text-black
    dark:hover:text-white
    rounded-full shadow-none!`;
  const btnCurrentStyle = `
    text-black 
    dark:text-white
    outline-gray-300
    dark:outline-gray-800
    outline
    `;

  return (
    <footer
      className={cn(
        "place-self-center w-full grid grid-cols-3 items-center",
        className
      )}
    >
      <NavigationMenu className="place-self-center shadow-none! col-2">
        <NavigationMenuList>
          {components.map((component) => (
            <NavigationMenuLink
              asChild
              className="md:text-lg lg:text-xl text-gray-800 dark:text-white hover:text-blue-600 transition-colors"
              key={component.href}
              href={component.href}
            >
              <Link href={component.href}>{component.title}</Link>
            </NavigationMenuLink>
          ))}
        </NavigationMenuList>
      </NavigationMenu>
      <div className="flex-none flex justify-end text-gray-500">
        <fieldset className="flex items-center gap-1 border border-gray-300 dark:border-gray-800 rounded-full">
          <RadioThemeItem
            id="theme-system"
            value="system"
            className={cn(
              btnStyle,
              currentTheme.theme === "system" && btnCurrentStyle
            )}
            onClick={() => currentTheme.setTheme("system")}
          >
            <LaptopIcon className="size-3 md:size-4" />
          </RadioThemeItem>
          <RadioThemeItem
            id="theme-light"
            value="light"
            className={cn(
              btnStyle,
              currentTheme.theme === "light" && btnCurrentStyle
            )}
            onClick={() => currentTheme.setTheme("light")}
          >
            <SunIcon className="size-3 md:size-4" />
          </RadioThemeItem>
          <RadioThemeItem
            id="theme-dark"
            value="dark"
            className={cn(
              btnStyle,
              currentTheme.theme === "dark" && btnCurrentStyle
            )}
            onClick={() => currentTheme.setTheme("dark")}
          >
            <MoonIcon className="size-3 md:size-4" />
          </RadioThemeItem>
        </fieldset>
      </div>
    </footer>
  );
}
