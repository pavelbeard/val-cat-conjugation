import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { VerbSearch } from '@/components/verb-search'

export const Route = createFileRoute('/verbs/')({
  // Estado de paginación en la URL: /verbs?page=3
  validateSearch: (search: Record<string, unknown>): { page: number } => {
    const p = Number(search.page)
    return { page: Number.isInteger(p) && p >= 1 ? p : 1 }
  },
  component: VerbsPage,
})

function VerbsPage() {
  const { page } = Route.useSearch()
  const navigate = useNavigate()
  return (
    <VerbSearch
      page={page}
      // page segue a la URL (?page=n) però sense reset de scroll: només canvia la llista
      onPageChange={(p) =>
        void navigate({ to: '/verbs', search: { page: p }, resetScroll: false })
      }
    />
  )
}
