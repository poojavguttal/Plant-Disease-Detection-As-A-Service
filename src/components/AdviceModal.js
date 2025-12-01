import React from 'react';
import { StyleSheet, View, ScrollView, Platform } from 'react-native';
import Markdown from 'react-native-markdown-display';
import { Modal, Portal, Text, Button, ActivityIndicator } from 'react-native-paper';
import { colors, spacing } from '../theme';

function AdviceBody({ content }) {
  const safeContent = typeof content === 'string' ? content : '';

  if (Platform.OS === 'web') {
    // On web: avoid react-native-markdown-display (it’s causing the node.children error)
    return (
      <Text style={styles.body}>
        {safeContent}
      </Text>
    );
  }

  // On native (Android / iOS): use markdown renderer
  return (
    <Markdown style={markdownStyles}>
      {safeContent}
    </Markdown>
  );
}

export function AdviceModal({ visible, onDismiss, title, content, loading }) {
  return (
    <Portal>
      <Modal
        visible={visible}
        onDismiss={onDismiss}
        contentContainerStyle={styles.modalContainer}
        style={{ justifyContent: 'center' }}
      >
        <View style={styles.badge} />
        <Text variant="titleMedium" style={styles.title}>
          {title}
        </Text>

        {loading ? (
          <ActivityIndicator animating size="small" />
        ) : (
          <ScrollView
            style={styles.scroll}
            persistentScrollbar={true}                // always show scrollbar
            showsVerticalScrollIndicator={true}
            indicatorStyle="black"
            scrollIndicatorInsets={{ right: 1 }}      // makes scrollbar look slimmer
          >
            <AdviceBody content={content} />
          </ScrollView>
        )}

        <Button mode="contained" onPress={onDismiss} style={styles.button}>
          Got it
        </Button>
      </Modal>
    </Portal>
  );
}

const styles = StyleSheet.create({
  modalContainer: {
    backgroundColor: colors.surface,
    padding: spacing.lg,
    borderRadius: spacing.lg,
    width: '85%',
    alignSelf: 'center',
    maxHeight: '70%',
  },
  scroll: {
    marginBottom: spacing.lg,
  },
  badge: {
    alignSelf: 'center',
    width: 48,
    height: 4,
    borderRadius: spacing.pill,
    backgroundColor: colors.accentGreen,
    marginBottom: spacing.md,
  },
  title: {
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  body: {
    color: colors.subtext,
    fontSize: 15,
    lineHeight: 22,
  },
  button: {
    borderRadius: spacing.md,
    marginTop: spacing.md,
  },
});

const markdownStyles = {
  body: {
    color: colors.subtext,
    fontSize: 15,
    lineHeight: 22,
  },
};
