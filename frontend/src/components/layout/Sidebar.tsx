import React, { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { 
  Box, 
  Tooltip, 
  useMantineTheme,
  useMantineColorScheme,
  rgba,
  MantineTheme
} from '@mantine/core';
import { 
  IconHome, 
  IconLayoutDashboard, 
  IconSettings, 
  IconLayoutSidebarLeftCollapse, 
  IconLayoutSidebarLeftExpand 
} from '@tabler/icons-react';

// Constants
const COLLAPSED_WIDTH = 60;
const EXPANDED_WIDTH = 250;
const TRANSITION_DURATION = 200;

// Types
interface NavItem {
  label: string;
  icon: React.ElementType;
  to: string;
}

interface NavLinkItemProps {
  item: NavItem;
  collapsed: boolean;
  isActive: boolean;
  onClick?: () => void;
}

interface SidebarContentProps {
  children: React.ReactNode;
  theme: MantineTheme;
}

interface SidebarProps {
  collapsed: boolean;
  toggleSidebar: () => void;
  navItems: NavItem[];
  children?: React.ReactNode;
}

// Navigation items
const navItems: NavItem[] = [
  { 
    label: 'Home', 
    icon: IconHome,
    to: '/',
  },
  { 
    label: 'Dashboard', 
    icon: IconLayoutDashboard,
    to: '/dashboard',
  },
  { 
    label: 'Settings', 
    icon: IconSettings,
    to: '/settings'
  }
];

const NavLinkItem: React.FC<NavLinkItemProps> = ({ item, collapsed, isActive, onClick }) => {
  const { colorScheme } = useMantineColorScheme() as { colorScheme: 'light' | 'dark' };
  const theme = useMantineTheme();
  const Icon = item.icon;

  const linkContent = (
    <Box
      component={NavLink}
      to={item.to}
      style={{
        display: 'flex',
        alignItems: 'center',
        padding: '0.75rem 1rem',
        margin: '0.25rem 0.5rem',
        borderRadius: theme.radius.md,
        textDecoration: 'none',
        color: isActive 
          ? theme.colors.orange[6] 
          : colorScheme === 'dark' 
            ? theme.colors.gray[4] 
            : theme.colors.gray[7],
        backgroundColor: isActive 
          ? colorScheme === 'dark' 
            ? rgba(theme.colors.orange[6], 0.2)
            : rgba(theme.colors.orange[6], 0.1)
          : 'transparent',
        transition: 'all 0.2s ease-in-out',
      }}
      onMouseEnter={(e) => {
        if (isActive) {
          e.currentTarget.style.backgroundColor = colorScheme === 'dark'
            ? rgba(theme.colors.orange[6], 0.25)
            : rgba(theme.colors.orange[6], 0.15);
        } else {
          e.currentTarget.style.backgroundColor = colorScheme === 'dark'
            ? theme.colors.dark[6]
            : theme.colors.gray[1];
        }
        e.currentTarget.style.transform = 'translateX(2px)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = '';
        if (isActive) {
          e.currentTarget.style.backgroundColor = colorScheme === 'dark'
            ? rgba(theme.colors.orange[6], 0.2)
            : rgba(theme.colors.orange[6], 0.1);
        } else {
          e.currentTarget.style.backgroundColor = 'transparent';
        }
      }}
      onClick={onClick}
    >
      <Box 
        style={{
          minWidth: '24px',
          display: 'flex',
          justifyContent: 'center',
          marginRight: collapsed ? 0 : '0.75rem',
          transition: 'margin-right 0.2s ease-in-out',
        }}
      >
        <Icon size={20} />
      </Box>
      {!collapsed && (
        <Box 
          component="span"
          style={{
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            transition: 'opacity 0.15s ease-in-out',
          }}
        >
          {item.label}
        </Box>
      )}
    </Box>
  );

  if (collapsed) {
    return (
      <Tooltip label={item.label} position="right" withArrow>
        {linkContent}
      </Tooltip>
    );
  }

  return linkContent;
};



interface SidebarContentProps {
  children: React.ReactNode;
  theme: MantineTheme;
}

const SidebarContent: React.FC<SidebarContentProps> = ({ children, theme }) => (
  <Box
    style={{
      marginLeft: `var(--sidebar-width, ${EXPANDED_WIDTH}px)`,
      transition: `margin-left ${TRANSITION_DURATION}ms ease-in-out`,
      minHeight: 'calc(100vh - 64px)',
      padding: '1rem',
      '@media (max-width: 768px)': {
        marginLeft: 0,
        width: '100%'
      }
    }}
  >
    {children}
  </Box>
);

export const Sidebar: React.FC<SidebarProps> = ({ collapsed, toggleSidebar, navItems, children }) => {
  const [isMobile, setIsMobile] = useState(false);
  const location = useLocation();
  const theme = useMantineTheme();
  const { colorScheme } = useMantineColorScheme() as { colorScheme: 'light' | 'dark' };

  // Check if mobile view
  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (mobile && !collapsed) {
        toggleSidebar();
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [collapsed, toggleSidebar]);

  const isActive = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path);
  };

  // Set CSS custom property for sidebar width
  useEffect(() => {
    document.documentElement.style.setProperty(
      '--sidebar-width', 
      `${collapsed ? COLLAPSED_WIDTH : EXPANDED_WIDTH}px`
    );
  }, [collapsed]);

  return (
    <>
      {/* Sidebar */}
      <Box
        style={{
          position: 'fixed',
          top: '64px',
          left: 0,
          bottom: 0,
          width: `var(--sidebar-width, ${EXPANDED_WIDTH}px)`,
          backgroundColor: colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0],
          borderRight: `1px solid ${colorScheme === 'dark' ? theme.colors.dark[5] : theme.colors.gray[3]}`,
          padding: '1rem 0',
          zIndex: 100,
          overflow: 'hidden',
          transition: `width ${TRANSITION_DURATION}ms ease-in-out, transform ${TRANSITION_DURATION}ms ease-in-out`,
          boxShadow: '2px 0 10px rgba(0, 0, 0, 0.05)',
          display: 'flex',
          flexDirection: 'column',
          '@media (max-width: 768px)': {
            transform: collapsed ? 'translateX(-100%)' : 'translateX(0)',
            zIndex: 200,
            boxShadow: '4px 0 20px rgba(0, 0, 0, 0.1)',
          }
        }}
      >
        <Box
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '0.5rem',
          }}
        >
          {/* Navigation Items */}
          <Box>
            {navItems.map((item) => (
              <NavLinkItem
                key={item.to}
                item={item}
                collapsed={collapsed}
                isActive={isActive(item.to)}
                onClick={() => isMobile && toggleSidebar()}
              />
            ))}
          </Box>

          {/* Collapse Button */}
          <Box
            component="button"
            onClick={toggleSidebar}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '100%',
              padding: '0.75rem',
              marginTop: 'auto',
              backgroundColor: 'transparent',
              border: 'none',
              borderTop: `1px solid ${colorScheme === 'dark' ? theme.colors.dark[5] : theme.colors.gray[3]}`,
              color: colorScheme === 'dark' ? theme.colors.gray[5] : theme.colors.gray[6],
              cursor: 'pointer',
              transition: 'all 0.2s ease-in-out',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = colorScheme === 'dark' 
                ? theme.colors.dark[6] 
                : theme.colors.gray[1];
              e.currentTarget.style.color = colorScheme === 'dark' 
                ? theme.colors.gray[5] 
                : theme.colors.gray[6];
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'transparent';
              e.currentTarget.style.color = colorScheme === 'dark' 
                ? theme.colors.gray[5] 
                : theme.colors.gray[6];
            }}
          >
            {collapsed ? <IconLayoutSidebarLeftExpand size={20} /> : <IconLayoutSidebarLeftCollapse size={20} />}
          </Box>
        </Box>
      </Box>
      <SidebarContent theme={theme}>
        {children}
      </SidebarContent>
    </>
  );
};