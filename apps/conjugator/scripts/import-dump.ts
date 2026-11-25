/**
 * Importa los verbos desde dump/verbs/verbs.bson a MongoDB.
 * Uso: pnpm import:dump  (requiere MONGODB_URI en apps/conjugator/.env)
 *
 * Los ficheros .bson de mongodump son una concatenación de documentos BSON.
 * Los leemos secuencialmente y los insertamos por lotes.
 */
import { deserialize } from 'bson'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { db } from '@vcc/api-builder'
import 'dotenv/config'

const DUMP_PATH = resolve(
  import.meta.dirname ?? process.cwd(),
  '../../../dump/verbs/verbs.bson',
)

type VerbDoc = {
  infinitive?: string
  _id?: unknown
  [k: string]: unknown
}

async function* iterBson(path: string): AsyncGenerator<VerbDoc> {
  const buffer = readFileSync(path)
  let offset = 0
  while (offset + 5 <= buffer.length) {
    const size = buffer.readInt32LE(offset)
    if (size < 5 || offset + size > buffer.length) break
    yield deserialize(buffer.subarray(offset, offset + size)) as VerbDoc
    offset += size
  }
}

async function main() {
  if (!process.env.MONGODB_URI) throw new Error('MONGODB_URI is not set')
  await db.connect(process.env.MONGODB_URI)
  const verbs = db.getCollection('verbs')

  let count = 0
  const batch: Record<string, unknown>[] = []
  for await (const doc of iterBson(DUMP_PATH)) {
    // Normaliza el _id de Mongo y campos de fecha
    const clean = { ...doc } as Record<string, unknown>
    delete clean._id
    batch.push(clean)
    if (batch.length >= 100) {
      await verbs.insertMany(batch, { ordered: false })
      count += batch.length
      batch.length = 0
      console.log(`… ${count} verbos importados`)
    }
  }
  if (batch.length) {
    await verbs.insertMany(batch, { ordered: false })
    count += batch.length
  }
  console.log(`Total importado: ${count} verbos`)
  await db.disconnect()
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
