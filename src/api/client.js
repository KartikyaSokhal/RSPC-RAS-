import axios from 'axios'

let csrfToken

function getCookie(name) {
  if (typeof document === 'undefined') return null
  const match = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]*)'))
  return match ? decodeURIComponent(match[2]) : null
}

export async function get(path, signal) {
  let response
  try { response = await axios.get(`/api${path}`, { signal, withCredentials: true }) }
  catch (error) { expireSession(error); throw error }
  const { data } = response
  if (path === '/config/' && data.csrf_token) csrfToken = data.csrf_token
  return data
}

export async function post(path, body, signal) {
  let token = getCookie('csrftoken') || csrfToken
  if (!token) {
    await get('/config/', signal)
    token = getCookie('csrftoken') || csrfToken
  }
  let response
  try { response = await axios.post(`/api${path}`, body, {
    signal,
    headers: { 'X-CSRFToken': token || '' },
    withCredentials: true,
  }) } catch (error) { expireSession(error); throw error }
  const { data } = response
  return data
}

function expireSession(error) {
  if (error?.response?.status === 401 && error?.response?.data?.error?.code === 'auth_required') {
    window.dispatchEvent(new Event('prepal:session-expired'))
  }
}

export function errorMessage(error, fallback = 'We could not load this page. Please try again.') {
  return error?.response?.data?.error?.message || error?.response?.data?.detail || fallback
}

export function resetClient() {
  csrfToken = undefined
}

