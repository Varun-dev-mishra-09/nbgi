import React from 'react';

export function PageShell({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-5xl rounded-xl bg-white p-6 shadow">
        <h1 className="mb-6 text-2xl font-semibold">{title}</h1>
        {children}
      </div>
    </main>
  );
}
