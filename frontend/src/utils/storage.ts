const storage = {
  get(key: string): string | null {
    if (typeof localStorage === 'undefined') {
      return null
    }
    try {
      return localStorage.getItem(key)
    } catch {
      return null
    }
  },

  set(key: string, value: string): void {
    if (typeof localStorage === 'undefined') {
      return
    }
    try {
      localStorage.setItem(key, value)
    } catch {
      // ignore
    }
  },

  remove(key: string): void {
    if (typeof localStorage === 'undefined') {
      return
    }
    try {
      localStorage.removeItem(key)
    } catch {
      // ignore
    }
  },

  clear(): void {
    if (typeof localStorage === 'undefined') {
      return
    }
    try {
      localStorage.clear()
    } catch {
      // ignore
    }
  },

  getJSON<T = any>(key: string): T | null {
    const value = this.get(key)
    if (!value) {
      return null
    }
    try {
      return JSON.parse(value) as T
    } catch {
      return null
    }
  },

  setJSON(key: string, value: any): void {
    try {
      this.set(key, JSON.stringify(value))
    } catch {
      // ignore
    }
  }
}

export default storage
