import { createContext } from 'react'

export const AuthContext = createContext({
  user: null,
  authenticated: false,
  loading: true,
  login: async () => {},
  register: async () => {},
  logout: async () => {},
  refreshStatus: async () => {},
})

export default AuthContext
