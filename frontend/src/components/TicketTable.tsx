'use client';
import { useState, useMemo } from 'react'; // Añadimos useMemo para rendimiento
import { CheckCircle, XCircle, Send, ArrowUpDown, ChevronUp, ChevronDown } from 'lucide-react';

const CATEGORIES_UNIFIED = [
  { id: 0, label: "Reembolso / Refund" },
  { id: 1, label: "Técnico / Technical" },
  { id: 2, label: "Cancelación / Cancellation" },
  { id: 3, label: "Consulta Producto / Inquiry" },
  { id: 4, label: "Facturación / Billing" }
];

export default function TicketTable({ tickets, loading }: { tickets: any[], loading: boolean }) {
  const [correctingId, setCorrectingId] = useState<number | null>(null);
  const [feedback, setFeedback] = useState("");
  
  // --- Lógica de Ordenación ---
  const [sortOrder, setSortOrder] = useState<'ASC' | 'DESC'>('ASC');

  const sortedTickets = useMemo(() => {
    // BLINDAJE: Si tickets no es un array, devolvemos array vacío
    if (!Array.isArray(tickets)) return [];

    const data = [...tickets]; 
    return data.sort((a, b) => {
      return sortOrder === 'ASC' ? a.id - b.id : b.id - a.id;
    });
  }, [tickets, sortOrder]);

  if (loading) return <div>Cargando tabla...</div>;

  const toggleSort = () => {
    setSortOrder(prev => prev === 'ASC' ? 'DESC' : 'ASC');
  };
  // ----------------------------

  const handleCorrect = (id: number) => {
    if (correctingId === id) {
      setCorrectingId(null);
      setFeedback("");
    } else {
      setCorrectingId(id);
    }
  };

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-xl overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead className="bg-slate-50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800">
            {/* Hacemos que la fila del encabezado sea interactiva */}
            <tr 
              onClick={toggleSort} 
              className="cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-700/50 transition-colors"
              title="Click para cambiar orden por ID"
            >
              <th className="px-6 py-4 text-xs font-bold uppercase text-slate-500 dark:text-slate-400 flex items-center gap-2">
                ID 
                {sortOrder === 'ASC' ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
              </th>
              <th className="px-6 py-4 text-xs font-bold uppercase text-slate-500 dark:text-slate-400">Incidencia</th>
              <th className="px-6 py-4 text-xs font-bold uppercase text-slate-500 dark:text-slate-400 text-center">IA Categoría</th>
              <th className="px-6 py-4 text-xs font-bold uppercase text-slate-500 dark:text-slate-400 text-center">Confianza</th>
              <th className="px-6 py-4 text-xs font-bold uppercase text-slate-500 dark:text-slate-400 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
            {/* Usamos sortedTickets en lugar de tickets directamente */}
            {sortedTickets.map((t) => (
              <tr
                key={t.id}
                className="hover:bg-slate-50/80 dark:hover:bg-slate-800/20 transition-all duration-500 ease-in-out group"
              >
                <td className="px-6 py-4 text-sm font-mono text-blue-600 dark:text-blue-400 align-top">#{t.id}</td>

                <td className="px-6 py-4">
                  <div className="flex flex-col gap-3">
                    <div className="relative overflow-hidden group-hover:max-h-[1000px] max-h-[1.5rem] transition-[max-height] duration-700 ease-in-out">
                      <p className="text-sm text-slate-700 dark:text-slate-300 absolute inset-0 truncate group-hover:opacity-0 transition-opacity duration-300 pointer-events-none">
                        {t.userText}
                      </p>
                      <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed opacity-0 group-hover:opacity-100 transition-opacity duration-500 delay-100">
                        {t.userText}
                        {t.aiResponse && (
                          <span className="block mt-2 text-xs text-slate-500 dark:text-slate-400">
                            Respuesta IA: <br/>{t.aiResponse}
                          </span>
                        )}
                      </p>
                    </div>

                    {correctingId === t.id && (
                      <div className="flex items-center gap-2 animate-in fade-in slide-in-from-top-1 duration-500 ease-in-out">
                        <div className="relative flex-grow">
                          <select
                            autoFocus
                            className="w-full text-xs p-2.5 rounded border border-red-200 dark:border-red-900/40 bg-red-50/50 dark:bg-red-950/10 text-slate-800 dark:text-slate-200 outline-none focus:ring-1 focus:ring-red-400 appearance-none cursor-pointer transition-colors duration-300"
                            value={feedback}
                            onChange={(e) => setFeedback(e.target.value)}
                          >
                            <option value="" disabled>Indique la categoría correcta...</option>
                            {CATEGORIES_UNIFIED.map((cat) => (
                              <option key={cat.id} value={cat.label} className="bg-white dark:bg-slate-900">
                                {cat.label}
                              </option>
                            ))}
                          </select>
                        </div>
                        <button
                          disabled={feedback === ""} // Deshabilitamos el botón si no hay feedback
                          className="p-2.5 bg-red-500 text-white rounded hover:bg-red-600 transition-all duration-300 disabled:opacity-30 disabled:cursor-not-allowed"
                          onClick={() => {
                            console.log(`Guardando corrección #${t.id}: ${feedback}`);
                            setCorrectingId(null);
                            setFeedback("");
                          }}
                        >
                          <Send size={14} />
                        </button>
                      </div>
                    )}
                  </div>
                </td>

                <td className="px-6 py-4 text-center align-top">
                  <span className="px-3 py-1 rounded-full text-xs font-bold bg-blue-100/80 text-blue-800 dark:bg-blue-900/20 dark:text-blue-300 border border-blue-200/50 dark:border-blue-800/50">
                    {t.predictedCategory}
                  </span>
                </td>

                <td className="px-6 py-4 text-center font-bold dark:text-white align-top">
                  {t.confidence}%
                </td>

                <td className="px-6 py-4 text-right align-top">
                  <div className="flex justify-end gap-2">
                    <button className="text-slate-400 hover:text-green-500 transition-colors duration-300 p-1">
                      <CheckCircle size={20} />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation(); // Evitamos que el click en el botón active el orden de la fila si estuviera en la cabecera
                        handleCorrect(t.id);
                      }}
                      className={`p-1 transition-all duration-300 ${correctingId === t.id ? 'text-red-500 rotate-90' : 'text-slate-400 hover:text-red-500'}`}
                    >
                      <XCircle size={20} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}