import { useContext } from 'react'
import { AuthContext } from '../context/authContextDef.js'

export function useAuth() {
  return useContext(AuthContext)
}

export default useAuth
