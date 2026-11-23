import { NotFoundError } from '../errors.js'
import { adminRepository, type AdminRepository } from './admin.repository.js'

/**
 * Lógica de negocio del panel de administración.
 * La validación de payload HTTP vive en middlewares/validate.ts.
 */
export function createAdminBll(repo: AdminRepository = adminRepository) {
  return {
    listVerbs() {
      return repo.findAll()
    },

    async createVerb(data: Record<string, unknown>) {
      return repo.create(data)
    },

    async updateVerb(infinitive: string, data: Record<string, unknown>) {
      const verb = await repo.updateByInfinitive(infinitive, data)
      if (!verb) throw new NotFoundError('Verb not found')
      return verb
    },

    async deleteVerb(infinitive: string) {
      const deleted = await repo.deleteByInfinitive(infinitive)
      if (!deleted) throw new NotFoundError('Verb not found')
      return deleted
    },
  }
}

export type AdminBll = ReturnType<typeof createAdminBll>
