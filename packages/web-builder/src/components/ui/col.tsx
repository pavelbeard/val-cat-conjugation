import * as React from 'react'
import { cn } from '../../lib/utils'

const GAPS = {
  0: 'gap-0',
  0.5: 'gap-0.5',
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
  stretch: 'items-stretch',
} as const
const JUSTIFYS = {
  start: 'justify-start',
  center: 'justify-center',
  end: 'justify-end',
  between: 'justify-between',
} as const

type ColProps = React.ComponentProps<'div'> & {
  gap?: keyof typeof GAPS
  align?: keyof typeof ALIGNS
  justify?: keyof typeof JUSTIFYS
  grow?: boolean
}

function Col({ gap = 0, align, justify, grow, className, ...props }: ColProps) {
  return (
    <div
      data-slot="col"
      className={cn(
        'flex flex-col',
        GAPS[gap],
        align && ALIGNS[align],
        justify && JUSTIFYS[justify],
        grow && 'flex-1',
        className,
      )}
      {...props}
    />
  )
}

export { Col }
