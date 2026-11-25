import { useEffect, useState } from 'react'
import { defaultTheme } from './default'
import type { ThemeHelper } from './types'

export type { ThemeHelper }
export { defaultTheme }

/**
 * Llibrería de temas reutilitzables.
 *
 * - registerTheme('nom', tema) afegeix un tema al registre.
 * - getTheme() retorna el tema actiu (persistit a localStorage).
 * - useAppTheme() és la versió reactiva per als components.
 * - th és un alias del tema per defecte, per compatibilitat.
 */

const KEY = 'vcc-ui-theme'
const CHANGE_EVENT = 'vcc-ui-theme-change'

const registry = new Map<string, ThemeHelper>()

export function registerTheme(name: string, theme: ThemeHelper): void {
  registry.set(name, theme)
}

registerTheme('default', defaultTheme)

export function listThemes(): string[] {
  return [...registry.keys()]
}

function storedName(): string | null {
  if (typeof localStorage === 'undefined') return null
  return localStorage.getItem(KEY)
}

export function getTheme(name?: string): ThemeHelper {
  const key = name ?? storedName() ?? 'default'
  return registry.get(key) ?? defaultTheme
}

export function setAppTheme(name: string): void {
  localStorage.setItem(KEY, name)
  window.dispatchEvent(new Event(CHANGE_EVENT))
}

export function useAppTheme(): ThemeHelper {
  const [name, setName] = useState<string | undefined>(() => storedName() ?? undefined)
  useEffect(() => {
    const onChange = () => setName(storedName() ?? undefined)
    window.addEventListener(CHANGE_EVENT, onChange)
    window.addEventListener('storage', onChange)
    return () => {
      window.removeEventListener(CHANGE_EVENT, onChange)
      window.removeEventListener('storage', onChange)
    }
  }, [])
  return getTheme(name)
}

/** Alias del tema per defecte (els components existents fan servir `th`). */
export const th: ThemeHelper = defaultTheme
