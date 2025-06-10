import React, { useEffect, useState } from 'react';
import Header from '@/components/Header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  mfa_enabled: boolean;
  preferences: Record<string, unknown> | null;
}

const API_BASE = 'http://localhost:8000/api/accounts';

const Users = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [form, setForm] = useState({ username: '', password: '', email: '' });

  const loadUsers = async () => {
    try {
      const res = await fetch(`${API_BASE}/users/`);
      if (res.ok) {
        const data = await res.json();
        setUsers(data);
      }
    } catch {
      /* ignore errors for demo */
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE}/users/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (res.ok) {
        setForm({ username: '', password: '', email: '' });
        await loadUsers();
      }
    } catch {
      /* ignore errors for demo */
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-3xl mx-auto p-8 space-y-8">
        <Card>
          <CardHeader>
            <CardTitle>Create User</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                name="username"
                placeholder="Username"
                value={form.username}
                onChange={handleChange}
              />
              <Input
                name="password"
                type="password"
                placeholder="Password"
                value={form.password}
                onChange={handleChange}
              />
              <Input
                name="email"
                type="email"
                placeholder="Email"
                value={form.email}
                onChange={handleChange}
              />
              <Button type="submit">Add User</Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Existing Users</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {users.map((u) => (
                <li key={u.id} className="border-b pb-1 last:border-none">
                  {u.username} – {u.email}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Users;
