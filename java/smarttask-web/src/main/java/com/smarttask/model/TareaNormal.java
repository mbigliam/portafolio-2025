package com.smarttask.model;

import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;

@Entity
@DiscriminatorValue("NORMAL")
public class TareaNormal extends Tarea {
	public TareaNormal() {
	}

	public TareaNormal(String nombre, String prioridad) {
		super(nombre, prioridad);
	}

	@Override
	public String obtenerDetalles() {
		return "ID: " + getId() + " | Tarea: " + getNombre() + " | Prioridad: " + getPrioridad()
				+ " | Estado: " + (isCompletada() ? "✓ Completada" : "⏳ Pendiente");
	}

	@Override
	public String getTipo() {
		return "NORMAL";
	}
}
