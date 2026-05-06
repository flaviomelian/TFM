package com.flavios.tfm.spring;
import org.springframework.boot.builder.SpringApplicationBuilder;

import java.util.HashMap;
import java.util.Map;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.web.reactive.function.client.WebClient;

import io.github.cdimascio.dotenv.Dotenv;

@SpringBootApplication
@EnableScheduling
public class Application {

    public static void main(String[] args) {
        Dotenv dotenv = Dotenv.configure()
        .directory("./") // Al estar en 'backend/spring', el .env está en el root actual
        .filename(".env") 
        .ignoreIfMissing()
        .load();

        // Creamos un mapa con las variables del .env
        Map<String, Object> envProps = new HashMap<>();
        dotenv.entries().forEach(e -> envProps.put(e.getKey(), e.getValue()));

        new SpringApplicationBuilder(Application.class)
                .properties(envProps) // Esto las mete en el Environment ANTES que la DB
                .run(args);
    }

    @Bean
    public WebClient.Builder webClientBuilder() {
        return WebClient.builder();
    }
}
