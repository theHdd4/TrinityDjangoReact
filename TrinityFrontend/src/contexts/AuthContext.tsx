
import React, { createContext, useContext, useState, useEffect } from 'react';
import { ACCOUNTS_API } from '@/lib/api';

interface UserInfo {
  id: number;
  username: string;
  email: string;
  mfa_enabled: boolean;
  preferences: Record<string, unknown> | null;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: UserInfo | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_BASE = ACCOUNTS_API;

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<UserInfo | null>(null);

  useEffect(() => {
    const authState = localStorage.getItem('isAuthenticated');
    if (authState === 'true') {
      // check session
      fetch(`${API_BASE}/users/me/`, { credentials: 'include' })
        .then(async (res) => {
          if (res.ok) {
            const data = await res.json();
            setUser(data);
            setIsAuthenticated(true);
          } else {
            setIsAuthenticated(false);
          }
        })
        .catch(() => setIsAuthenticated(false));
    }
  }, []);

  const login = async (username: string, password: string) => {
    console.log('Attempting login for', username);
    try {
      const res = await fetch(`${API_BASE}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username, password }),
      });
      console.log('Login response status', res.status);
      if (res.ok) {
        const data = await res.json();
        console.log('Login success, user:', data.username);
        setUser(data);
        localStorage.setItem('isAuthenticated', 'true');
        setIsAuthenticated(true);
        return true;
      } else {
        const text = await res.text();
        console.log('Login failed:', text);
      }
    } catch (err) {
      console.log('Login request error', err);
    }
    return false;
  };

  const logout = async () => {
    await fetch(`${API_BASE}/logout/`, { method: 'POST', credentials: 'include' });
    localStorage.removeItem('isAuthenticated');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
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
