/** Páginas a mostrar: 1 2 3 … n (con elipsis). delta = páginas alrededor de la actual (0 en móvil). */
export function pageItems(current: number, total: number, delta: number): (number | '…')[] {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const wanted = new Set([1, 2, total - 1, total])
  for (let p = current - delta; p <= current + delta; p++) wanted.add(p)
  const pages = [...wanted].filter((p) => p >= 1 && p <= total).sort((a, b) => a - b)
  const out: (number | '…')[] = []
  let prev = 0
  for (const p of pages) {
    if (p - prev > 1) out.push('…')
    out.push(p)
    prev = p
  }
  return out
}
