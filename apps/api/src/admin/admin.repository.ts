import { Verb } from '../models/verb.js'

/** Acceso a la BBDD para el CRUD de administración. */
export const adminRepository = {
  findAll() {
    return Verb.find().sort({ infinitive: 1 }).lean()
  },

  create(data: Record<string, unknown>) {
    return Verb.create(data)
  },

  updateByInfinitive(infinitive: string, data: Record<string, unknown>) {
    return Verb.findOneAndUpdate({ infinitive }, data, { new: true }).lean()
  },

  deleteByInfinitive(infinitive: string) {
    return Verb.findOneAndDelete({ infinitive }).lean()
  },
}

export type AdminRepository = typeof adminRepository
