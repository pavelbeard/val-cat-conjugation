export class ApiClient {
  static async get<T>(url: string, options?: RequestInit): Promise<T> {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`Failed to fetch from ${url}: ${response.statusText}`)
    }

    return response.json() as Promise<T>
  }

  static async post<T>(
    url: string,
    data: any,
    options?: RequestInit
  ): Promise<T> {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(data),
      ...options,
    })

    if (!response.ok) {
      throw new Error(`Failed to post to ${url}: ${response.statusText}`)
    }

    return response.json() as Promise<T>
  }

  static async put<T>(
    url: string,
    data: any,
    options?: RequestInit
  ): Promise<T> {
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      ...options,
    })

    if (!response.ok) {
      throw new Error(`Failed to put to ${url}: ${response.statusText}`)
    }

    return response.json() as Promise<T>
  }

  static async delete(url: string): Promise<boolean> {
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`Failed to delete from ${url}: ${response.statusText}`)
    }

    return true
  }
}
