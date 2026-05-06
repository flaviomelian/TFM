import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import './globals.css';
import Link from 'next/link';
import { ThemeProvider } from '@/components/ThemeProvider';
import ThemeToggle from '@/components/ThemeToggle';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: 'IA Support System - TFM',
  description: 'Sistema de clasificación de incidencias con RNN',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased flex flex-col min-h-screen bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-300`}>
        <ThemeProvider>
          {/* HEADER / NAVBAR */}
          <header className="bg-gray-200 dark:bg-slate-900 border-b border-gray-200 dark:border-slate-800 shadow-sm transition-colors">
            <nav className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
              <div className="font-bold text-xl text-blue-600 dark:text-blue-400 font-mono tracking-tighter">
                IA-TFM
              </div>
              
              <div className="flex items-center space-x-6">
                <div className="space-x-6 hidden md:block">
                  <Link href="/" className="hover:text-blue-600 dark:hover:text-blue-400 transition">Inicio</Link>
                  <Link href="/reportar-incidencia" className="hover:text-blue-600 dark:hover:text-blue-400 transition">Reportar</Link>
                  <Link href="/admin" className="hover:text-orange-600 transition font-semibold text-orange-600 dark:text-orange-500">Admin</Link>
                </div>
                
                {/* EL BOTONCITO */}
                <div className="pl-4 border-l border-gray-200 dark:border-slate-700">
                  <ThemeToggle />
                </div>
              </div>
            </nav>
          </header>

          {/* CONTENIDO PRINCIPAL */}
          <main className="flex-grow container mx-auto px-4 py-8">
            {children}
          </main>

          {/* FOOTER */}
          <footer className="bg-gray-200 dark:bg-slate-900 border-t border-gray-200 dark:border-slate-800 py-6 transition-colors">
            <div className="max-w-6xl mx-auto px-4 text-center text-gray-500 dark:text-gray-400 text-sm">
              © {new Date().getFullYear()} - Sistema de Gestión IA - Desarrollado por 
              <span className="font-semibold text-blue-600 dark:text-blue-400 ml-1">@flaviomelian</span>
            </div>
          </footer>
        </ThemeProvider>
      </body>
    </html>
  );
}