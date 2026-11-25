import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function zip<T, U>(a: T[], b: U[]): [T | undefined, U | undefined][] {
  const len = Math.max(a.length, b.length)
  return Array.from({ length: len }, (_, i) => [a[i], b[i]])
}
