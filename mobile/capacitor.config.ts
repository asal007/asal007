import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'de.meinimmokauf.app',
  appName: 'MeinImmoKauf',
  webDir: 'www',
  bundledWebRuntime: false,
  server: {
    androidScheme: 'https',
    url: 'https://meinimmokauf.onrender.com', // Produktions-URL (Render)
    cleartext: false,
  },
  ios: {
    contentInset: 'automatic',
  },
  android: {
    allowMixedContent: false,
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 3000,
      launchAutoHide: true,
      androidScaleType: 'CENTER_CROP',
      androidSpinnerStyle: 'large',
      iosSpinnerStyle: 'small',
      splashImmersive: false,
      showSpinner: true,
    },
    StatusBar: {
      style: 'dark',
      backgroundColor: '#0f172a',
    },
  },
};

export default config;
