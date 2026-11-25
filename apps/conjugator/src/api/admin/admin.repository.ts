import { db } from '@vcc/api-builder'

const COLLECTION = 'verbs'

/** Acceso a la BBDD para el CRUD de administración. Toda query pasa por db.getCollection(COLLECTION). */
export async function findAll() {
  return db.getCollection(COLLECTION).find().sort({ infinitive: 1 }).toArray()
}

export async function create(data: Record<string, unknown>) {
  const now = new Date()
  const doc = { ...data, created_at: now, updated_at: now }
  await db.getCollection(COLLECTION).insertOne(doc)
  return doc
}

export async function updateByInfinitive(infinitive: string, data: Record<string, unknown>) {
  return db
    .getCollection(COLLECTION)
    .findOneAndUpdate(
      { infinitive },
      { $set: { ...data, updated_at: new Date() } },
      { returnDocument: 'after' },
    )
}

export async function deleteByInfinitive(infinitive: string) {
  return db.getCollection(COLLECTION).findOneAndDelete({ infinitive })
}

export const adminRepository = { findAll, create, updateByInfinitive, deleteByInfinitive }
export type AdminRepository = typeof adminRepository
