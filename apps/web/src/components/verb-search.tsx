import { useEffect, useRef, useState } from 'react'
import { Link } from '@tanstack/react-router'
import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-react'
import type { Paginated, Verb } from '@/types'
import { searchVerbs, type SearchVerbsParams } from '@/api/client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { cn } from '@/lib/utils'

const LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÇ'.split('')
const PAGE_SIZES = [10, 25, 50] as const
const PAGE_SIZE_KEY = 'vcc-page-size'

function storedPageSize(): number {
  const v = Number(localStorage.getItem(PAGE_SIZE_KEY))
  return (PAGE_SIZES as readonly number[]).includes(v) ? v : 50
}

/** Páginas a mostrar: 1 2 3 … n (con elipsis). delta = páginas alrededor de la actual (0 en móvil). */
function pageItems(current: number, total: number, delta: number): (number | '…')[] {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const wanted = new Set([1, 2, total - 1, total])
  for (let p = current - delta; p <= current + delta; p++) wanted.add(p)
  const pages = [...wanted].filter((p) => p >= 1 && p <= total).sort((a, b) => a - b)
  const out: (number | '…')[] = []
  let prev = 0
  for (const p of pages) {
    if (p - prev > 1) out.push('…')
    out.push(p)
    prev = p
  }
  return out
}

function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(
    () => typeof window !== 'undefined' && window.matchMedia(query).matches,
  )
  useEffect(() => {
    const mq = window.matchMedia(query)
    const fn = () => setMatches(mq.matches)
    fn()
    mq.addEventListener('change', fn)
    return () => mq.removeEventListener('change', fn)
  }, [query])
  return matches
}

export function VerbSearch({
  page,
  onPageChange,
}: {
  /** Página actual (1-based, viene de la URL ?page=). */
  page: number
  onPageChange: (page: number) => void
}) {
  const [tab, setTab] = useState<'top' | 'all'>('all')
  const [query, setQuery] = useState('')
  const [letter, setLetter] = useState('')
  const [byForm, setByForm] = useState(false)
  const [pageSize, setPageSize] = useState(storedPageSize)
  const [result, setResult] = useState<Paginated<Verb> | null>(null)
  const [loading, setLoading] = useState(true)
  const listRef = useRef<HTMLDivElement>(null)
  const firstRun = useRef(true)
  const isDesktop = useMediaQuery('(min-width: 640px)')

  // debounce de la búsqueda (250 ms)
  const [debouncedQuery, setDebouncedQuery] = useState(query)
  useEffect(() => {
    const t = setTimeout(() => setDebouncedQuery(query), 250)
    return () => clearTimeout(t)
  }, [query])

  // Al cambiar de pestaña, búsqueda, letra, modo o tamaño de página, volvemos a la página 1
  // (se omite la primera ejecución para respetar ?page= de la URL)
  useEffect(() => {
    if (firstRun.current) {
      firstRun.current = false
      return
    }
    onPageChange(1)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab, debouncedQuery, letter, byForm, pageSize])

  // Búsqueda paginada en el servidor (nunca se cargan todos los verbs)
  useEffect(() => {
    let cancelled = false
    setLoading(true)
    const params: SearchVerbsParams = {
      page,
      limit: pageSize,
      sort: tab === 'top' ? 'clicks' : 'infinitive',
    }
    if (byForm) {
      const f = debouncedQuery.trim()
      if (f) params.form = f
    } else {
      const q = debouncedQuery.trim()
      if (q) params.q = q
      if (tab === 'all' && letter) params.letter = letter
    }
    searchVerbs(params)
      .then((r) => {
        if (!cancelled) setResult(r)
      })
      .catch(() => {
        if (!cancelled) setResult(null)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [tab, debouncedQuery, letter, byForm, page, pageSize])

  // Al cambiar de página, volver arriba de la lista
  useEffect(() => {
    listRef.current?.scrollTo({ top: 0 })
  }, [page])

  const list = result?.data ?? []
  const total = result?.metadata.total ?? 0
  const totalPages = result?.metadata.totalPages ?? 1
  const safePage = Math.min(Math.max(page, 1) - 1, totalPages - 1) // 0-based, acotado

  return (
    <div ref={listRef} className="flex flex-col flex-1 overflow-y-auto">
      <div className="flex-none p-4 mx-3 flex items-center gap-2">
        <Input
          aria-label="Cerca de verbs"
          className="w-full max-w-md bg-gray-300 text-black dark:text-white"
          type="search"
          placeholder={byForm ? 'Buscar per forma (ex. "vaig")…' : 'Buscar verbs…'}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button
          variant={byForm ? 'default' : 'outline'}
          size="sm"
          onClick={() => setByForm(!byForm)}
        >
          Per forma
        </Button>
      </div>

      <div className="flex w-full px-7">
        <Button
          onClick={() => setTab('top')}
          className={cn(
            'rounded-none! rounded-tl-md! border-b! border-b-gray-400! dark:border-b-gray-600!',
            tab === 'top' && 'bg-violet-700 font-bold',
          )}
        >
          Verbs principals
        </Button>
        <Button
          onClick={() => setTab('all')}
          className={cn(
            'rounded-none! rounded-tr-md! border-b! border-b-gray-400! dark:border-b-gray-600!',
            tab === 'all' && 'bg-violet-700 font-bold',
          )}
        >
          Verbs
        </Button>
      </div>

      <div className="flex">
        {/* Columna: lista (crece con el contingut) + paginació enganxada a sota (sticky) */}
        <div className="flex-1 flex flex-col bg-white dark:bg-black w-full">
          <div className="px-5">
            {loading && list.length === 0 && (
              <p className="p-4 text-sm text-gray-500">Buscant…</p>
            )}
            <ul className="divide-y divide-gray-200 dark:divide-gray-800">
              {list.map((v) => (
                <li key={v._id}>
                  <Link
                    to="/verbs/$verb"
                    params={{ verb: v.infinitive }}
                    className="flex items-baseline gap-3 py-1.5 sm:py-2 hover:bg-muted/50 px-1"
                  >
                    <strong>{v.infinitive}</strong>
                    <span className="text-sm italic text-gray-500">{v.translation}</span>
                  </Link>
                </li>
              ))}
            </ul>
            {!loading && list.length === 0 && (
              <p className="p-4 text-sm text-gray-500">
                Cap verb trobat{query && <> per «{query}»</>}.
              </p>
            )}
          </div>

          {total > 0 && (
            <nav
              aria-label="Paginació"
              className="sticky bottom-0 z-10 flex-none flex items-center justify-center gap-1 sm:gap-1.5 px-3 pt-2 pb-[calc(0.75rem+env(safe-area-inset-bottom))] sm:py-3 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-black flex-wrap"
            >
              {totalPages > 1 && (
                <>
                  <Button
                    variant="outline"
                    size="sm"
                    aria-label="Pàgina anterior"
                    className="h-7 px-1.5 sm:h-8 sm:px-4"
                    disabled={safePage === 0}
                    onClick={() => onPageChange(safePage)}
                  >
                    <ChevronLeftIcon className="size-4 sm:hidden" />
                    <span className="hidden sm:inline">Anterior</span>
                  </Button>
                  {pageItems(safePage + 1, totalPages, isDesktop ? 1 : 0).map((item, i) =>
                    item === '…' ? (
                      <span key={`e${i}`} className="px-0.5 text-gray-400 select-none text-xs sm:text-sm">
                        …
                      </span>
                    ) : (
                      <Button
                        key={item}
                        variant={item === safePage + 1 ? 'default' : 'outline'}
                        size="sm"
                        className="h-7 min-w-7 px-0 text-xs sm:h-8 sm:min-w-8 sm:text-sm tabular-nums"
                        aria-current={item === safePage + 1 ? 'page' : undefined}
                        onClick={() => onPageChange(item)}
                      >
                        {item}
                      </Button>
                    ),
                  )}
                  <Button
                    variant="outline"
                    size="sm"
                    aria-label="Pàgina següent"
                    className="h-7 px-1.5 sm:h-8 sm:px-4"
                    disabled={safePage >= totalPages - 1}
                    onClick={() => onPageChange(safePage + 2)}
                  >
                    <ChevronRightIcon className="size-4 sm:hidden" />
                    <span className="hidden sm:inline">Següent</span>
                  </Button>
                </>
              )}
              <label className="flex items-center gap-1 sm:gap-1.5 text-xs sm:text-sm text-gray-500 ml-1 sm:ml-2">
                <span className="hidden sm:inline">Per pàgina</span>
                <span className="sm:hidden">Pàg.</span>
                <select
                  aria-label="Resultats per pàgina"
                  className="h-7 sm:h-8 rounded-md border bg-background px-1.5 sm:px-2 text-xs sm:text-sm"
                  value={pageSize}
                  onChange={(e) => {
                    const n = Number(e.target.value)
                    localStorage.setItem(PAGE_SIZE_KEY, String(n))
                    setPageSize(n)
                  }}
                >
                  {PAGE_SIZES.map((n) => (
                    <option key={n} value={n}>
                      {n}
                    </option>
                  ))}
                </select>
              </label>
              <span className="hidden sm:inline text-xs text-gray-400 ml-2">{total} verbs</span>
            </nav>
          )}
        </div>

        {tab === 'all' && !byForm && (
          <nav className="flex-none flex flex-col items-center gap-1 px-2 py-4 text-xs text-gray-500">
            {LETTERS.map((l) => (
              <button
                key={l}
                type="button"
                className={cn('hover:text-blue-600', letter === l && 'font-bold text-blue-600')}
                onClick={() => setLetter(letter === l ? '' : l)}
              >
                {l}
              </button>
            ))}
          </nav>
        )}
      </div>
    </div>
  )
}
