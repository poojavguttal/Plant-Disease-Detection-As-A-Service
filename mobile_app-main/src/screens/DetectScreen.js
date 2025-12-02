import { useMemo, useState } from 'react';
import { Image, StyleSheet, View } from 'react-native';
import { Button, Chip, HelperText, Text } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { colors, spacing } from '../theme';
import { useImagePicker } from '../hooks/useImagePicker';
import { usePrediction } from '../hooks/usePrediction';
import { AdviceModal } from '../components/AdviceModal';
import { LoadingOverlay } from '../components/LoadingOverlay';
import { formatConfidence } from '../utils/formatConfidence';

const languages = ['English', 'Hindi', 'Spanish'];

export function DetectScreen() {
  const { pickFromLibrary, captureWithCamera, pickerError } = useImagePicker();
  const {
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
  } = usePrediction();

  const [lang, setLang] = useState(languages[0]);
  const [adviceVisible, setAdviceVisible] = useState(false);

  const preview = useMemo(() => {
    if (!image) {
      return (
        <View style={styles.placeholder}>
          <MaterialCommunityIcons name="image-search-outline" size={48} color={colors.subtext} />
          <Text style={styles.placeholderText}>Upload a clear photo of the leaf</Text>
        </View>
      );
    }

    return <Image source={{ uri: image.uri }} style={styles.previewImage} />;
  }, [image]);

  const handlePick = async (source) => {
    const asset = source === 'camera' ? await captureWithCamera() : await pickFromLibrary();
    if (asset) {
      setError(null);
      setImage(asset);
    }
  };

  const handleDetect = async () => {
    await detect();
  };

  const handleAdvice = async () => {
    setAdviceVisible(true);
    await requestAdvice(lang);
  };

  const showError = error || pickerError;

  return (
    <View style={styles.container}>
      <View style={styles.controls}>
        <Button
          icon="image-multiple"
          mode="contained-tonal"
          onPress={() => handlePick('gallery')}
          style={styles.controlButton}
        >
          Open gallery
        </Button>
        <Button
          icon="camera"
          mode="contained"
          onPress={() => handlePick('camera')}
          style={styles.controlButton}
        >
          Start camera
        </Button>
      </View>

      <View style={styles.preview}>{preview}</View>

      <Button
        mode="contained"
        onPress={handleDetect}
        disabled={!image}
        style={styles.detectButton}
      >
        Detect
      </Button>

      {result ? (
        <View style={styles.resultCard}>
          <View style={styles.resultHeader}>
            <Text variant="titleMedium">{result.label}</Text>
            <Text style={styles.confidence}>{formatConfidence(result.confidence)}</Text>
          </View>

          <View style={styles.langRow}>
            <Text style={styles.langLabel}>Advice language</Text>
            <View style={styles.langChips}>
              {languages.map((option) => (
                <Chip
                  key={option}
                  selected={lang === option}
                  onPress={() => setLang(option)}
                  style={styles.chip}
                >
                  {option}
                </Chip>
              ))}
            </View>
          </View>

          <Button mode="outlined" onPress={handleAdvice} loading={adviceLoading}>
            Precaution
          </Button>
        </View>
      ) : null}

      <AdviceModal
        visible={adviceVisible}
        onDismiss={() => setAdviceVisible(false)}
        title={result?.label || 'Advice'}
        content={advice || 'Fetching guidance...'}
        loading={adviceLoading}
      />

      {showError ? (
        <HelperText type="error" visible>
          {showError}
        </HelperText>
      ) : null}
      {loading && <LoadingOverlay message="Analyzing leaf..." />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: spacing.lg,
    backgroundColor: colors.background,
    gap: spacing.md,
  },
  controls: {
    flexDirection: 'row',
    gap: spacing.md,
  },
  controlButton: {
    flex: 1,
    borderRadius: spacing.md,
  },
  preview: {
    height: 260,
    borderRadius: spacing.lg,
    overflow: 'hidden',
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholder: {
    justifyContent: 'center',
    alignItems: 'center',
    gap: spacing.sm,
  },
  placeholderText: {
    color: colors.subtext,
  },
  previewImage: {
    width: '100%',
    height: '100%',
  },
  detectButton: {
    borderRadius: spacing.md,
  },
  resultCard: {
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: spacing.lg,
    borderWidth: 1,
    borderColor: colors.border,
    gap: spacing.md,
  },
  resultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  confidence: {
    color: colors.accentGreen,
    fontWeight: '600',
  },
  langRow: {
    gap: spacing.sm,
  },
  langLabel: {
    color: colors.subtext,
  },
  langChips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },
  chip: {
    borderRadius: spacing.pill,
  },
});

