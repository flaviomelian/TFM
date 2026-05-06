'use client';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

export default function TicketStatsWheel({ tickets }: { tickets: any[] }) {
  // Procesar datos para categorías
  const categoryData = tickets.reduce((acc: any[], ticket) => {
    const existing = acc.find(item => item.name === ticket.predictedCategory);
    if (existing) existing.value++;
    else acc.push({ name: ticket.predictedCategory, value: 1 });
    return acc;
  }, []);

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      {/* Gráfico de Sectores - Categorías */}
      <div className="bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 className="text-sm font-bold text-slate-500 dark:text-slate-400 mb-4 uppercase tracking-wider">
          Distribución por categorías (RNN)
        </h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={categoryData}
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="none" />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff' }}
                itemStyle={{ color: '#fff' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Gráfico de Barras - Confianza Media */}
      <div className="bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 className="text-sm font-bold text-slate-500 dark:text-slate-400 mb-4 uppercase tracking-wider">
          Métricas de Rendimiento RNN
        </h3>
        <div className="flex items-center justify-center h-64">
           <div className="text-center">
              <span className="block text-5xl font-extrabold text-blue-600 dark:text-blue-400">
                {tickets.length > 0 
                  ? (tickets.reduce((a, b) => a + b.confidence, 0) / tickets.length).toFixed(1) 
                  : 0}%
              </span>
              <span className="text-slate-500 text-sm italic">Confianza Media del Modelo</span>
           </div>
        </div>
      </div>

      
    </div>
  );
}