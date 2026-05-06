'use client';

import { useTheme } from 'next-themes';
import { Sun, Moon } from 'lucide-react';
import { useEffect, useState } from 'react';

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  // Importante: Este useEffect evita errores de hidratación.
  // Next.js (SSR) no sabe qué tema tiene el usuario hasta que llega al cliente.
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    // Retornamos un placeholder del mismo tamaño para evitar saltos visuales
    return <div className="p-2 w-10 h-10" />;
  }

  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="p-2 rounded-lg bg-gray-100 dark:bg-slate-800 hover:bg-gray-200 dark:hover:bg-slate-700 transition-all duration-200 flex items-center justify-center group"
      aria-label="Cambiar modo de color"
    >
      {theme === 'dark' ? (
        <Sun className="text-yellow-400 group-hover:rotate-45 transition-transform" size={20} />
      ) : (
        <Moon className="text-slate-700" size={20} />
      )}
    </button>
  );
}