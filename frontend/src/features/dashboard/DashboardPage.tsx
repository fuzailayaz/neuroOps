import { Card, Title, Text, Grid, Badge, Progress } from '@mantine/core';
import { useAuthStore } from '@/stores/auth';

// Icons with proper size handling
const FiActivity = ({ size = 24 }: { size?: number }) => (
  <span className="text-2xl">📊</span>
);
const FiDatabase = ({ size = 24 }: { size?: number }) => (
  <span className="text-2xl">💾</span>
);
const FiUsers = ({ size = 24 }: { size?: number }) => (
  <span className="text-2xl">👥</span>
);
const FiClock = ({ size = 24 }: { size?: number }) => (
  <span className="text-2xl">⏱️</span>
);

export const DashboardPage = () => {
  const { user } = useAuthStore();
  
  // Type assertion for user since we know the shape from auth store
  type UserWithName = { username?: string; email?: string; first_name?: string; };

  // Mock data - replace with real data from your API
  const stats = [
    { title: 'Active Agents', value: '3', icon: <FiActivity size={24} />, color: 'blue' },
    { title: 'Documents Processed', value: '1.2K', icon: <FiDatabase size={24} />, color: 'green' },
    { title: 'Total Queries', value: '5.7K', icon: <FiUsers size={24} />, color: 'violet' },
    { title: 'Avg. Response Time', value: '1.4s', icon: <FiClock size={24} />, color: 'orange' },
  ];

  // Mock recent activity
  const recentActivity = [
    { id: 1, action: 'Document uploaded', time: '2 minutes ago', type: 'upload' },
    { id: 2, action: 'New chat started', time: '15 minutes ago', type: 'chat' },
    { id: 3, action: 'Agent response generated', time: '1 hour ago', type: 'agent' },
    { id: 4, action: 'System update completed', time: '2 hours ago', type: 'system' },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Welcome back, {(user as UserWithName)?.first_name || (user as UserWithName)?.username || 'User'}!
        </h1>
        <p className="mt-1 text-gray-600 dark:text-gray-400">
          Here's what's happening with your NeuroOps platform today.
        </p>
      </div>

      {/* Stats Grid */}
      <Grid>
        {stats.map((stat) => (
          <Grid.Col key={stat.title} span={{ base: 12, sm: 6, lg: 3 }}>
            <Card className="h-full bg-white dark:bg-gray-800 rounded-xl shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <Text className="text-sm font-medium text-gray-500 dark:text-gray-400">
                    {stat.title}
                  </Text>
                  <Title order={3} className="mt-1 text-2xl font-bold">
                    {stat.value}
                  </Title>
                </div>
                <div className={`p-3 rounded-full bg-${stat.color}-100 dark:bg-${stat.color}-900/30 text-${stat.color}-600`}>
                  {stat.icon}
                </div>
              </div>
            </Card>
          </Grid.Col>
        ))}
      </Grid>

      {/* Main Content */}
      <Grid gutter="md">
        {/* Recent Activity */}
        <Grid.Col span={{ base: 12, lg: 8 }}>
          <Card className="h-full bg-white dark:bg-gray-800 rounded-xl shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <Title order={3} className="text-lg font-semibold">
                Recent Activity
              </Title>
              <button className="text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
                View All
              </button>
            </div>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-start pb-4 border-b border-gray-100 dark:border-gray-700 last:border-0 last:pb-0">
                  <div className="flex-shrink-0 mt-1">
                    <div className="w-2 h-2 rounded-full bg-primary-500"></div>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {activity.action}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {activity.time}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </Grid.Col>

        {/* System Status */}
        <Grid.Col span={{ base: 12, lg: 4 }}>
          <Card className="h-full bg-white dark:bg-gray-800 rounded-xl shadow-sm">
            <Title order={3} className="text-lg font-semibold mb-6">
              System Status
            </Title>
            
            <div className="space-y-6">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium text-gray-700 dark:text-gray-300">CPU Usage</span>
                  <span className="text-gray-500">42%</span>
                </div>
                <Progress value={42} color="blue" size="sm" className="h-2" />
              </div>
              
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium text-gray-700 dark:text-gray-300">Memory</span>
                  <span className="text-gray-500">65%</span>
                </div>
                <Progress value={65} color="green" size="sm" className="h-2" />
              </div>
              
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium text-gray-700 dark:text-gray-300">Storage</span>
                  <span className="text-gray-500">28%</span>
                </div>
                <Progress value={28} color="violet" size="sm" className="h-2" />
              </div>
              
              <div className="pt-4 border-t border-gray-100 dark:border-gray-700">
                <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  System Version: v1.0.0
                </div>
                <Badge color="green" variant="outline" className="text-xs">
                  All systems operational
                </Badge>
              </div>
            </div>
          </Card>
        </Grid.Col>
      </Grid>
    </div>
  );
};
