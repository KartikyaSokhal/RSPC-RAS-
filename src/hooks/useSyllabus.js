import { useContext } from 'react'
import { SyllabusContext } from '../components/study/syllabusContext.js'

export default function useSyllabus() {
  return useContext(SyllabusContext)
}
