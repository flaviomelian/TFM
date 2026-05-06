import TicketForm from '@/components/TicketForm';

export default function ReportarPage() {
  return (
    <div className="py-6">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white">Nueva Incidencia</h1>
        <p className="text-gray-500 dark:text-gray-400">Nuestro motor de IA procesará su mensaje al instante.</p>
      </div>
      <TicketForm />
    </div>
  );
}