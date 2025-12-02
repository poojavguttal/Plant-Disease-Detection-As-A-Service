import axios from 'axios';
import { Platform } from 'react-native';

const fallbackHost =
  Platform.OS === 'web' ? 'http://localhost:8000' : 'http://192.168.1.10:8000';

const baseURL = process.env.EXPO_PUBLIC_API_URL || fallbackHost;

export const apiClient = axios.create({
  baseURL,
  timeout: 20000,
});

