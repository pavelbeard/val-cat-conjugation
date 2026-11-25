import { useSyncExternalStore } from 'react'

export interface Settings {
  show_valencian: boolean
  show_catalan: boolean
  show_balearic: boolean
  show_opt_pre2017: boolean
}

const KEY = 'vcc-settings'

const DEFAULTS: Settings = {
  show_valencian: true,
  show_catalan: false,
  show_balearic: false,
  show_opt_pre2017: false,
}

function load(): Settings {
  if (typeof localStorage === 'undefined') return DEFAULTS
  try {
    return { ...DEFAULTS, ...JSON.parse(localStorage.getItem(KEY) ?? '{}') }
  } catch {
    return DEFAULTS
  }
}

let current: Settings = load()
const listeners = new Set<() => void>()

function subscribe(fn: () => void) {
  listeners.add(fn)
  return () => listeners.delete(fn)
}

export function getSettings(): Settings {
  return current
}

export function updateSettings(patch: Partial<Settings>) {
  current = { ...current, ...patch }
  localStorage.setItem(KEY, JSON.stringify(current))
  listeners.forEach((fn) => fn())
}

export function useSettings(): Settings {
  return useSyncExternalStore(subscribe, getSettings)
}
