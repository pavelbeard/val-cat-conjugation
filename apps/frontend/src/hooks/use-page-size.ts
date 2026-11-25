import { useState } from 'react'

export const PAGE_SIZES = [10, 25, 50] as const
const PAGE_SIZE_KEY = 'vcc-page-size'

function storedPageSize(): number {
  const v = Number(localStorage.getItem(PAGE_SIZE_KEY))
  return (PAGE_SIZES as readonly number[]).includes(v) ? v : 50
}

/** Tamaño de página persistido en localStorage. */
export function usePageSize() {
  const [pageSize, setPageSizeState] = useState(storedPageSize)

  const setPageSize = (n: number) => {
    localStorage.setItem(PAGE_SIZE_KEY, String(n))
    setPageSizeState(n)
  }

  return { pageSize, setPageSize }
}
