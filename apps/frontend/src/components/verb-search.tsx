import { useEffect, useRef } from 'react'
import { Link } from '@tanstack/react-router'
import { flexRender, getCoreRowModel, useReactTable, type ColumnDef } from '@tanstack/react-table'
import type { Verb } from '@/types'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table'
import { Pagination } from '@/components/pagination'
import { useVerbSearch } from '@/hooks/use-verb-search'
import { PAGE_SIZES } from '@/hooks/use-page-size'
import { cn } from '@/lib/utils'
import { L } from '@/lib/literals'

const LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÇ'.split('')

const pageClass = 'flex flex-col flex-1 overflow-hidden'
// Escritorio: pestañas y cerca en la misma fila; en móvil la cerca pasa debajo de las pestañas
const tabs = 'flex-none flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-3 w-full px-4 sm:px-7 py-2'
const tabGroup = 'flex shrink-0'
const searchBar = 'flex items-center gap-2 w-full sm:flex-1 sm:justify-start'
const tabClass = (side: 'left' | 'right') =>
  cn('rounded-none border-b border-b-border', side === 'left' ? 'rounded-tl-md' : 'rounded-tr-md')
const listArea = 'flex flex-1 min-h-0 overflow-hidden'
// La columna ocupa siempre todo el alto disponible: la tabla (con scroll) crece en flex-1
// y la paginación queda fija abajo, así la altura total nunca varía según el nº de filas.
const listCol = 'flex-1 min-h-0 flex flex-col overflow-hidden w-full bg-background'
const listScroll = 'flex-1 min-h-0 overflow-y-auto px-5'
const translation = 'text-sm italic text-muted-foreground'
const notice = 'p-4 text-sm text-muted-foreground'
const letters =
  'flex-none self-stretch flex flex-col items-center justify-start gap-0 px-1.5 py-1.5 text-[10px] leading-none sm:text-xs text-muted-foreground'
const letterClass = (active: boolean) => cn('hover:text-primary', active && 'font-bold text-primary')

const columns: ColumnDef<Verb>[] = [
  {
    accessorKey: 'infinitive',
    cell: ({ row }) => (
      <Link
        to="/verbs/$verb"
        params={{ verb: row.original.infinitive }}
        className="font-medium hover:underline"
      >
        {row.original.infinitive}
      </Link>
    ),
  },
  {
    accessorKey: 'translation',
    cell: ({ row }) => <span className={translation}>{row.original.translation}</span>,
  },
]

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
  const table = useReactTable({
    data: s.list,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getRowId: (v) => v._id,
  })

  // Al cambiar de página, volver arriba de la lista
  useEffect(() => {
    listRef.current?.scrollTo({ top: 0 })
  }, [page])

  return (
    <div className={pageClass}>
      <div className={tabs}>
        <div className={tabGroup}>
          <Button
            variant={s.tab === 'top' ? 'default' : 'ghost'}
            onClick={() => s.setTab('top')}
            className={tabClass('left')}
          >
            {L.search.tabTop}
          </Button>
          <Button
            variant={s.tab === 'all' ? 'default' : 'ghost'}
            onClick={() => s.setTab('all')}
            className={tabClass('right')}
          >
            {L.search.tabAll}
          </Button>
        </div>

        {/* La cerca (y "Per forma") solo es visible a la pestanya "Verbs" */}
        {s.tab === 'all' && (
          <div className={searchBar}>
            <Input
              aria-label={L.search.inputLabel}
              className="w-full max-w-md"
              type="search"
              placeholder={
                s.mode === 'form'
                  ? L.search.placeholderByForm
                  : s.mode === 'translation'
                    ? L.search.placeholderByTranslation
                    : L.search.placeholder
              }
              value={s.query}
              onChange={(e) => s.setQuery(e.target.value)}
            />
            <Button
              variant={s.mode === 'form' ? 'default' : 'outline'}
              size="sm"
              aria-pressed={s.mode === 'form'}
              onClick={() => s.setMode(s.mode === 'form' ? 'inf' : 'form')}
            >
              {L.search.byForm}
            </Button>
            <Button
              variant={s.mode === 'translation' ? 'default' : 'outline'}
              size="sm"
              aria-pressed={s.mode === 'translation'}
              onClick={() => s.setMode(s.mode === 'translation' ? 'inf' : 'translation')}
            >
              {L.search.byTranslation}
            </Button>
          </div>
        )}
      </div>

      <div className={listArea}>
        {/* Columna: tabla con alto fijo (flex-1) + paginación fija abajo */}
        <div className={listCol}>
          <div ref={listRef} className={listScroll}>
            {s.isLoading && s.list.length === 0 && <p className={notice}>{L.search.searching}</p>}
            <Table>
              <TableBody>
                {table.getRowModel().rows.map((row) => (
                  <TableRow key={row.id}>
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            {!s.isLoading && s.list.length === 0 && (
              <p className={notice}>
                {s.query ? L.search.notFoundFor(s.query) : L.search.notFound}
              </p>
            )}

            {/* La paginació va al flujo, bajo la última fila; la pestanya "principals" no en té */}
            {s.tab === 'all' && s.total > 0 && (
              <Pagination
                page={s.safePage}
                totalPages={s.totalPages}
                total={s.total}
                isDesktop={s.isDesktop}
                onPageChange={onPageChange}
                pageSize={s.pageSize}
                pageSizes={PAGE_SIZES}
                onPageSizeChange={s.setPageSize}
              />
            )}
          </div>
        </div>

        {s.tab === 'all' && s.mode === 'inf' && (
          <nav aria-label={L.search.letters} className={letters}>
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
