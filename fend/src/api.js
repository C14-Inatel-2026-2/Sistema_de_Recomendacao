import axios from 'axios';

const bruto = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
const baseURL = (/^https?:\/\//.test(bruto) ? bruto : `https://${bruto}`).replace(/\/+$/, '');

const api = axios.create({ baseURL });

export default api;
