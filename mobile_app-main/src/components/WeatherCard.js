import { StyleSheet, View } from 'react-native';
import { Text } from 'react-native-paper';
import { colors, spacing } from '../theme';

export function WeatherCard({ temperature = 58.1, condition = 'Overcast clouds' }) {
  return (
    <View style={styles.card}>
      <View>
        <Text variant="titleLarge">{temperature}°C</Text>
        <Text style={styles.caption}>{condition}</Text>
      </View>
      <View style={styles.badge}>
        <Text style={styles.badgeText}>Today</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: spacing.md,
    borderColor: colors.border,
    borderWidth: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  caption: {
    color: colors.subtext,
    marginTop: 4,
    textTransform: 'capitalize',
  },
  badge: {
    backgroundColor: colors.accentPeach,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: spacing.pill,
  },
  badgeText: {
    color: colors.dark,
    fontWeight: '600',
  },
});

