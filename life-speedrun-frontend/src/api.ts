// src/api.ts
const API_BASE = 'http://localhost:8000';

const handleResponse = async (res: Response) => {
  if (!res.ok) {
    let message = `HTTP ${res.status}`;
    try {
      const json = await res.json();
      message = json.detail || json.msg || message;
    } catch {}
    throw new Error(message);
  }
  return res.json();
};

export const api = {
  // Auth
  register: (email: string, password: string) =>
    fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    }).then(handleResponse),

  verify: (email: string, code: string) =>
    fetch(`${API_BASE}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, code })
    }).then(handleResponse),

  login: (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('email', email);
    formData.append('password', password);
    return fetch(`${API_BASE}/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString()
    }).then(handleResponse);
  },

  me: (token: string) =>
    fetch(`${API_BASE}/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    }).then(handleResponse),

  // Events
  createEvent: (token: string, event: {
    title: string;
    startTime: string;
    endTime: string;
    date: string;
    isRange: boolean;
    isRecurring: boolean;
    recurrenceDays: number;
    reminder: boolean;
    reminderMinutes: number;
    color: string;
    description: string | null;
    tags: number[];
  }) =>
    fetch(`${API_BASE}/events`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(event)
    }).then(handleResponse),

  getEvents: (token: string, date: string) =>
    fetch(`${API_BASE}/events?date=${date}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    }).then(handleResponse),

  // Token helpers
  setToken: (token: string) => localStorage.setItem('jwt_token', token),
  getToken: () => localStorage.getItem('jwt_token'),
  clearToken: () => localStorage.removeItem('jwt_token')
};