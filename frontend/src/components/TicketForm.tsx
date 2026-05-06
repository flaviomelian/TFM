'use client';
import { useState } from 'react';
import { ticketService } from '@/services/ticketService';

export default function TicketForm() {
    const [text, setText] = useState('');
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState<any>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const data = await ticketService.classify(text);
            setResponse(data);
        } catch (err) {
            alert("Error al conectar con Spring Boot.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="w-full max-w-xl mx-auto">
            <section className="w-full max-w-xl mx-auto">
                <form
                    onSubmit={handleSubmit}
                    className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-md border border-gray-100 dark:border-slate-800 transition-colors"
                >
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 italic">
                        <strong>Descripción de la incidencia:</strong>
                    </label>

                    <textarea
                        className="w-full p-4 border border-gray-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder:text-gray-400 dark:placeholder:text-slate-500"
                        rows={5}
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Ej: El clúster de Spark no responde..."
                        required
                    />

                    <button
                        type="submit"
                        disabled={loading}
                        className="mt-4 w-full bg-blue-600 text-white font-bold py-3 rounded-lg hover:bg-blue-700 disabled:bg-blue-300 transition-all shadow-lg shadow-blue-100 dark:shadow-none active:scale-[0.98]"
                    >
                        {loading ? (
                            <span className="flex items-center justify-center gap-2">
                                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Procesando con RNN...
                            </span>
                        ) : 'Analizar Incidencia'}
                    </button>
                </form>
            </section>

            {response && (
                <div className="mt-8 bg-white dark:bg-slate-900 border-l-4 border-green-500 p-6 rounded-lg shadow-sm dark:shadow-none animate-in fade-in slide-in-from-top-4 transition-colors">
                    <h2 className="text-green-800 dark:text-green-400 font-bold flex items-center gap-2">
                        ✅ Análisis Finalizado
                    </h2>

                    <div className="grid grid-cols-2 gap-4 mt-4 text-sm">
                        <div className="bg-gray-50 dark:bg-slate-800 p-3 rounded-lg border border-transparent dark:border-slate-700">
                            <span className="block text-gray-500 dark:text-gray-400 uppercase text-[10px] font-bold tracking-wider">
                                Categoría
                            </span>
                            <span className="font-bold text-slate-900 dark:text-white">
                                {response.predictedCategory}
                            </span>
                        </div>

                        <div className="bg-gray-50 dark:bg-slate-800 p-3 rounded-lg border border-transparent dark:border-slate-700">
                            <span className="block text-gray-500 dark:text-gray-400 uppercase text-[10px] font-bold tracking-wider">
                                Confianza
                            </span>
                            <span className="font-bold text-slate-900 dark:text-white">
                                {response.confidence}%
                            </span>
                        </div>
                    </div>

                    <p className="text-gray-600 dark:text-gray-300 mt-4 italic border-t border-gray-100 dark:border-slate-700 pt-4">
                        {response.aiResponse}
                    </p>
                </div>
            )}
        </section>
    );
}