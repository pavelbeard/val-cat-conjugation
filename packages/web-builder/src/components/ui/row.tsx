import * as React from 'react'
import { cn } from '../../lib/utils'

const GAPS = {
  0: 'gap-0',
  1: 'gap-1',
  2: 'gap-2',
  3: 'gap-3',
  4: 'gap-4',
  6: 'gap-6',
  8: 'gap-8',
} as const
const ALIGNS = {
  start: 'items-start',
  center: 'items-center',
  end: 'items-end',
  baseline: 'items-baseline',
  stretch: 'items-stretch',
} as const
const JUSTIFYS = {
  start: 'justify-start',
  center: 'justify-center',
  end: 'justify-end',
  between: 'justify-between',
  around: 'justify-around',
} as const

type RowProps = React.ComponentProps<'div'> & {
  gap?: keyof typeof GAPS
  align?: keyof typeof ALIGNS
  justify?: keyof typeof JUSTIFYS
  wrap?: boolean
}

function Row({ gap = 0, align = 'center', justify, wrap, className, ...props }: RowProps) {
  return (
    <div
      data-slot="row"
      className={cn('flex', GAPS[gap], ALIGNS[align], justify && JUSTIFYS[justify], wrap && 'flex-wrap', className)}
      {...props}
    />
  )
}

export { Row }
