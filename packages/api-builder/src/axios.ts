import axios, { type AxiosInstance } from 'axios'
import type { Request } from 'express'

/** Headers de la petición entrante que se propagan a las llamadas salientes. */
const FORWARDED_HEADERS = [
  'authorization',
  'content-type',
  'accept',
  'accept-language',
  'user-agent',
  'x-forwarded-for',
  'x-real-ip',
]

/**
 * Builder de instancias axios.
 * recoge los headers de la petición entrante (y los que se añadan a mano)
 * y construye la instancia lista para llamar a otros servicios:
 *
 *   const http = AxiosBuilder.fromRequest(req).withBaseURL('https://api.mistral.ai').build()
 *   const { data } = await http.get('/v1/models')
 */
export class AxiosBuilder {
  private headers: Record<string, string> = {}
  private baseURL?: string

  private constructor(private readonly req?: Request) {}

  static fromRequest(req?: Request): AxiosBuilder {
    return new AxiosBuilder(req)
  }

  withBaseURL(baseURL: string): this {
    this.baseURL = baseURL
    return this
  }

  withHeader(name: string, value: string): this {
    this.headers[name] = value
    return this
  }

  withHeaders(headers: Record<string, string>): this {
    Object.assign(this.headers, headers)
    return this
  }

  /** Construye la instancia axios con los headers recogidos. */
  build(): AxiosInstance {
    const forwarded: Record<string, string> = {}
    if (this.req) {
      for (const name of FORWARDED_HEADERS) {
        const value = this.req.headers[name]
        if (typeof value === 'string') forwarded[name] = value
      }
    }
    return axios.create({
      baseURL: this.baseURL,
      headers: { ...forwarded, ...this.headers },
    })
  }
}
