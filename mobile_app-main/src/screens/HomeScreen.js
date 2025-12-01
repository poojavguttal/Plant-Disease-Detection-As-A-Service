import { ScrollView, StyleSheet, View } from 'react-native';
import { Text, Button } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { colors, spacing } from '../theme';
import { WeatherCard } from '../components/WeatherCard';

const crops =
  'apple, blueberry, cherry, corn, grape, orange, peach, pepper, potato, tomato, raspberry, strawberry';

const steps = [
  { icon: 'camera-outline', label: 'Take a picture' },
  { icon: 'cellphone-information', label: 'Get the result' },
  { icon: 'lab-flask', label: 'Get diagnosis' },
];

export function HomeScreen({ navigation }) {
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.hero}>
        <Text variant="labelLarge" style={styles.tag}>
          Pests
        </Text>
        <Text variant="headlineMedium" style={styles.heroTitle}>
          Heal your crop
        </Text>
        <Text style={styles.heroBody}>
          Available crops: {crops}
        </Text>
      </View>

      <View style={styles.stepsCard}>
        {steps.map((step, index) => (
          <View key={step.label} style={styles.step}>
            <View style={styles.stepIcon}>
              <MaterialCommunityIcons name={step.icon} size={24} color={colors.accentGreen} />
            </View>
            <Text style={styles.stepText}>{step.label}</Text>
            {index < steps.length - 1 && <View style={styles.arrow} />}
          </View>
        ))}
      </View>

      <Button
        mode="contained"
        style={styles.cta}
        contentStyle={styles.ctaContent}
        onPress={() => navigation.navigate('Detect')}
      >
        Take a picture
      </Button>

      <View style={styles.section}>
        <Text variant="titleMedium">Weather</Text>
        <WeatherCard />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    backgroundColor: colors.background,
    padding: spacing.lg,
    gap: spacing.lg,
  },
  hero: {
    backgroundColor: colors.accentPeach,
    padding: spacing.lg,
    borderRadius: spacing.lg,
  },
  tag: {
    color: colors.text,
  },
  heroTitle: {
    marginTop: spacing.sm,
    fontWeight: '700',
  },
  heroBody: {
    marginTop: spacing.sm,
    color: colors.text,
  },
  stepsCard: {
    backgroundColor: colors.surface,
    borderRadius: spacing.lg,
    padding: spacing.lg,
    borderWidth: 1,
    borderColor: colors.border,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  step: {
    alignItems: 'center',
    flex: 1,
    gap: spacing.sm,
  },
  stepIcon: {
    width: 56,
    height: 56,
    borderRadius: spacing.lg,
    borderWidth: 1,
    borderColor: colors.accentGreen,
    justifyContent: 'center',
    alignItems: 'center',
  },
  stepText: {
    textAlign: 'center',
    color: colors.text,
  },
  arrow: {
    position: 'absolute',
    right: -spacing.md,
    top: 28,
    width: spacing.md,
    height: 2,
    backgroundColor: colors.border,
  },
  cta: {
    borderRadius: spacing.lg,
  },
  ctaContent: {
    paddingVertical: spacing.sm,
  },
  section: {
    marginTop: spacing.md,
    gap: spacing.md,
  },
});

