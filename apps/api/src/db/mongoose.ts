/**
 * Wrapper de Mongoose: único punto de acceso a la conexión.
 * El resto de la app (repositories) usa los modelos, nunca mongoose directo.
 */
import mongoose, { type ClientSession } from 'mongoose'

export async function connectMongo(uri?: string) {
  if (!uri) throw new Error('MONGODB_URI is not set')
  await mongoose.connect(uri, { serverSelectionTimeoutMS: 5000 })
  console.log('Connected to MongoDB')
  return mongoose.connection
}

export async function disconnectMongo() {
  await mongoose.disconnect()
}

export function getConnection() {
  return mongoose.connection
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
