/**
 * Wrapper de la BBDD: único punto de acceso a MongoDB.
 * Los repositories usan db.getCollection('verbs').findOne(...) etc.,
 * nunca mongoose directamente.
 */
import mongoose, { type ClientSession } from 'mongoose'

export * from './query.js'

export async function connect(uri?: string) {
  if (!uri) throw new Error('MONGODB_URI is not set')
  await mongoose.connect(uri, { serverSelectionTimeoutMS: 5000 })
  console.log('Connected to MongoDB')
  return mongoose.connection
}

export async function disconnect() {
  await mongoose.disconnect()
}

export function getConnection() {
  return mongoose.connection
}

/** Devuelve la colección nativa de MongoDB (driver) por nombre. */
export function getCollection(name: string) {
  return mongoose.connection.collection(name)
}

/** Ejecuta fn dentro de una transacción de MongoDB. */
export async function withTransaction<T>(fn: (session: ClientSession) => Promise<T>): Promise<T> {
  const session = await mongoose.startSession()
  try {
    let result: T
    await session.withTransaction(async () => {
      result = await fn(session)
    })
    return result!
  } finally {
    await session.endSession()
  }
}

/** Punto único de entrada: db.connect(), db.getCollection('verbs'), db.withTransaction(...). */
export const db = { connect, disconnect, getConnection, getCollection, withTransaction }
export default db
