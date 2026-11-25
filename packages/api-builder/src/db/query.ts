/**
 * Helpers genéricos (agnósticos de dominio) para construir queries de MongoDB.
 * No conocen campos de negocio: el repository compone el filtro y toMongoQuery
 * solo normaliza (omite undefined).
 */

export function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/** Normaliza un filtro genérico a query de Mongo (omite claves undefined). */
export function toMongoQuery(filter: Record<string, unknown>): Record<string, unknown> {
  const query: Record<string, unknown> = {}
  for (const [key, value] of Object.entries(filter)) {
    if (value !== undefined) query[key] = value
  }
  return query
}

/** Filtro $or con regex insensible a mayúsculas sobre varios campos. */
export function orRegex(fields: string[], value: string): { $or: Array<Record<string, unknown>> } {
  return { $or: fields.map((f) => ({ [f]: { $regex: escapeRegExp(value), $options: 'i' } })) }
}

/** Condición "empieza por" insensible a mayúsculas. */
export function startsWith(value: string): { $regex: string; $options: string } {
  return { $regex: `^${escapeRegExp(value)}`, $options: 'i' }
}
