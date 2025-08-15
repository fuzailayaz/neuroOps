import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button, TextInput, PasswordInput, Card, Title, Text } from '@mantine/core';
import { useMutation } from '@tanstack/react-query';
import { authService } from '@/services/auth';
import { Link, useNavigate } from 'react-router-dom';
import { notifications } from '@mantine/notifications';

const registerSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters'),
  email: z.string()
    .min(1, 'Email is required')
    .email('Invalid email address'),
  first_name: z.string()
    .min(1, 'First name is required'),
  last_name: z.string()
    .min(1, 'Last name is required'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters'),
  password2: z.string()
    .min(8, 'Please confirm your password'),
}).refine((data) => data.password === data.password2, {
  message: "Passwords don't match",
  path: ["password2"],
});

type RegisterFormData = z.infer<typeof registerSchema>;

export const RegisterPage = () => {
  const navigate = useNavigate();

  const { register, handleSubmit, formState: { errors } } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const registerMutation = useMutation({
    mutationFn: (data: RegisterFormData) => 
      authService.register({
        username: data.username,
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
        password: data.password,
        password2: data.password2
      }),
    onSuccess: () => {
      notifications.show({
        title: 'Registration successful',
        message: 'Please check your email to verify your account',
        color: 'green',
      });
      navigate('/login');
    },
    onError: (error: any) => {
      console.error('Registration error:', error);
      let errorMessage = 'An error occurred during registration';
      
      // Handle different types of errors
      if (error.message) {
        // Handle duplicate username/email errors
        if (error.message.includes('already exists')) {
          if (error.message.includes('username') && error.message.includes('email')) {
            errorMessage = 'Both username and email are already in use. Please try different ones.';
          } else if (error.message.includes('username')) {
            errorMessage = 'This username is already taken. Please choose a different one.';
          } else if (error.message.includes('email')) {
            errorMessage = 'This email is already registered. Please use a different email or log in.';
          } else {
            errorMessage = error.message.split('\n')[0];
          }
        } else {
          errorMessage = error.message;
        }
      }
      
      notifications.show({
        title: 'Registration failed',
        message: errorMessage,
        color: 'red',
        autoClose: 5000,
      });
    },
  });

  const onSubmit = (data: RegisterFormData) => {
    registerMutation.mutate(data);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <Title order={2} className="text-3xl font-extrabold text-gray-900">
            Create a new account
          </Title>
          <Text className="mt-2 text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
              Sign in here
            </Link>
          </Text>
        </div>
        <Card withBorder shadow="md" p="xl" className="mt-8">
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            <div className="space-y-4">
              <TextInput
                label="Username"
                placeholder="johndoe"
                required
                error={errors.username?.message}
                {...register('username')}
              />
              <TextInput
                label="Email address"
                placeholder="you@example.com"
                required
                error={errors.email?.message}
                {...register('email')}
              />
              <TextInput
                label="First Name"
                placeholder="John"
                required
                error={errors.first_name?.message}
                {...register('first_name')}
              />
              <TextInput
                label="Last Name"
                placeholder="Doe"
                required
                error={errors.last_name?.message}
                {...register('last_name')}
              />
              <PasswordInput
                label="Password"
                placeholder="••••••••"
                required
                error={errors.password?.message}
                {...register('password')}
              />
              <PasswordInput
                label="Confirm Password"
                placeholder="••••••••"
                required
                error={errors.password2?.message}
                {...register('password2')}
              />
            </div>

            <div>
              <Button
                type="submit"
                fullWidth
                loading={registerMutation.isPending}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Create account
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};
