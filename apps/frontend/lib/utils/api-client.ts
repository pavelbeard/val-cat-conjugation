import { withErrorHandler } from "./error-handler";

export class ApiClient {
  static async get<T>(url: string, options?: RequestInit): Promise<T> {
    const response = await withErrorHandler(async () =>
      fetch(url, { method: "GET", ...options })
    )();

    return response.json() as Promise<T>;
  }

  static async post<T>(
    url: string,
    data: any,
    options?: RequestInit
  ): Promise<T> {
    const response = await withErrorHandler(async () =>
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify(data),
        ...options,
      })
    )();

    return response.json() as Promise<T>;
  }

  static async put<T>(
    url: string,
    data: any,
    options?: RequestInit
  ): Promise<T> {
    const response = await withErrorHandler(async () =>
      fetch(url, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        ...options,
      })
    )();

    return response.json() as Promise<T>;
  }

  static async delete(url: string): Promise<boolean> {
    const response = await withErrorHandler(async () =>
      fetch(url, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      })
    )();

    return response.ok;
  }
}
