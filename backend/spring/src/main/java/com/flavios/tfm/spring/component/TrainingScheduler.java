package com.flavios.tfm.spring.component;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.File;

@Component
public class TrainingScheduler {

    // Ruta absoluta a tu script y al entorno de python
    private final String SCRIPT_PATH = "C:\\Users\\Flavios\\Desktop\\IA\\TFM\\backend\\fastapi\\entrenar_categorias.py";
    private final String WORKING_DIR = "C:\\Users\\Flavios\\Desktop\\IA\\TFM\\backend\\fastapi\\";
    private final String PYTHON_EXE = "C:\\Users\\Flavios\\Desktop\\IA\\TFM\\backend\\fastapi\\venv\\Scripts\\python.exe"; // O la ruta a tu venv: "C:/.../venv/Scripts/python.exe"

    @Scheduled(cron = "0 15 20 * * MON") // Ejecución: Lunes a las 00:00
    public void triggerRetraining() {
        System.out.println("🚀 Iniciando proceso semanal de reentrenamiento de la Red Neuronal...");

        try {
            // Configuración del proceso
            ProcessBuilder pb = new ProcessBuilder(PYTHON_EXE, SCRIPT_PATH);
            pb.directory(new File(WORKING_DIR));
            pb.redirectErrorStream(true); // Redirige errores a la salida estándar

            Process process = pb.start();

            // Leemos la salida del script para logs de Spring
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null)
                System.out.println("[Python Training]: " + line);
            

            int exitCode = process.waitFor();
            if (exitCode == 0) System.out.println("✅ Reentrenamiento finalizado con éxito.");
            else System.err.println("❌ El script de entrenamiento falló con código: " + exitCode);
            

        } catch (Exception e) {
            System.err.println("❌ Error crítico al ejecutar el entrenamiento: " + e.getMessage());
            e.printStackTrace();
        }
    }
}