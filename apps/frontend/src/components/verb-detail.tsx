import { Fragment } from 'react'
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  type ColumnDef,
} from '@tanstack/react-table'
import type { ConjugationForm, TenseBlock, Verb } from '@/types'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table'
import { Col, Row } from '@/components/layout'
import { cn, zip } from '@/lib/utils'
import { useSettings } from '@/lib/settings'

// Paleta de la demo: un color por tiempo verbal
const COLORS: Record<string, Record<string, string>> = {
  indicatiu: {
    present: 'bg-red-600 dark:bg-red-700',
    perfet: 'bg-violet-600 dark:bg-violet-700',
    imperfet: 'bg-blue-600 dark:bg-blue-700',
    plusquamperfet: 'bg-sky-600 dark:bg-sky-700',
    passat_simple: 'bg-orange-600 dark:bg-orange-700',
    passat_perifràstic: 'bg-orange-600 dark:bg-orange-700',
    passat_anterior: 'bg-orange-600 dark:bg-orange-700',
    passat_anterior_perifràstic: 'bg-orange-600 dark:bg-orange-700',
    futur: 'bg-purple-600 dark:bg-purple-700',
    futur_perfet: 'bg-purple-600 dark:bg-purple-700',
    condicional: 'bg-cyan-600 dark:bg-cyan-700',
    condicional_perfet: 'bg-cyan-600 dark:bg-cyan-700',
  },
  subjuntiu: {
    present: 'bg-red-700/90 dark:bg-red-900',
    perfet: 'bg-violet-700/90 dark:bg-violet-900',
    imperfet: 'bg-blue-700/90 dark:bg-blue-900',
    plusquamperfet: 'bg-sky-700/90 dark:bg-sky-900',
  },
  imperatiu: {
    present: 'bg-green-600 dark:bg-green-700',
  },
  formes_no_personals: {
    infinitiu: 'bg-slate-500/80 dark:bg-slate-700',
    infinitiu_compost: 'bg-slate-500/80 dark:bg-slate-700',
    gerundi: 'bg-slate-500/80 dark:bg-slate-700',
    gerundi_compost: 'bg-slate-500/80 dark:bg-slate-700',
    participi: 'bg-slate-500/80 dark:bg-slate-700',
  },
}

function tenseColor(mood: string, tense: string): string {
  return COLORS[mood]?.[tense] ?? 'bg-gray-500 dark:bg-gray-700'
}

// Decide qué variantes dialectales se muestran según los ajustes
function visibleForm(index: number, variation: string | null | undefined, settings: ReturnType<typeof useSettings>): boolean {
  const v = variation?.replace(/[()]/g, '').trim() ?? ''
  if (!v) return true
  if (v.includes('val') && !v.includes('cent')) return settings.show_valencian
  if (v.includes('bal')) return settings.show_balearic
  if (v.includes('pre-2017')) return settings.show_opt_pre2017
  return true
}

function PronounCell({ conjugation }: { conjugation: ConjugationForm }) {
  return (
    <Col gap={0.5}>
      <span className="font-medium whitespace-normal">{conjugation.pronoun.replaceAll('_', ' ')}</span>
      {conjugation.translation && (
        <span className="text-xs text-muted-foreground">{conjugation.translation}</span>
      )}
    </Col>
  )
}

function FormsCell({ conjugation }: { conjugation: ConjugationForm }) {
  const settings = useSettings()
  return (
    <ul className="flex flex-col gap-0.5">
      {conjugation.forms.map((form, i) =>
        visibleForm(i, conjugation.variation_types?.[i], settings) ? (
          <li key={i}>
            {form}
            {conjugation.variation_types?.[i] && (
              <sup className="text-muted-foreground ml-0.5 text-[0.65rem]">
                {conjugation.variation_types[i]}
              </sup>
            )}
          </li>
        ) : null,
      )}
    </ul>
  )
}

const columns: ColumnDef<ConjugationForm>[] = [
  {
    accessorKey: 'pronoun',
    cell: ({ row }) => <PronounCell conjugation={row.original} />,
  },
  {
    id: 'forms',
    cell: ({ row }) => <FormsCell conjugation={row.original} />,
  },
]

function TenseCard({ mood, tenseBlock }: { mood: string; tenseBlock: TenseBlock }) {
  const table = useReactTable({
    data: tenseBlock.conjugation,
    columns,
    getCoreRowModel: getCoreRowModel(),
  })
  return (
    <Card className="overflow-hidden w-90 sm:w-96 md:w-[420px] shrink-0 gap-0 py-0">
      <CardHeader className={cn('py-2', tenseColor(mood, tenseBlock.tense))}>
        <CardTitle className="text-white text-sm uppercase tracking-wide">
          {tenseBlock.tense}
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <Table>
          <TableBody>
            {table.getRowModel().rows.map((row) => (
              <TableRow key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id} className="align-top">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

export function VerbDetail({ verb }: { verb: Verb }) {
  const moods = verb.moods ?? []
  const indicatiu = moods[0]?.tenses ?? []
  const subjuntiu = moods[1]?.tenses ?? []
  const firstFour = zip(indicatiu.slice(0, 4), subjuntiu)
  const restIndicatiu = indicatiu.slice(4)
  const restMoods = moods.slice(2)

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <Col align="center" gap={1} className="pt-3 pb-2">
        <h1 className="text-sm lg:text-xl font-bold">{verb.infinitive}</h1>
        <p className="text-xs lg:text-lg text-muted-foreground">{verb.translation}</p>
      </Col>

      <div className="flex-1 overflow-y-auto overflow-x-hidden w-full p-4">
        <Col align="center" gap={4}>
          {firstFour.map(([ind, subj], i) => (
            <Row key={i} gap={4} align="start" justify="center" wrap>
              {ind && <TenseCard mood="indicatiu" tenseBlock={ind} />}
              {subj && <TenseCard mood="subjuntiu" tenseBlock={subj} />}
            </Row>
          ))}
          {restIndicatiu.map((t, i) => (
            <TenseCard key={`${t.tense}-${i}`} mood="indicatiu" tenseBlock={t} />
          ))}
          {restMoods.map((moodBlock, i) => (
            <Fragment key={i}>
              {moodBlock.tenses.map((t) => (
                <TenseCard key={`${moodBlock.mood}-${t.tense}`} mood={moodBlock.mood} tenseBlock={t} />
              ))}
            </Fragment>
          ))}
        </Col>
      </div>

      <footer className="p-2 text-xs w-full text-muted-foreground">
        Advertencia: traducciones están creadas por un modelo de IA y pueden no ser precisas.
        <br />
        Materiales de referencia:{' '}
        <a
          className="text-primary font-bold hover:underline"
          target="_blank"
          rel="noreferrer"
          href={`https://www.softcatala.org/conjugador-de-verbs/verb/${verb.infinitive.replace("-se", "").replace("-se'n", '')}`}
        >
          Softcatala
        </a>
        ,{' '}
        <a
          className="text-primary font-bold hover:underline"
          target="_blank"
          rel="noreferrer"
          href={`https://www.diccionari.cat/catala-castella/${verb.infinitive}`}
        >
          Diccionari.cat
        </a>
      </footer>
    </div>
  )
}
