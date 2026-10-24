import axios from 'axios'

let csrfToken

function getCookie(name) {
  if (typeof document === 'undefined') return null
  const match = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]*)'))
  return match ? decodeURIComponent(match[2]) : null
}

export async function get(path, signal) {
  const { data } = await axios.get(`/api${path}`, { signal, withCredentials: true })
  if (path === '/config/' && data.csrf_token) csrfToken = data.csrf_token
  return data
}

export async function post(path, body, signal) {
  let token = getCookie('csrftoken') || csrfToken
  if (!token) {
    await get('/config/', signal)
    token = getCookie('csrftoken') || csrfToken
  }
  const { data } = await axios.post(`/api${path}`, body, {
    signal,
    headers: { 'X-CSRFToken': token || '' },
    withCredentials: true,
  })
  return data
}

export function errorMessage(error, fallback = 'We could not load this page. Please try again.') {
  return error?.response?.data?.error?.message || error?.response?.data?.detail || fallback
}

export function resetClient() {
  csrfToken = undefined
}

