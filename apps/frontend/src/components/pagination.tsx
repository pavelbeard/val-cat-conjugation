import { ChevronLeftIcon, ChevronRightIcon } from '@/components/icons'
import { Button } from '@/components/ui/button'
import { pageItems } from '@/lib/pagination'
import { L } from '@/lib/literals'
import { cn } from '@/lib/utils'

const nav = 'flex items-center justify-end gap-1 px-3 py-1.5 border-t border-border flex-wrap'
const pageBtn = 'min-w-6 h-6 px-0 text-xs tabular-nums'
const ellipsis = 'px-0.5 text-muted-foreground select-none text-xs'
const perPageLabel = 'flex items-center gap-1 text-xs text-muted-foreground ml-2'
const perPageSelect =
  'h-6 rounded-md border border-input bg-background px-1.5 text-xs shadow-xs focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50'
const totalCount = 'hidden sm:inline text-xs text-muted-foreground ml-2'

export function Pagination({
  page,
  totalPages,
  total,
  isDesktop,
  onPageChange,
  pageSize,
  pageSizes,
  onPageSizeChange,
}: {
  /** Página actual 0-based (acotada). */
  page: number
  totalPages: number
  total: number
  isDesktop: boolean
  onPageChange: (page: number) => void
  pageSize: number
  pageSizes: readonly number[]
  onPageSizeChange: (n: number) => void
}) {
  return (
    <nav aria-label={L.pagination.label} className={nav}>
      {totalPages > 1 && (
        <>
          <Button
            variant="outline"
            size="icon-xs"
            aria-label={L.pagination.prev}
            disabled={page === 0}
            onClick={() => onPageChange(page)}
          >
            <ChevronLeftIcon />
          </Button>
          {pageItems(page + 1, totalPages, isDesktop ? 1 : 0).map((item, i) =>
            item === '…' ? (
              <span key={`e${i}`} className={ellipsis}>
                …
              </span>
            ) : (
              <Button
                key={item}
                variant={item === page + 1 ? 'default' : 'outline'}
                size="icon-xs"
                className={cn(pageBtn)}
                aria-current={item === page + 1 ? 'page' : undefined}
                onClick={() => onPageChange(item)}
              >
                {item}
              </Button>
            ),
          )}
          <Button
            variant="outline"
            size="icon-xs"
            aria-label={L.pagination.next}
            disabled={page >= totalPages - 1}
            onClick={() => onPageChange(page + 2)}
          >
            <ChevronRightIcon />
          </Button>
        </>
      )}
      <label className={perPageLabel}>
        <span className="hidden sm:inline">{L.pagination.perPage}</span>
        <span className="sm:hidden">{L.pagination.perPageShort}</span>
        <select
          aria-label={L.pagination.perPageLabel}
          className={perPageSelect}
          value={pageSize}
          onChange={(e) => onPageSizeChange(Number(e.target.value))}
        >
          {pageSizes.map((n) => (
            <option key={n} value={n}>
              {n}
            </option>
          ))}
        </select>
      </label>
      <span className={totalCount}>{L.pagination.total(total)}</span>
    </nav>
  )
}
