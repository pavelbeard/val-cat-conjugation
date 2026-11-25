import { useEffect, useMemo, useRef, useState } from 'react'
import { useQuery, keepPreviousData } from '@tanstack/react-query'
import { searchVerbs, type SearchVerbsParams } from '@/api/client'
import { useDebouncedValue } from '@/hooks/use-debounced-value'
import { useMediaQuery } from '@/hooks/use-media-query'
import { usePageSize } from '@/hooks/use-page-size'

/** Modo de búsqueda: por infinitivo (normal), por forma conjugada o por traducción. */
export type SearchMode = 'inf' | 'form' | 'translation'

/**
 * Lógica de la búsqueda de verbs: pestañas, query con debounce, modo de búsqueda,
 * letra, tamaño de página y la query paginada al servidor.
 * `page`/`onPageChange` vienen de la URL (?page=n) y son de la ruta.
 */
export function useVerbSearch({
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
  const [mode, setMode] = useState<SearchMode>('inf')
  const { pageSize, setPageSize } = usePageSize()
  const debouncedQuery = useDebouncedValue(query, 250)
  const isDesktop = useMediaQuery('(min-width: 640px)')
  const firstRun = useRef(true)

  // Al cambiar de pestaña, búsqueda, letra, modo o tamaño de página, volvemos a la página 1
  // (se omite la primera ejecución para respetar ?page= de la URL)
  useEffect(() => {
    if (firstRun.current) {
      firstRun.current = false
      return
    }
    onPageChange(1)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab, debouncedQuery, letter, mode, pageSize])

  // Búsqueda paginada en el servidor (nunca se cargan todos los verbs) vía TanStack Query
  const params = useMemo<SearchVerbsParams>(() => {
    const p: SearchVerbsParams = {
      page,
      limit: pageSize,
      sort: tab === 'top' ? 'clicks' : 'infinitive',
    }
    const q = debouncedQuery.trim()
    if (mode === 'form') {
      if (q) p.form = q
    } else if (mode === 'translation') {
      if (q) p.translation = q
    } else {
      if (q) p.q = q
      if (tab === 'all' && letter) p.letter = letter
    }
    return p
  }, [tab, debouncedQuery, letter, mode, page, pageSize])

  const { data: result, isLoading } = useQuery({
    queryKey: ['verbs', 'search', params],
    queryFn: () => searchVerbs(params),
    placeholderData: keepPreviousData,
  })

  const list = result?.data ?? []
  const total = result?.metadata.total ?? 0
  const totalPages = result?.metadata.totalPages ?? 1
  const safePage = Math.min(Math.max(page, 1) - 1, totalPages - 1) // 0-based, acotado

  return {
    tab,
    setTab,
    query,
    setQuery,
    letter,
    setLetter,
    mode,
    setMode,
    pageSize,
    setPageSize,
    isDesktop,
    isLoading,
    list,
    total,
    totalPages,
    safePage,
  }
}
