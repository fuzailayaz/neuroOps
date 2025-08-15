import React, { ReactNode, useState, useCallback } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { useAuthStore } from '@/stores/auth';
import { Navigate } from 'react-router-dom';
import { Box, useMantineColorScheme, Container } from '@mantine/core';
import { 
  IconLayoutDashboard, 
  IconSettings,
  IconMessage,
  IconBook
} from '@tabler/icons-react';

interface MainLayoutProps {
  children: ReactNode;
}

export const MainLayout = ({ children }: MainLayoutProps) => {
  const { isAuthenticated } = useAuthStore();
  const { colorScheme } = useMantineColorScheme();
  const [collapsed, setCollapsed] = useState(false);

  const toggleSidebar = useCallback(() => {
    setCollapsed((prev) => !prev);
  }, []);

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return (
    <Box
      style={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        backgroundColor: colorScheme === 'dark' ? 'var(--mantine-color-dark-8)' : 'var(--mantine-color-gray-0)',
      }}
    >
      <Header />
      <Box
        style={{
          display: 'flex',
          flex: 1,
          overflow: 'hidden',
          paddingTop: '64px', // Header height
        }}
      >
        <Box style={{ display: 'flex', width: '100%' }}>
          <Sidebar 
            collapsed={collapsed} 
            toggleSidebar={toggleSidebar}
            navItems={[
              { label: 'Dashboard', to: '/', icon: IconLayoutDashboard },
              { label: 'Chat', to: '/chat', icon: IconMessage },
              { label: 'Knowledge Base', to: '/knowledge', icon: IconBook },
              { label: 'Settings', to: '/settings', icon: IconSettings }
            ]}
          />
          <Box
            component="main"
            style={{
              flex: 1,
              overflow: 'auto',
              transition: 'all 0.2s ease-in-out',
              padding: '1.5rem',
              width: '100%',
              margin: '0 auto',
              maxWidth: '100%',
              '@media (min-width: 768px)': {
                maxWidth: 'calc(100% - 1rem)'
              }
            }}
          >
            <Container size="xl" p={0}>
              {children}
            </Container>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};
