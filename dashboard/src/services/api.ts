import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export interface SimplifyRequest {
  input: string
  format: 'text' | 'html'
  mode: 'easy' | 'light'
  glossary_id?: string
  preserve_html_tags?: boolean
  max_output_chars?: number
}

export interface SimplifyResponse {
  job_id: string
  status: string
  model_version: string
  output: string
  processing_time_ms: number
  cache_hit: boolean
}

export const translationAPI = {
  simplify: async (data: SimplifyRequest): Promise<SimplifyResponse> => {
    const response = await api.post('/v1/simplify', data)
    return response.data
  },

  getCacheStats: async () => {
    const response = await api.get('/v1/cache/stats')
    return response.data
  },

  flushCache: async () => {
    const response = await api.post('/v1/cache/flush')
    return response.data
  },
}

export const glossaryAPI = {
  getAll: async () => {
    const response = await api.get('/v1/glossaries')
    return response.data
  },

  create: async (data: any) => {
    const response = await api.post('/v1/glossaries', data)
    return response.data
  },

  update: async (id: string, data: any) => {
    const response = await api.put(`/v1/glossaries/${id}`, data)
    return response.data
  },

  delete: async (id: string) => {
    const response = await api.delete(`/v1/glossaries/${id}`)
    return response.data
  },
}

export default api
