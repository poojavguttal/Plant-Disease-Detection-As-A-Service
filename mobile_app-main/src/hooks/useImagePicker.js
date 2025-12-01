import { useCallback, useState } from 'react';
import * as ImagePicker from 'expo-image-picker';
import { Camera } from 'expo-camera';

export function useImagePicker() {
  const [error, setError] = useState(null);

  const pickFromLibrary = useCallback(async () => {
    try {
      setError(null);
      const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (status !== 'granted') {
        throw new Error('Media library permission is required.');
      }

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        quality: 0.8,
      });

      if (result.canceled) {
        return null;
      }

      return result.assets[0];
    } catch (err) {
      setError(err.message);
      return null;
    }
  }, []);

  const captureWithCamera = useCallback(async () => {
    try {
      setError(null);
      const { status } = await Camera.requestCameraPermissionsAsync();
      if (status !== 'granted') {
        throw new Error('Camera permission is required.');
      }

      const result = await ImagePicker.launchCameraAsync({
        allowsEditing: true,
        quality: 0.8,
      });

      if (result.canceled) {
        return null;
      }

      return result.assets[0];
    } catch (err) {
      setError(err.message);
      return null;
    }
  }, []);

  return {
    pickFromLibrary,
    captureWithCamera,
    pickerError: error,
    clearPickerError: () => setError(null),
  };
}

