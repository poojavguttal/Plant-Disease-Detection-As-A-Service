import { apiClient } from './client';

const formDataHeaders = { headers: { 'Content-Type': 'multipart/form-data' } };

export async function fetchAdvice(payload) {
  const { data } = await apiClient.post('/advice', payload);
  return data;
}

// api/predict.ts
import { Platform } from 'react-native';

export async function predictDisease(imageUri) {
  const formData = new FormData();

  if (Platform.OS === 'web') {
    // 🧠 Web: need a real Blob/File
    const res = await fetch(imageUri);
    const blob = await res.blob();

    // File is available in browsers
    const file = new File([blob], 'plant-leaf.jpg', {
      type: blob.type || 'image/jpeg',
    });

    formData.append('file', file);
  } else {
    // 📱 Native (iOS/Android): RN understands { uri, name, type }
    formData.append('file', {
      uri: imageUri,
      name: 'plant-leaf.jpg',
      type: 'image/jpeg',
    });
  }

  const { data } = await apiClient.post('/predict', formData, {
    headers: {
      // Let axios/RN handle boundary; this is usually enough
      'Content-Type': 'multipart/form-data',
    },
    // Make sure axios doesn't try to JSON.stringify the FormData
    transformRequest: (body) => body,
  });

  return data;
}
