import { z } from 'zod'
import { isSchema } from './request.js'

/**
 * DSL de validadores: cada campo es un FieldBuilder que mw.validator
 * convierte a schema zod. P. ej.:
 *
 *   const search = {
 *     query: {
 *       form: validator.string.required(),
 *       verbose: validator.bool.notRequired().default(false),
 *     },
 *     params: { id: validator.stringRequired },
 *   }
 */
export type FieldType = 'string' | 'number' | 'boolean' | 'array' | 'object'

export interface FieldSpec {
  type: FieldType
  required: boolean
  hasDefault: boolean
  defaultValue?: unknown
}

export class FieldBuilder {
  readonly __field = true as const
  constructor(readonly spec: FieldSpec) {}
  required(): FieldBuilder {
    return new FieldBuilder({ ...this.spec, required: true })
  }
  notRequired(): FieldBuilder {
    return new FieldBuilder({ ...this.spec, required: false, hasDefault: false, defaultValue: undefined })
  }
  default(value: unknown): FieldBuilder {
    return new FieldBuilder({ ...this.spec, required: false, hasDefault: true, defaultValue: value })
  }
}

const makeType = (type: FieldType) => ({
  required: () => new FieldBuilder({ type, required: true, hasDefault: false }),
  notRequired: () => new FieldBuilder({ type, required: false, hasDefault: false }),
})

/** Objeto `validator` para construir los descriptores de los *.validator.ts */
export const validator = {
  string: makeType('string'),
  number: makeType('number'),
  bool: makeType('boolean'),
  boolean: makeType('boolean'),
  array: makeType('array'),
  object: makeType('object'),
  // shorthands
  stringRequired: makeType('string').required(),
  stringOptional: makeType('string').notRequired(),
  numberRequired: makeType('number').required(),
  numberOptional: makeType('number').notRequired(),
  boolRequired: makeType('boolean').required(),
  boolOptional: makeType('boolean').notRequired(),
}

type Where = 'params' | 'query' | 'body'

/** Descriptor de request: { params?, query?, body? } con FieldBuilders (o un FieldBuilder directo en body). */
export type RequestDescriptor = Partial<Record<Where, Record<string, FieldBuilder> | FieldBuilder>>

export function isDescriptor(v: unknown): v is RequestDescriptor {
  return typeof v === 'object' && v !== null && !isSchema(v as never)
}

function labelFor(where: Where, name: string): string {
  if (where === 'params') return `param "${name}"`
  if (where === 'query') return `query param "${name}"`
  return name
}

function fieldToZod(where: Where, name: string, spec: FieldSpec): z.ZodTypeAny {
  const requiredMsg = `${labelFor(where, name)} is required`
  let base: z.ZodTypeAny
  switch (spec.type) {
    case 'string':
      base = z.string({ error: requiredMsg })
      break
    case 'number':
      // coerce: en query llega como string ("3")
      base = z.coerce.number()
      break
    case 'boolean':
      // acepta booleano real (body) y "true"/"false" (query)
      base = z.union([
        z.boolean(),
        z.literal('true').transform(() => true as const),
        z.literal('false').transform(() => false as const),
      ])
      break
    case 'array':
      base = z.array(z.unknown())
      break
    case 'object':
      base = z.looseObject({})
      break
  }
  if (spec.required) {
    if (spec.type === 'string') return (base as z.ZodString).trim().min(1, requiredMsg)
    return base
  }
  if (spec.hasDefault) return base.default(spec.defaultValue)
  return base.optional()
}

/** Convierte un descriptor { params, query, body } en un schema zod del request completo. */
export function buildRequestSchema(d: RequestDescriptor) {
  const shape: Record<string, z.ZodTypeAny> = {}
  for (const where of ['params', 'query', 'body'] as const) {
    const part = d[where]
    if (!part) continue
    if (part instanceof FieldBuilder) {
      shape[where] = fieldToZod(where, where, part.spec)
    } else {
      const fields: Record<string, z.ZodTypeAny> = {}
      for (const [name, f] of Object.entries(part)) fields[name] = fieldToZod(where, name, f.spec)
      shape[where] = z.looseObject(fields as z.ZodRawShape)
    }
  }
  return z.looseObject(shape as z.ZodRawShape)
}
