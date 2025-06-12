import React, { useEffect, useState } from 'react';
import Header from '@/components/Header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Trash2 } from 'lucide-react';
import { TENANTS_API } from '@/lib/api';

interface Tenant {
  id: number;
  name: string;
  schema_name: string;
  domain: string;
}

const Clients = () => {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [form, setForm] = useState({ name: '', schema_name: '', domain: '' });

  const loadTenants = async () => {
    const res = await fetch(`${TENANTS_API}/tenants/`, { credentials: 'include' });
    if (res.ok) {
      const data = await res.json();
      const domainsRes = await fetch(`${TENANTS_API}/domains/`, { credentials: 'include' });
      const domains = domainsRes.ok ? await domainsRes.json() : [];
      setTenants(
        data.map((t: any) => ({
          ...t,
          domain: domains.find((d: any) => d.tenant === t.id && d.is_primary)?.domain || '',
        }))
      );
    }
  };

  useEffect(() => {
    loadTenants();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch(`${TENANTS_API}/tenants/`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    if (res.ok) {
      setForm({ name: '', schema_name: '', domain: '' });
      loadTenants();
    } else {
      console.error('Tenant creation failed', await res.text());
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete tenant?')) return;
    const res = await fetch(`${TENANTS_API}/tenants/${id}/`, {
      method: 'DELETE',
      credentials: 'include',
    });
    if (res.ok) {
      loadTenants();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-3xl mx-auto p-8 space-y-8">
        <Card>
          <CardHeader>
            <CardTitle>Create Client</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input name="name" placeholder="Client Name" value={form.name} onChange={handleChange} />
              <Input name="schema_name" placeholder="Schema Name" value={form.schema_name} onChange={handleChange} />
              <Input name="domain" placeholder="Domain" value={form.domain} onChange={handleChange} />
              <Button type="submit">Add Client</Button>
            </form>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Existing Clients</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {tenants.map((t) => (
                <li key={t.id} className="border-b pb-1 last:border-none flex justify-between items-center">
                  <span>{t.name} – {t.domain}</span>
                  <button onClick={() => handleDelete(t.id)} className="text-red-600 hover:text-red-800">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Clients;
