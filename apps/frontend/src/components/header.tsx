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
import { Row } from '@vcc/web-builder'
import { useAppTheme } from '@vcc/web-builder'
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
  const th = useAppTheme()

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
    <header className={th.header}>
      <Row justify="between" className={className}>
        <Row gap={2}>
          {isDetail && (
            <Link to="/verbs" search={{ page: 1 }} aria-label="Tornar a la llista" className={th.iconButton}>
              <ArrowLeftIcon className="size-5" />
            </Link>
          )}
          <h1 className={th.pageTitle}>{title.toLocaleUpperCase()}</h1>
        </Row>
        <div className="relative" ref={menuRef}>
          <button
            type="button"
            aria-label={open ? 'Tancar menú' : 'Obrir menú'}
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
            className={th.iconButton}
          >
            {open ? <XIcon className="size-5" /> : <MenuIcon className="size-5" />}
          </button>
          {open && (
            <div className={`absolute right-0 top-full mt-2 w-60 ${th.panel}`}>
              <nav className="flex flex-col">
                {LINKS.map((l) => (
                  <Link
                    key={l.to}
                    to={l.to}
                    activeOptions={{ exact: true }}
                    className={th.menuLink(pathname === l.to)}
                    activeProps={{ className: 'font-bold bg-gray-100 dark:bg-gray-900' }}
                  >
                    {l.title}
                  </Link>
                ))}
              </nav>
              <div className={th.divider} />
              <p className={th.menuLabel}>Tema</p>
              <Row gap={1} className="px-1">
                {THEMES.map(({ value, icon: Icon, label }) => (
                  <button
                    key={value}
                    type="button"
                    onClick={() => setTheme(value)}
                    aria-pressed={theme === value}
                    className={th.themeOption(theme === value)}
                  >
                    <Icon className="size-4" />
                    {label}
                  </button>
                ))}
              </Row>
              <div className={th.divider} />
              <p className={`${th.menuLabel} px-3`}>Font normativa: AVL</p>
            </div>
          )}
        </div>
      </Row>
    </header>
  )
}
