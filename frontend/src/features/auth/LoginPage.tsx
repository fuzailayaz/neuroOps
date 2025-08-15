import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button, TextInput, PasswordInput, Card, Title, Text } from '@mantine/core';
import { authService } from '@/services/auth';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { notifications } from '@mantine/notifications';
import { useAuthStore } from '@/stores/auth';

const loginSchema = z.object({
  email: z.string()
    .min(1, 'Email is required')
    .email('Invalid email address'),
  password: z.string()
    .min(1, 'Password is required')
    .min(6, 'Password must be at least 6 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/';

  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const setUser = useAuthStore((state) => state.setUser);
  const setTokens = useAuthStore((state) => state.setTokens);

  const onSubmit = async (data: LoginFormData) => {
    try {
      const response = await authService.login({
        email: data.email,
        password: data.password
      });
      
      // Update auth store with user data
      if (response.user) {
        setUser({
          id: response.user.id.toString(),
          email: response.user.email,
          // Add any other required user fields here
        });
        
        setTokens({
          access: response.access,
          refresh: response.refresh
        });
      }
      
      // Show success message
      notifications.show({
        title: 'Login successful',
        message: `Welcome back, ${response.user?.first_name || 'User'}!`,
        color: 'green',
      });
      
      // Redirect to home or previous page
      navigate(from, { replace: true });
    } catch (error: any) {
      notifications.show({
        title: 'Login failed',
        message: error.message || 'Invalid email or password',
        color: 'red',
      });
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <Title order={2} className="text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </Title>
          <Text className="mt-2 text-sm text-gray-600">
            Or{' '}
            <Link to="/register" className="font-medium text-indigo-600 hover:text-indigo-500" style={{ textDecoration: 'none' }}>
              create a new account
            </Link>
          </Text>
        </div>
        <Card withBorder shadow="md" p="xl" className="mt-8">
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            <div className="space-y-4">
              <TextInput
                label="Email address"
                placeholder="you@example.com"
                required
                error={errors.email?.message}
                {...register('email')}
              />
              <PasswordInput
                label="Password"
                placeholder="••••••••"
                required
                error={errors.password?.message}
                {...register('password')}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                  Remember me
                </label>
              </div>

              <div className="text-sm">
                <Link to="/forgot-password" className="font-medium text-indigo-600 hover:text-indigo-500" style={{ textDecoration: 'none' }}>
                  Forgot your password?
                </Link>
              </div>
            </div>

            <div>
              <Button
                type="submit"
                fullWidth
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Sign in
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};
