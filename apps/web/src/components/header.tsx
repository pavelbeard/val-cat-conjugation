import { useEffect, useRef, useState } from 'react'
import { Link, useRouterState } from '@tanstack/react-router'
import {
  ArrowLeftIcon,
  LaptopIcon,
  MenuIcon,
  MoonIcon,
  SunIcon,
  XIcon,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useTheme, type Theme } from '@/lib/theme'

const PAGENAME_MAP: Record<string, string> = {
  verbs: 'Verbs',
  settings: 'Ajusts',
  translator: 'Traductor',
}

const LINKS: { title: string; to: string }[] = [
  { title: 'Verbs', to: '/verbs' },
  { title: 'Traductor', to: '/translator' },
  { title: 'Ajusts', to: '/settings' },
]

const THEMES: { value: Theme; icon: typeof SunIcon; label: string }[] = [
  { value: 'system', icon: LaptopIcon, label: 'Sistema' },
  { value: 'light', icon: SunIcon, label: 'Clar' },
  { value: 'dark', icon: MoonIcon, label: 'Fosc' },
]

export default function Header({ className }: { className?: string }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname })
  const [open, setOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)
  const { theme, setTheme } = useTheme()

  const isDetail = /\/verbs\/[^/]+/.test(pathname)
  const pageMatch = pathname.match(/\/(\w+)(?:\/|$)/)
  const title = pageMatch ? (PAGENAME_MAP[pageMatch[1]] ?? '') : ''

  // Cerrar el menú al navegar, con Escape o al clicar fuera
  useEffect(() => setOpen(false), [pathname])
  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false)
    const onClick = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener('keydown', onKey)
    document.addEventListener('mousedown', onClick)
    return () => {
      document.removeEventListener('keydown', onKey)
      document.removeEventListener('mousedown', onClick)
    }
  }, [open])

  return (
    <header
      className={cn(
        'relative flex-none bg-white dark:bg-black px-4 py-2 shadow z-10',
        className,
      )}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {isDetail && (
            <Link
              to="/verbs"
              search={{ page: 1 }}
              aria-label="Tornar a la llista"
              className="p-1 -ml-1 text-gray-600 dark:text-gray-300 hover:text-black dark:hover:text-white"
            >
              <ArrowLeftIcon className="size-5" />
            </Link>
          )}
          <h1 className="text-lg font-semibold">{title.toLocaleUpperCase()}</h1>
        </div>
        <div className="relative" ref={menuRef}>
          <button
            type="button"
            aria-label={open ? 'Tancar menú' : 'Obrir menú'}
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
            className="p-1.5 -mr-1 text-gray-700 dark:text-gray-200 hover:text-black dark:hover:text-white"
          >
            {open ? <XIcon className="size-5" /> : <MenuIcon className="size-5" />}
          </button>
          {open && (
            <div className="absolute right-0 top-full mt-2 w-60 rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-black shadow-lg p-2">
              <nav className="flex flex-col">
                {LINKS.map((l) => (
                  <Link
                    key={l.to}
                    to={l.to}
                    activeOptions={{ exact: true }}
                    className="rounded-md px-3 py-2 text-sm text-gray-800 dark:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-900"
                    activeProps={{ className: 'font-bold bg-gray-100 dark:bg-gray-900' }}
                  >
                    {l.title}
                  </Link>
                ))}
              </nav>
              <div className="my-2 border-t border-gray-200 dark:border-gray-800" />
              <p className="px-3 pb-1 text-xs text-gray-400 dark:text-gray-500">Tema</p>
              <div className="flex gap-1 px-1">
                {THEMES.map(({ value, icon: Icon, label }) => (
                  <button
                    key={value}
                    type="button"
                    onClick={() => setTheme(value)}
                    aria-pressed={theme === value}
                    className={cn(
                      'flex-1 flex flex-col items-center gap-0.5 rounded-md px-2 py-1.5 text-xs text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-900',
                      theme === value &&
                        'bg-gray-100 dark:bg-gray-900 text-black dark:text-white font-semibold',
                    )}
                  >
                    <Icon className="size-4" />
                    {label}
                  </button>
                ))}
              </div>
              <div className="my-2 border-t border-gray-200 dark:border-gray-800" />
              <p className="px-3 text-xs text-gray-400 dark:text-gray-500">
                Font normativa: AVL
              </p>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
