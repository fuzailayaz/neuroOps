// Design System Tokens for NeuroOps

export const theme = {
  // Color System
  colors: {
    // Primary Brand Colors
    primary: {
      50: '#FFF5F0',
      100: '#FFE8D9',
      200: '#FFD0B0',
      300: '#FFB180',
      400: '#FF8C42',
      500: '#F26207', // Primary brand orange
      600: '#D45300',
      700: '#B34600',
      800: '#8F3900',
      900: '#662800',
    },
    
    // Neutral Colors
    neutral: {
      25: '#FCFCFD',
      50: '#F9FAFB',
      100: '#F2F4F7',
      200: '#EAECF0',
      300: '#D0D5DD',
      400: '#98A2B3',
      500: '#667085',
      600: '#475467',
      700: '#344054',
      800: '#1D2939',
      900: '#101828',
    },
    
    // Semantic Colors
    success: {
      50: '#ECFDF3',
      100: '#D1FADF',
      500: '#12B76A',
      700: '#027A48',
    },
    warning: {
      50: '#FFFAEB',
      100: '#FEF0C7',
      500: '#F79009',
      700: '#B54708',
    },
    error: {
      50: '#FEF3F2',
      100: '#FEE4E2',
      500: '#F04438',
      700: '#B42318',
    },
    info: {
      50: '#EFF8FF',
      100: '#D1E9FF',
      500: '#2E90FA',
      700: '#175CD3',
    },
    
    // Surface Colors
    surface: {
      primary: '#FFFFFF',
      secondary: '#F9FAFB',
      tertiary: '#F2F4F7',
      dark: '#101828',
    },
    
    // Border Colors
    border: {
      light: '#EAECF0',
      default: '#D0D5DD',
      dark: '#98A2B3',
    },
  },
  // Spacing System (4px base unit)
  spacing: {
    px: '1px',
    0: '0',
    0.5: '0.125rem',  // 2px
    1: '0.25rem',     // 4px
    1.5: '0.375rem',  // 6px
    2: '0.5rem',      // 8px
    2.5: '0.625rem',  // 10px
    3: '0.75rem',     // 12px
    3.5: '0.875rem',  // 14px
    4: '1rem',        // 16px
    5: '1.25rem',     // 20px
    6: '1.5rem',      // 24px
    7: '1.75rem',     // 28px
    8: '2rem',        // 32px
    9: '2.25rem',     // 36px
    10: '2.5rem',     // 40px
    11: '2.75rem',    // 44px
    12: '3rem',       // 48px
    14: '3.5rem',     // 56px
    16: '4rem',       // 64px
    20: '5rem',       // 80px
    24: '6rem',       // 96px
    28: '7rem',       // 112px
    32: '8rem',       // 128px
    36: '9rem',       // 144px
    40: '10rem',      // 160px
    44: '11rem',      // 176px
    48: '12rem',      // 192px
    52: '13rem',      // 208px
    56: '14rem',      // 224px
    60: '15rem',      // 240px
    64: '16rem',      // 256px
    72: '18rem',      // 288px
    80: '20rem',      // 320px
    96: '24rem',      // 384px
  },
  // Border Radius
  borderRadius: {
    none: '0',
    xs: '0.125rem',  // 2px
    sm: '0.25rem',   // 4px
    DEFAULT: '0.375rem', // 6px
    md: '0.5rem',    // 8px
    lg: '0.75rem',   // 12px
    xl: '1rem',      // 16px
    '2xl': '1.5rem', // 24px
    '3xl': '2rem',   // 32px
    full: '9999px',
  },
  
  // Box Shadow
  boxShadow: {
    xs: '0px 1px 2px 0px rgba(16, 24, 40, 0.05)',
    sm: '0px 1px 3px 0px rgba(16, 24, 40, 0.10), 0px 1px 2px -1px rgba(16, 24, 40, 0.10)',
    DEFAULT: '0px 1px 2px 0px rgba(16, 24, 40, 0.06), 0px 1px 3px 0px rgba(16, 24, 40, 0.10)',
    md: '0px 2px 4px -1px rgba(16, 24, 40, 0.06), 0px 4px 6px -1px rgba(16, 24, 40, 0.10)',
    lg: '0px 4px 6px -2px rgba(16, 24, 40, 0.03), 0px 12px 16px -4px rgba(16, 24, 40, 0.08)',
    xl: '0px 8px 8px -4px rgba(16, 24, 40, 0.03), 0px 20px 24px -4px rgba(16, 24, 40, 0.08)',
    '2xl': '0px 24px 48px -12px rgba(16, 24, 40, 0.18)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    none: 'none',
  },
  
  // Typography
  fontFamily: {
    sans: ['Inter', 'sans-serif'],
    mono: ['Roboto Mono', 'monospace'],
  },
  
  // Z-Index
  zIndex: {
    hide: -1,
    auto: 'auto',
    base: 0,
    docked: 10,
    dropdown: 1000,
    sticky: 1100,
    banner: 1200,
    overlay: 1300,
    modal: 1400,
    popover: 1500,
    skipLink: 1600,
    toast: 1700,
    tooltip: 1800,
    10: '10',
    20: '20',
    30: '30',
    40: '40',
    50: '50',
  },
  // Add more theme values as needed
} as const;

export type Theme = typeof theme;
