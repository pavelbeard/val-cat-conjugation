import * as React from 'react'
import { cn } from '@/lib/utils'

type SlotProps = React.HTMLAttributes<HTMLElement> & { children?: React.ReactNode }

/** Slot mínimo (sustituye a @radix-ui/react-slot): fusiona props y className en el único hijo. */
export function Slot({ children, className, ...props }: SlotProps) {
  if (!React.isValidElement(children)) return null
  const child = children as React.ReactElement<Record<string, unknown>>
  return React.cloneElement(child, {
    ...props,
    ...child.props,
    className: cn(className, child.props.className as string | undefined),
  })
}
