import { useEffect, useRef } from 'react'
import { Link } from '@tanstack/react-router'
import { ChevronLeftIcon, ChevronRightIcon } from '@/components/icons'
import type { Verb } from '@/types'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useVerbSearch } from '@/hooks/use-verb-search'
import { PAGE_SIZES } from '@/hooks/use-page-size'
import { pageItems } from '@/lib/pagination'
import { cn } from '@/lib/utils'

const LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÇ'.split('')

const pageClass = 'flex flex-col flex-1 overflow-hidden'
const searchBar = 'flex-none p-4 mx-3 flex items-center gap-2'
const tabs = 'flex w-full px-7'
const tabClass = (side: 'left' | 'right') =>
  cn('rounded-none border-b border-b-border', side === 'left' ? 'rounded-tl-md' : 'rounded-tr-md')
const listArea = 'flex flex-1 overflow-hidden'
const listCol = 'flex-1 flex flex-col overflow-hidden w-full h-full bg-background'
const listScroll = 'flex-1 overflow-y-auto px-5'
const listDivider = 'divide-y divide-border'
const listItem = 'flex items-baseline gap-3 py-1.5 sm:py-2 hover:bg-muted/50 px-1'
const translation = 'text-sm italic text-muted-foreground'
const notice = 'p-4 text-sm text-muted-foreground'
const pagination =
  'order-first flex-none flex items-center justify-center gap-1 sm:gap-1.5 px-3 py-2 sm:py-2.5 border-b border-border flex-wrap bg-background'
const pageBtn = 'h-7 min-w-7 px-0 text-xs sm:h-8 sm:min-w-8 sm:text-sm tabular-nums'
const pageBtnNav = 'h-7 px-1.5 sm:h-8 sm:px-4'
const ellipsis = 'px-0.5 text-muted-foreground select-none text-xs sm:text-sm'
const perPageLabel = 'flex items-center gap-1 sm:gap-1.5 text-xs sm:text-sm text-muted-foreground ml-1 sm:ml-2'
const perPageSelect =
  'h-7 sm:h-8 rounded-md border border-input bg-background px-1.5 sm:px-2 text-xs sm:text-sm shadow-xs focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50'
const totalCount = 'hidden sm:inline text-xs text-muted-foreground ml-2'
const letters =
  'flex-none self-stretch flex flex-col items-center justify-start gap-0 px-1.5 py-1.5 text-[10px] leading-none sm:text-xs text-muted-foreground'
const letterClass = (active: boolean) => cn('hover:text-primary', active && 'font-bold text-primary')

export function VerbSearch({
  page,
  onPageChange,
}: {
  /** Página actual (1-based, viene de la URL ?page=). */
  page: number
  onPageChange: (page: number) => void
}) {
  const s = useVerbSearch({ page, onPageChange })
  const listRef = useRef<HTMLDivElement>(null)

  // Al cambiar de página, volver arriba de la lista
  useEffect(() => {
    listRef.current?.scrollTo({ top: 0 })
  }, [page])

  return (
    <div className={pageClass}>
      <div className={searchBar}>
        <Input
          aria-label="Cerca de verbs"
          className="w-full max-w-md"
          type="search"
          placeholder={s.byForm ? 'Buscar per forma (ex. "vaig")…' : 'Buscar verbs…'}
          value={s.query}
          onChange={(e) => s.setQuery(e.target.value)}
        />
        <Button
          variant={s.byForm ? 'default' : 'outline'}
          size="sm"
          onClick={() => s.setByForm(!s.byForm)}
        >
          Per forma
        </Button>
      </div>

      <div className={tabs}>
        <Button
          variant={s.tab === 'top' ? 'default' : 'ghost'}
          onClick={() => s.setTab('top')}
          className={tabClass('left')}
        >
          Verbs principals
        </Button>
        <Button
          variant={s.tab === 'all' ? 'default' : 'ghost'}
          onClick={() => s.setTab('all')}
          className={tabClass('right')}
        >
          Verbs
        </Button>
      </div>

      <div className={listArea}>
        {/* Columna: paginació fixa dalt + lista amb scroll (flex-1) */}
        <div className={listCol}>
          <div ref={listRef} className={listScroll}>
            {s.isLoading && s.list.length === 0 && <p className={notice}>Buscant…</p>}
            <ul className={listDivider}>
              {s.list.map((v: Verb) => (
                <li key={v._id}>
                  <Link
                    to="/verbs/$verb"
                    params={{ verb: v.infinitive }}
                    className={listItem}
                  >
                    <strong>{v.infinitive}</strong>
                    <span className={translation}>{v.translation}</span>
                  </Link>
                </li>
              ))}
            </ul>
            {!s.isLoading && s.list.length === 0 && (
              <p className={notice}>
                Cap verb trobat{s.query && <> per «{s.query}»</>}.
              </p>
            )}
          </div>

          {s.total > 0 && (
            <nav aria-label="Paginació" className={pagination}>
              {s.totalPages > 1 && (
                <>
                  <Button
                    variant="outline"
                    size="sm"
                    aria-label="Pàgina anterior"
                    className={pageBtnNav}
                    disabled={s.safePage === 0}
                    onClick={() => onPageChange(s.safePage)}
                  >
                    <ChevronLeftIcon className="size-4 sm:hidden" />
                    <span className="hidden sm:inline">Anterior</span>
                  </Button>
                  {pageItems(s.safePage + 1, s.totalPages, s.isDesktop ? 1 : 0).map((item, i) =>
                    item === '…' ? (
                      <span key={`e${i}`} className={ellipsis}>
                        …
                      </span>
                    ) : (
                      <Button
                        key={item}
                        variant={item === s.safePage + 1 ? 'default' : 'outline'}
                        size="sm"
                        className={pageBtn}
                        aria-current={item === s.safePage + 1 ? 'page' : undefined}
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
                    className={pageBtnNav}
                    disabled={s.safePage >= s.totalPages - 1}
                    onClick={() => onPageChange(s.safePage + 2)}
                  >
                    <ChevronRightIcon className="size-4 sm:hidden" />
                    <span className="hidden sm:inline">Següent</span>
                  </Button>
                </>
              )}
              <label className={perPageLabel}>
                <span className="hidden sm:inline">Per pàgina</span>
                <span className="sm:hidden">Pàg.</span>
                <select
                  aria-label="Resultats per pàgina"
                  className={perPageSelect}
                  value={s.pageSize}
                  onChange={(e) => s.setPageSize(Number(e.target.value))}
                >
                  {PAGE_SIZES.map((n) => (
                    <option key={n} value={n}>
                      {n}
                    </option>
                  ))}
                </select>
              </label>
              <span className={totalCount}>{s.total} verbs</span>
            </nav>
          )}
        </div>

        {s.tab === 'all' && !s.byForm && (
          <nav aria-label="Índex alfabètic" className={letters}>
            {LETTERS.map((l) => (
              <button
                key={l}
                type="button"
                className={letterClass(s.letter === l)}
                onClick={() => s.setLetter(s.letter === l ? '' : l)}
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
