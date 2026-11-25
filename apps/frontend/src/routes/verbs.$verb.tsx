import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { VerbDetail } from '@/components/verb-detail'
import { getVerb } from '@/api/client'
import { L } from '@/lib/literals'

export const Route = createFileRoute('/verbs/$verb')({
  component: VerbPage,
})

function VerbPage() {
  const { verb } = Route.useParams()
  const { data, isLoading, error } = useQuery({
    queryKey: ['verb', verb],
    queryFn: () => getVerb(verb),
  })

  if (isLoading) {
    return (
      <div className="p-4 text-sm text-muted-foreground">{L.verbDetail.loading}</div>
    )
  }
  if (error || !data) {
    return (
      <div className="p-4">
        <h1 className="font-bold">{L.verbDetail.notFound}</h1>
        <p className="text-sm text-muted-foreground">{String(error)}</p>
      </div>
    )
  }
  return <VerbDetail verb={data} />
}
