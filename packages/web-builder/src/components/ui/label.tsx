import * as React from 'react'
import { cn } from '../../lib/utils'

function Label({ className, ...props }: React.ComponentProps<'label'>) {
  return (
    <label
      data-slot="label"
      className={cn('flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400', className)}
      {...props}
    />
  )
}

export { Label }
