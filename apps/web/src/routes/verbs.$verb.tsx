import { createFileRoute } from '@tanstack/react-router'
import { VerbDetail } from '@/components/verb-detail'
import { getVerb } from '@/api/client'

export const Route = createFileRoute('/verbs/$verb')({
  loader: ({ params }) => getVerb(params.verb),
  component: () => <VerbDetail verb={Route.useLoaderData()} />,
  errorComponent: ({ error }) => (
    <div className="p-4">
      <h1 className="font-bold">Verb no trobat</h1>
      <p className="text-sm text-gray-500">{String(error)}</p>
    </div>
  ),
})
