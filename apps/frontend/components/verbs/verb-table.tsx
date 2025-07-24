'use client'

import { ScrollArea } from '@radix-ui/react-scroll-area'
import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import {
  Database__ConjugationForm,
  Database__TenseBlock,
  Database__VerbOutput,
} from '@/lib/types/verbs'
import { ScrollBar } from '../ui/scroll-area'
import { zip } from '@/lib/utils/zip'
import { cn } from '@/lib/utils'

import '@/lib/utils/capitalize'

const colors: { [key: string]: { [key: string]: string } } = {
  indicatiu: {
    present: 'bg-blue-400',
    imperfet: 'bg-red-400',
    perfet: 'bg-red-400',
    plusquamperfet: 'bg-red-400',
    passat_simple: 'bg-purple-400',
    passat_perifràstic: 'bg-purple-400',
    passat_anterior: 'bg-purple-400',
    passat_anterior_perifràstic: 'bg-purple-400',
    futur: 'bg-orange-400',
    futur_perfet: 'bg-orange-400',
    condicional: 'bg-yellow-400',
    condicional_perfet: 'bg-yellow-400',
  },
  subjuntiu: {
    present: 'bg-indigo-400',
    imperfet: 'bg-violet-400',
    perfet: 'bg-violet-400',
    plusquamperfet: 'bg-violet-400',
  },
  imperatiu: {
    present: 'bg-green-400',
  },
  formes_no_personals: {
    infinitiu: 'bg-slate-400',
    infinitiu_compost: 'bg-slate-400',
    gerundi: 'bg-slate-400',
    gerundi_compost: 'bg-slate-400',
    participi: 'bg-slate-400',
  },
} as const

function ConjugationCard({
  conjugation,
}: {
  conjugation: Database__ConjugationForm
}) {
  return (
    <li className="flex items-start gap-2">
      <div className={cn('flex flex-col gap-0.5', 'w-32')}>
        <p className="text-xs font-semibold" style={{ marginBlock: '0.25lh' }}>
          {conjugation.pronoun.replaceAll('_', ' ')}:
        </p>
        <div
          className="flex flex-col gap-0.5 text-[10px] text-gray-700"
          style={{ marginBlock: '0.25lh' }}
        >
          {conjugation?.translation &&
            conjugation?.translation?.split(',')?.map((item, index) => (
              <span key={index}>
                {item.trim()}
                {index <
                (conjugation?.translation?.split(',') as string[])?.length - 1
                  ? ', '
                  : ''}
              </span>
            ))}
        </div>
      </div>
      <div className="flex flex-col flex-1 gap-0.5">
        {conjugation?.variation_types
          ? (
              zip(
                conjugation.forms as string[],
                conjugation.variation_types as string[]
              ) as [string, string][]
            ).map(([form, type], i) => (
              <p key={i} className="text-xs" style={{ marginBlock: '0.25lh' }}>
                {`${form}${type ? ` ${type}` : ''}${
                  i < conjugation.forms.length - 1 ? ',' : ''
                }`}
              </p>
            ))
          : conjugation.forms.map((form, i) => (
              <p key={i} className="text-xs" style={{ marginBlock: '0.25lh' }}>
                {form}
              </p>
            ))}
      </div>
    </li>
  )
}

function BigTenseCard({
  mood,
  tenseBlock,
}: {
  mood: string
  tenseBlock: Database__TenseBlock
}) {
  return (
    <Card
      className={cn(
        'flex-shrink-0',
        colors[mood]?.[tenseBlock?.tense],
        mood === 'indicatiu' ? 'w-84' : 'w-[600px] mr-4'
      )}
    >
      <CardHeader>
        <CardTitle>
          {tenseBlock?.tense?.capitalize().replaceAll('_', ' ')} {mood}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="flex flex-col gap-1">
          {tenseBlock.conjugation.map((conjugation, index) => (
            <ConjugationCard key={index} conjugation={conjugation} />
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}

function SmallTenseCard({
  mood,
  tenseBlock,
}: {
  mood: string
  tenseBlock: Database__TenseBlock
}) {
  return (
    <Card
      className={cn(
        'w-84',
        colors[mood.toLowerCase().replaceAll(' ', '_')]?.[tenseBlock?.tense],
        tenseBlock.tense === 'participi' && 'mb-8'
      )}
    >
      <CardHeader>
        <CardTitle>
          {tenseBlock?.tense?.capitalize().replaceAll('_', ' ')}{' '}
          {mood !== 'Formes no personals' && mood}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {tenseBlock?.conjugation?.slice(0, 1).map((conjugation, index) => (
          <ConjugationCard key={index} conjugation={conjugation} />
        ))}
      </CardContent>
    </Card>
  )
}

export default function VerbTable({ data }: { data: Database__VerbOutput }) {
  return (
    <ScrollArea
      className={cn(
        'flex-1 rounded-md h-screen overflow-y-auto overflow-x-hidden whitespace-nowrap',
        'w-[448px] md:w-[800px] lg:w-[1000px] xl:w-full dark:bg-zinc-800 dark:text-white'
      )}
    >
      <div className="flex flex-col gap-4 pr-4">
        {(
          zip(
            data?.moods?.[0]?.tenses as Database__TenseBlock[],
            data?.moods?.[1]?.tenses as Database__TenseBlock[]
          ) as [Database__TenseBlock, Database__TenseBlock][]
        ).map(([indicatiu, subjuntiu], i) => (
          <ScrollArea className="w-full overflow-x-auto" key={i}>
            <section className="flex gap-4 w-max">
              <BigTenseCard mood="indicatiu" tenseBlock={indicatiu} />
              {subjuntiu?.tense && (
                <BigTenseCard mood="subjuntiu" tenseBlock={subjuntiu} />
              )}
            </section>
          </ScrollArea>
        ))}
        {data?.moods?.slice(2).map((moodBlock, i) => (
          <section
            className="flex flex-col gap-4 w-max"
            key={`${moodBlock.mood}-${i}`}
          >
            {moodBlock.tenses.map((tenseBlock) => (
              <SmallTenseCard
                key={`${moodBlock.mood}-${tenseBlock.tense}`}
                mood={moodBlock.mood}
                tenseBlock={tenseBlock}
              />
            ))}
          </section>
        ))}
      </div>
      <ScrollBar orientation="vertical" />
    </ScrollArea>
  )
}
