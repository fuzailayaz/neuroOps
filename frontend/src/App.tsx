import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Notifications } from '@mantine/notifications';
import { MantineProvider } from '@mantine/core';
import { ThemeProvider } from '@/theme/ThemeProvider';
import { MainLayout } from '@/components/layout/MainLayout';
import { LoginPage } from '@/features/auth/LoginPage';
import { RegisterPage } from '@/features/auth/RegisterPage';
import { DashboardPage } from '@/features/dashboard/DashboardPage';
import { ChatPage } from '@/features/chat/ChatPage';

// Create query client with default options
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <MantineProvider>
        <ThemeProvider>
          <Notifications position="top-right" />
          <Router>
            <Routes>
              {/* Public routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              
              {/* Protected routes */}
              <Route element={<MainLayout><Outlet /></MainLayout>}>
                <Route index element={<DashboardPage />} />
                <Route path="chat" element={<ChatPage />} />
                
                {/* Add more protected routes here */}
                
                {/* Catch all route */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Route>
            </Routes>
          </Router>
        </ThemeProvider>
      </MantineProvider>
    </QueryClientProvider>
  );
}

export default App;
