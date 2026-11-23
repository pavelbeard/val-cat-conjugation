import mongoose from 'mongoose'
import { connectMongo, disconnectMongo } from '../src/db/mongoose.js'

export const TEST_URI = process.env.MONGODB_URI ?? 'mongodb://localhost:27017/conjugador_test'

export async function setupTestDb() {
  await connectMongo(TEST_URI)
  await mongoose.connection.collection('verbs').deleteMany({})
}

export async function teardownTestDb() {
  await mongoose.connection.collection('verbs').deleteMany({})
  await disconnectMongo()
}

export const ANAR_FIXTURE = {
  infinitive: 'anar',
  translation: 'ir',
  moods: [
    {
      mood: 'indicatiu',
      tenses: [
        {
          tense: 'present',
          conjugation: [
            { pronoun: 'jo', forms: ['vaig'], variation_types: null, translation: 'voy' },
            { pronoun: 'tu', forms: ['vas'], variation_types: null, translation: 'vas' },
            { pronoun: 'ell, ella, vostè', forms: ['va'], variation_types: null, translation: 'va' },
          ],
        },
      ],
    },
  ],
}
