'use client';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Cell 
} from 'recharts';

export default function TicketStatsHistogram({ tickets = [] }: { tickets: any[] }) {
  // 1. BLINDAJE CRÍTICO: Evitar que el componente rompa el renderizado
  if (!Array.isArray(tickets) || tickets.length === 0) {
    return (
      <div className="bg-white dark:bg-slate-900 p-6 mb-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm w-full h-96 flex items-center justify-center">
        <p className="text-slate-500 animate-pulse">Esperando datos de tickets...</p>
      </div>
    );
  }

  // 2. Procesar los datos (Añadido manejo de nulos en predictedCategory)
  const distributionData = tickets.reduce((acc: any[], ticket) => {
    const category = ticket.predictedCategory || 'Sin Clasificar';
    const existing = acc.find(item => item.name === category);
    
    if (existing) {
      existing.cantidad++;
    } else {
      acc.push({ name: category, cantidad: 1 });
    }
    return acc;
  }, []).sort((a, b) => b.cantidad - a.cantidad);

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  return (
    <div className="bg-white dark:bg-slate-900 p-6 mb-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm w-full">
      <div className="mb-6">
        <h3 className="text-sm font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
          Histograma de Distribución de Clases
        </h3>
        <p className="text-xs text-slate-400 mt-1">Frecuencia absoluta de predicciones por categoría RNN</p>
      </div>

      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={distributionData}
            margin={{ top: 10, right: 30, left: 0, bottom: 40 }} // Aumentado bottom para etiquetas
          >
            <CartesianGrid 
              strokeDasharray="3 3" 
              vertical={false} 
              stroke="#e2e8f0" 
              className="dark:stroke-slate-800"
            />
            
            <XAxis 
              dataKey="name" 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#94a3b8', fontSize: 11 }}
              interval={0} // Obliga a mostrar todas las etiquetas
              angle={-20}  // Rotación para evitar solapamiento
              textAnchor="end"
            />
            
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              allowDecimals={false}
            />

            <Tooltip
              cursor={{ fill: '#f1f5f9', opacity: 0.1 }}
              contentStyle={{ 
                backgroundColor: '#1e293b', 
                border: 'none', 
                borderRadius: '8px', 
                color: '#fff',
                fontSize: '12px'
              }}
            />

            <Bar 
              dataKey="cantidad" 
              radius={[4, 4, 0, 0]} 
              barSize={40}
            >
              {distributionData.map((_, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={COLORS[index % COLORS.length]} 
                  fillOpacity={0.8}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-slate-100 dark:border-slate-800">
        {distributionData.slice(0, 4).map((item, i) => (
          <div key={i} className="flex flex-col">
            <span className="text-[10px] text-slate-400 uppercase font-medium truncate w-full">{item.name}</span>
            <span className="text-lg font-semibold text-slate-700 dark:text-slate-200">{item.cantidad}</span>
          </div>
        ))}
      </div>
    </div>
  );
}