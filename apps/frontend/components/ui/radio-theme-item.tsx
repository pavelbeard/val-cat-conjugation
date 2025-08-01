import { cn } from "@/lib/utils";
import React from "react";

export default function RadioThemeItem({
  children,
  id,
  value,
  className,
  onClick,
}: {
  children: React.ReactNode;
  id: string;
  value: string;
  className?: string;
  onClick?: () => void;
}) {
  return (
    <span className={cn(className, "h-full p-1 md:p-2")} onClick={onClick}>
      <input type="radio" value={value} className="sr-only" id={id} />
      <label htmlFor={id}>
        {children}
        <span className="sr-only">{value}</span>
      </label>
    </span>
  );
}
