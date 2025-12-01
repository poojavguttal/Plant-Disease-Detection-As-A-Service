export function formatConfidence(value) {
  if (value === undefined || value === null) {
    return '--';
  }
  return `${Math.round(value * 100)}% confidence`;
}

