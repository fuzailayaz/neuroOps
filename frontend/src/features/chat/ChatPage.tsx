import { useState, useRef, useEffect } from 'react';
import { TextInput, Button, ScrollArea, Text } from '@mantine/core';

// Simple icons (replace with your preferred icon library)
const FiSend = () => <span>✉️</span>;
const FiUser = () => <span>👤</span>;
const FiBot = () => <span>🤖</span>;

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

export const ChatPage = () => {
  // User data is available via useAuthStore if needed
  // const { user } = useAuthStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `I'm your AI assistant. You said: "${input}"`,
        sender: 'ai',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    }, 1000);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Chat header */}
      <div className="border-b border-gray-200 dark:border-gray-700 p-4">
        <Text size="lg" fw={600} className="text-gray-900 dark:text-white">
          NeuroOps Chat
        </Text>
      </div>

      {/* Messages area */}
      <ScrollArea className="flex-1 p-4" scrollbarSize={8}>
        <div className="space-y-4">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
              <Text>Start a new conversation with the AI assistant</Text>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-3/4 rounded-lg p-4 ${
                    message.sender === 'user'
                      ? 'bg-primary-100 dark:bg-primary-900/30 rounded-tr-none'
                      : 'bg-gray-100 dark:bg-gray-800 rounded-tl-none'
                  }`}
                >
                  <div className="flex items-start space-x-2">
                    <div className="flex-shrink-0 mt-1">
                      {message.sender === 'user' ? <FiUser /> : <FiBot />}
                    </div>
                    <div>
                      <Text className="whitespace-pre-wrap">{message.content}</Text>
                      <Text size="xs" color="dimmed" className="mt-1">
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </Text>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      {/* Input area */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="flex space-x-2"
        >
          <TextInput
            placeholder="Type your message..."
            className="flex-1"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            autoFocus
          />
          <Button type="submit" variant="filled" color="primary">
            <FiSend />
          </Button>
        </form>
      </div>
    </div>
  );
};

export default ChatPage;
