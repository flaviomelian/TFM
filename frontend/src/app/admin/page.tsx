'use client';
import { useEffect, useState } from 'react';
import { ticketService } from '@/services/ticketService';
import { Database } from 'lucide-react';
import TicketStats from '@/components/TicketStatsWheel';
import TicketTable from '@/components/TicketTable';
import TicketStatsWheel from '@/components/TicketStatsWheel';
import TicketStatsHistogram from '@/components/TicketStatsHistogram';

export default function AdminPage() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    ticketService.getAll().then(setTickets).finally(() => setLoading(false));
    console.log("Tickets obtenidos para Admin:", tickets);
  }, []);

  return (
    <div className="max-w-6xl mx-auto animate-in fade-in duration-500">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Database className="text-blue-600" /> Admin Dashboard
          </h1>
          <p className="text-slate-500 dark:text-slate-400">Análisis de rendimiento de la Red Neuronal</p>
        </div>
      </header>

      <TicketStatsWheel tickets={tickets} />
      <TicketStatsHistogram tickets={tickets} />
      <TicketTable tickets={tickets} loading={loading} />
    </div>
  );
}