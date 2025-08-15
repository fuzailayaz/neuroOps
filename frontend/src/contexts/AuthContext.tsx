import { createContext, useContext, useEffect, ReactNode } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useAuthStore } from '@/stores/auth';
import { authService } from '@/services/auth';

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: any; // Replace 'any' with your User type
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const { isAuthenticated, user, setUser } = useAuthStore();
  const queryClient = useQueryClient();

  const { isLoading } = useQuery({
    queryKey: ['user'],
    queryFn: authService.getCurrentUser,
    enabled: isAuthenticated && !user,
    onSuccess: (data) => {
      setUser(data);
    },
    onError: () => {
      useAuthStore.getState().clearAuth();
    },
  });

  // Effect to handle token refresh on mount if we have a refresh token
  useEffect(() => {
    const { refreshToken } = useAuthStore.getState();
    if (refreshToken && !isAuthenticated) {
      authService.refreshToken().catch(() => {
        useAuthStore.getState().clearAuth();
      });
    }
  }, [isAuthenticated]);

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
