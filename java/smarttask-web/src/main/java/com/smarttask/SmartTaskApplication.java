package com.smarttask;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SmartTaskApplication {
	public static void main(String[] args) {
		SpringApplication.run(SmartTaskApplication.class, args);
		System.out.println("\n✓ SmartTask Web iniciada en http://localhost:8080/smarttask");
	}
}
