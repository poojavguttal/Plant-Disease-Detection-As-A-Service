import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { PaperProvider } from 'react-native-paper';
import RootNavigator from './navigation';
import { paperTheme } from './theme/paper';

export default function MobileApp() {
  return (
    <PaperProvider theme={paperTheme}>
      <SafeAreaProvider>
        <StatusBar style="dark" />
        <RootNavigator />
      </SafeAreaProvider>
    </PaperProvider>
  );
}

