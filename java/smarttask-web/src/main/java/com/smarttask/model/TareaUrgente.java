package com.smarttask.model;

import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;

@Entity
@DiscriminatorValue("URGENTE")
public class TareaUrgente extends Tarea {
	public TareaUrgente() {
	}

	public TareaUrgente(String nombre, String prioridad) {
		super(nombre, prioridad);
	}

	@Override
	public String obtenerDetalles() {
		return "[¡URGENTE!] ID: " + getId() + " | Tarea: " + getNombre() + " | Prioridad: " + getPrioridad()
				+ " | Estado: " + (isCompletada() ? "✓ Completada" : "⏳ Pendiente");
	}

	@Override
	public String getTipo() {
		return "URGENTE";
	}
}
