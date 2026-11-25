import { useEffect, useRef, useState } from 'react'
import { Link, useRouterState } from '@tanstack/react-router'
import {
  ArrowLeftIcon,
  LaptopIcon,
  MenuIcon,
  MoonIcon,
  SunIcon,
  XIcon,
} from '@/components/icons'
import { Separator } from '@/components/ui/separator'
import { Row } from '@/components/layout'
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

const iconButton = 'p-1.5 -mr-1 rounded-md text-foreground hover:bg-accent hover:text-accent-foreground'
const menuLink = (active: boolean) =>
  cn('rounded-md px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground', active && 'font-bold bg-accent')
const menuLabel = 'px-3 pb-1 text-xs text-muted-foreground'
const themeOption = (active: boolean) =>
  cn(
    'flex-1 flex flex-col items-center gap-0.5 rounded-md px-2 py-1.5 text-xs text-muted-foreground hover:bg-accent hover:text-accent-foreground',
    active && 'bg-accent text-foreground font-semibold',
  )

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
    <header className="relative flex-none px-4 py-2 shadow z-10 bg-background">
      <Row justify="between" className={className}>
        <Row gap={2}>
          {isDetail && (
            <Link to="/verbs" search={{ page: 1 }} aria-label="Tornar a la llista" className={iconButton}>
              <ArrowLeftIcon className="size-5" />
            </Link>
          )}
          <h1 className="text-lg font-semibold">{title.toLocaleUpperCase()}</h1>
        </Row>
        <div className="relative" ref={menuRef}>
          <button
            type="button"
            aria-label={open ? 'Tancar menú' : 'Obrir menú'}
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
            className={iconButton}
          >
            {open ? <XIcon className="size-5" /> : <MenuIcon className="size-5" />}
          </button>
          {open && (
            <div className="absolute right-0 top-full mt-2 w-60 rounded-lg border border-border bg-popover text-popover-foreground shadow-lg p-2">
              <nav className="flex flex-col">
                {LINKS.map((l) => (
                  <Link
                    key={l.to}
                    to={l.to}
                    activeOptions={{ exact: true }}
                    className={menuLink(pathname === l.to)}
                    activeProps={{ className: 'bg-accent' }}
                  >
                    {l.title}
                  </Link>
                ))}
              </nav>
              <Separator className="my-2" />
              <p className={menuLabel}>Tema</p>
              <Row gap={1} className="px-1">
                {THEMES.map(({ value, icon: Icon, label }) => (
                  <button
                    key={value}
                    type="button"
                    onClick={() => setTheme(value)}
                    aria-pressed={theme === value}
                    className={themeOption(theme === value)}
                  >
                    <Icon className="size-4" />
                    {label}
                  </button>
                ))}
              </Row>
              <Separator className="my-2" />
              <p className={`${menuLabel} px-3`}>Font normativa: AVL</p>
            </div>
          )}
        </div>
      </Row>
    </header>
  )
}
