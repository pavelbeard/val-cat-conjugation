'use client'

import getVerb from '@/actions/get-verb'
import translateVerb from '@/actions/translate-verb'
import { Button } from '@/components/ui/button'
import VerbTable from '@/components/verbs/verb-table'
import { Database__VerbOutput } from '@/lib/types/verbs'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { ChevronLeft, PlusIcon } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { use, useEffect } from 'react'

type Params = Promise<{ _id: string }>

export default function VerbPage({ params }: { params: Params }) {
  const queryClient = useQueryClient()
  const router = useRouter()
  const { _id } = use(params)
  const { data: verb } = useQuery({
    queryKey: ['verb', _id],
    queryFn: () => getVerb({ _id }) as Promise<Database__VerbOutput>,
    staleTime: 1000 * 60 * 60 * 24, // 1 day
    refetchOnWindowFocus: false,
  })

  const mutation = useMutation({
    mutationFn: (verb: string) => translateVerb(verb),
    onSuccess: (data) => {
      queryClient.setQueryData(['verb', data._id], data)
    },
  })

  useEffect(() => {
    if ((!verb?.moods || verb?.moods?.length === 0) && verb?.infinitive) {
      mutation.mutate(verb.infinitive)
    }
  }, [verb])

  if (!verb) return null

  return (
    <div className="flex h-full flex-col gap-4 p-4">
      {/* Controls */}
      <div className="flex items-center justify-between">
        <Button
          onClick={() => {
            router.back()
          }}
          variant="secondary"
          size="icon"
          className="flex-none size-8 bg-amber-300"
        >
          <ChevronLeft />
        </Button>

        <Button
          variant="secondary"
          size="icon"
          className="flex-none size-8 rounded-lg bg-zinc-500"
        >
          <PlusIcon />
        </Button>
      </div>
      {/* Infinitiu */}
      <div className="flex flex-col items-center gap-2">
        <h1 className="text-xl font-bold">{verb.infinitive}</h1>
        <p className="text-lg text-gray-500">{verb.translation}</p>
      </div>
      {/* Verb Card */}
      {mutation.isPending ? (
        <div className="flex h-full flex-col gap-4 items-center justify-center">
          <p className="text-lg text-gray-500">Esparando la traducción...</p>
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-gray-300 mt-4"></div>
          <p className="text-lg text-gray-500">
            Esto puede tardar unos segundos
          </p>
        </div>
      ) : (
        <VerbTable data={verb} />
      )}
      <footer className="flex-none mt-4 text-sm text-gray-500">
        <p>Source: {verb.source || 'Gemini 2.5 flash'}</p>
        <p>Created at: {new Date(verb.created_at).toLocaleDateString()}</p>
        <p>
          Advertencia: traducciones están creadas por un modelo de IA y pueden
          no ser precisas.
        </p>
      </footer>
    </div>
  )
}
