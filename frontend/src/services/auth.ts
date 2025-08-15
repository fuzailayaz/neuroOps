import { api } from '@/lib/api';
import { useAuthStore } from '@/stores/auth';

export interface LoginCredentials {
  username?: string;
  email?: string;
  password: string;
}

export interface RegisterData extends LoginCredentials {
  email: string;
  first_name: string;
  last_name: string;
  password2: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user?: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
  };
}

// Define and export the auth service methods
export const authService = {

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      // Send login request with email/username and password
      const loginData = {
        email: credentials.email,
        username: credentials.username,
        password: credentials.password
      };

      const response = await api.post('/api/auth/token/', loginData);
      
      // Store tokens
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      
      // Fetch user profile after successful login
      const userResponse = await this.getCurrentUser(response.data.access);
      
      return {
        access: response.data.access,
        refresh: response.data.refresh,
        user: userResponse
      };
    } catch (error: any) {
      console.error('Login error:', error);
      
      // Clear any invalid tokens
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      if (error.response) {
        console.error('Login response error:', error.response.data);
        
        // Handle different error statuses
        if (error.response.status === 401) {
          throw new Error('Invalid email/username or password');
        } else if (error.response.status === 400) {
          throw new Error(error.response.data?.detail || 'Invalid request');
        }
      }
      
      throw new Error('Login failed. Please try again.');
    }
  },

  /**
   * Formats validation errors into a user-friendly message
   */
  formatValidationErrors(data: Record<string, any>): string {
    const errorMessages: string[] = [];
    
    for (const [field, errors] of Object.entries(data)) {
      if (Array.isArray(errors)) {
        errorMessages.push(`${field}: ${errors.join(', ')}`);
      } else if (typeof errors === 'string') {
        errorMessages.push(errors);
      }
    }
    
    return errorMessages.join('\n');
  },

  /**
   * Handles API response errors
   */
  handleApiError(error: any): never {
    console.error('API Error:', error);

    if (!error.response) {
      if (error.request) {
        console.error('No response received:', error.request);
        throw new Error('No response from server. Please check your connection.');
      }
      console.error('Request setup error:', error.message);
      throw new Error(`Request failed: ${error.message}`);
    }

    const { status, data } = error.response;
    console.error(`Response status: ${status}`, data);

    // Handle 400 Bad Request with validation errors
    if (status === 400) {
      if (data?.detail) {
        throw new Error(data.detail);
      }
      if (data) {
        throw new Error(this.formatValidationErrors(data));
      }
    }

    // For other error statuses
    const errorMessage = data?.detail || data?.message || 'Registration failed. Please try again.';
    throw new Error(errorMessage);
  },

  /**
   * Registers a new user
   */
  async register(userData: RegisterData): Promise<{ user: any; message: string }> {
    try {
      const response = await api.post('/api/auth/register/', userData);
      return response.data;
    } catch (error: any) {
      this.handleApiError(error);
      // This line is unreachable because handleApiError always throws, but TypeScript needs it
      throw error;
    }
  },

  async refreshToken(refresh: string): Promise<{ access: string }> {
    const response = await api.post('/api/auth/token/refresh/', { refresh });
    return response.data;
  },

  async getCurrentUser(token?: string) {
    try {
      const config = token ? { headers: { Authorization: `Bearer ${token}` } } : {};
      const response = await api.get('/api/auth/profile/', config);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
      // Clear tokens on error
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      throw error;
    }
  },

  logout() {
    // Clear tokens from the store
    useAuthStore.getState().clearAuth();
  }
};
