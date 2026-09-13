package com.smarttask.model;

import jakarta.persistence.*;

@Entity
@Table(name = "tareas")
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "tipo_tarea", discriminatorType = DiscriminatorType.STRING)
public abstract class Tarea {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	@Column(nullable = false, length = 255)
	private String nombre;
	@Column(nullable = false)
	private String prioridad;
	@Column(nullable = false)
	private boolean completada;

	public Tarea() {
	}

	public Tarea(String nombre, String prioridad) {
		this.nombre = nombre;
		this.prioridad = prioridad;
		this.completada = false;
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getNombre() {
		return nombre;
	}

	public void setNombre(String nombre) {
		this.nombre = nombre;
	}

	public String getPrioridad() {
		return prioridad;
	}

	public void setPrioridad(String prioridad) {
		this.prioridad = prioridad;
	}

	public boolean isCompletada() {
		return completada;
	}

	public void setCompletada(boolean completada) {
		this.completada = completada;
	}

	public void marcarComoCompletada() {
		this.completada = true;
	}

	public abstract String obtenerDetalles();
	public abstract String getTipo();
}
