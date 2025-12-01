import { useCallback, useState } from 'react';
import { predictDisease, fetchAdvice } from '../api/predict';

export function usePrediction() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [advice, setAdvice] = useState(null);
  const [loading, setLoading] = useState(false);
  const [adviceLoading, setAdviceLoading] = useState(false);
  const [error, setError] = useState(null);

  const reset = useCallback(() => {
    setResult(null);
    setAdvice(null);
    setError(null);
  }, []);

  const detect = useCallback(async () => {
    if (!image) {
      setError('Select a leaf image first.');
      return null;
    }

    try {
      setError(null);
      setAdvice(null);
      setLoading(true);

      const prediction = await predictDisease(image.uri);
      setResult(prediction);
      return prediction;
    } catch (err) {
      setError('Unable to analyze the image. Please try again.');
      return null;
    } finally {
      setLoading(false);
    }
  }, [image]);

  const requestAdvice = useCallback(
    async (lang = 'English') => {
      if (!result) {
        setError('Run detection before requesting advice.');
        return null;
      }

      try {
        setError(null);
        setAdviceLoading(true);
        const response = await fetchAdvice({
          label: result.label,
          confidence: result.confidence,
          lang,
        });
        setAdvice(response.advice);
        return response.advice;
      } catch (err) {
        setError('Unable to fetch advice right now.');
        return null;
      } finally {
        setAdviceLoading(false);
      }
    },
    [result],
  );

  return {
    image,
    setImage,
    result,
    advice,
    loading,
    adviceLoading,
    error,
    setError,
    detect,
    requestAdvice,
    reset,
  };
}

