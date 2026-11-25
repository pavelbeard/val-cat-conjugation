import { error } from '@vcc/api-builder'
import { adminRepository } from './admin.repository.js'

/** Lógica de negocio del panel de administración (funciones async planas con el repository importado). */
export async function listVerbs() {
  return adminRepository.findAll()
}

export async function createVerb(data: Record<string, unknown>) {
  return adminRepository.create(data)
}

export async function updateVerb(infinitive: string, data: Record<string, unknown>) {
  const verb = await adminRepository.updateByInfinitive(infinitive, data)
  if (!verb) return error.notFound('Verb not found')
  return verb
}

export async function deleteVerb(infinitive: string) {
  const deleted = await adminRepository.deleteByInfinitive(infinitive)
  if (!deleted) return error.notFound('Verb not found')
  return deleted
}

export const adminBll = { listVerbs, createVerb, updateVerb, deleteVerb }
