import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="max-w-3xl mx-auto text-center py-12 transition-colors">
      <h1 className="text-4xl font-extrabold text-slate-900 dark:text-white mb-6">
        Clasificador de Incidencias Inteligente
      </h1>

      <p className="text-lg text-gray-600 dark:text-slate-300 mb-8">
        Este proyecto de TFM utiliza una <strong>Red Neuronal Recurrente (RNN)</strong> para categorizar tickets de soporte en tiempo real y automatizar las respuestas mediante una arquitectura de microservicios.
      </p>

      <Link
        href="/reportar-incidencia"
        className="inline-block bg-blue-600 text-white px-8 py-3 rounded-full font-bold hover:bg-blue-700 transition-all shadow-lg shadow-blue-200 dark:shadow-none hover:scale-105 active:scale-95"
      >
        Empezar el análisis
      </Link>

      {/* Badge tecnológico opcional para el TFM */}
      <div className="mt-12 flex justify-center gap-4 text-xs font-mono text-gray-400 dark:text-slate-500">
        <span className="border border-gray-200 dark:border-slate-800 px-2 py-1 rounded hover:border-blue-500 dark:hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all cursor-default">Next.js 15</span>
        <span className="border border-gray-200 dark:border-slate-800 px-2 py-1 rounded hover:border-blue-500 dark:hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all cursor-default">Spring Boot</span>
        <span className="border border-gray-200 dark:border-slate-800 px-2 py-1 rounded hover:border-blue-500 dark:hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all cursor-default">FastAPI (RNN)</span>
      </div>
    </div>
  );
}