import React from 'react';
import { useAuthStore } from '@/stores/auth';
import { ActionIcon, Avatar, Box, Group, Text, useMantineColorScheme } from '@mantine/core';
import { IconSun, IconMoonStars, IconBell, IconSearch, IconLogout } from '@tabler/icons-react';

export const Header = () => {
  const { user, logout } = useAuthStore();
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  const isDark = colorScheme === 'dark';

  // Get user initials for avatar
  const getUserInitials = (user: any) => {
    if (!user) return 'U';
    if (user.first_name && user.last_name) {
      return `${user.first_name[0]}${user.last_name[0]}`.toUpperCase();
    }
    if (user.username) {
      return user.username[0].toUpperCase();
    }
    return user.email ? user.email[0].toUpperCase() : 'U';
  };
  
  const userInitials = getUserInitials(user);

  return (
    <Box
      component="header"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        height: '64px',
        backgroundColor: 'var(--mantine-color-body)',
        borderBottom: '1px solid var(--mantine-color-gray-3)',
        zIndex: 100,
        padding: '0 1.5rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}
    >
      <Group gap="lg" align="center">
        <Text 
          component="span" 
          style={{
            fontSize: '1.25rem',
            fontWeight: 700,
            background: 'linear-gradient(90deg, #F26207 0%, #FF8C42 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          NeuroOps
        </Text>
        
        <Box
          style={{
            position: 'relative',
            display: 'none',
            '@media (min-width: 768px)': {
              display: 'block',
            },
          }}
        >
          <ActionIcon
            size="lg"
            variant="subtle"
            style={{
              position: 'absolute',
              left: '0.5rem',
              top: '50%',
              transform: 'translateY(-50%)',
              color: 'var(--mantine-color-gray-6)',
            }}
          >
            <IconSearch size={18} />
          </ActionIcon>
          <input
            type="text"
            placeholder="Search..."
            style={{
              padding: '0.5rem 1rem 0.5rem 2.5rem',
              borderRadius: '0.375rem',
              border: '1px solid var(--mantine-color-gray-3)',
              backgroundColor: 'var(--mantine-color-body)',
              width: '240px',
              fontSize: '0.875rem',
            }}
          />
        </Box>
      </Group>
      
      <Group gap="md">
        <ActionIcon
          variant="outline"
          color={isDark ? 'yellow' : 'blue'}
          onClick={() => toggleColorScheme()}
          title="Toggle color scheme"
        >
          {isDark ? <IconSun size={18} /> : <IconMoonStars size={18} />}
        </ActionIcon>
        
        <ActionIcon 
          variant="subtle" 
          size="lg" 
          aria-label="Notifications"
          style={{
            color: 'var(--mantine-color-gray-7)',
          }}
        >
          <IconBell size={20} />
        </ActionIcon>
        
        <Group gap="sm" style={{ cursor: 'pointer' }}>
          <Avatar 
            
            alt={user?.username || 'User'} 
            radius="xl"
            size="md"
            style={{
              border: '2px solid var(--mantine-color-gray-2)',
            }}
          >
            {userInitials}
          </Avatar>
          <Box style={{ display: 'none', '@media (min-width: 768px)': { display: 'block' } }}>
            <Text size="sm" fw={600} style={{ lineHeight: 1.2 }}>
              {user?.first_name || user?.username || 'User'}
            </Text>
            <Text size="xs" color="dimmed" style={{ lineHeight: 1.2 }}>
              {user?.email}
            </Text>
          </Box>
          <ActionIcon
            variant="subtle"
            onClick={logout}
            title="Sign out"
            style={{
              color: 'var(--mantine-color-gray-7)',
            }}
          >
            <IconLogout size={20} />
          </ActionIcon>
        </Group>
      </Group>
    </Box>
  );
};
