package com.smarttask.service;

import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.smarttask.model.Tarea;
import com.smarttask.model.TareaNormal;
import com.smarttask.model.TareaUrgente;
import com.smarttask.repository.TareaRepository;

@Service
public class TareaService {
	@Autowired
	private TareaRepository tareaRepository;

	public List<Tarea> listarTodas() {
		return tareaRepository.findAll();
	}

	public Optional<Tarea> obtenerPorId(Long id) {
		return tareaRepository.findById(id);
	}

	public Tarea crearTareaNormal(String nombre, String prioridad) {
		Tarea tarea = new TareaNormal(nombre, prioridad);
		return tareaRepository.save(tarea);
	}

	public Tarea crearTareaUrgente(String nombre, String prioridad) {
		Tarea tarea = new TareaUrgente(nombre, prioridad);
		return tareaRepository.save(tarea);
	}

	public Tarea actualizar(Long id, String nombre, String prioridad, String tipo) {
		Optional<Tarea> tareaOpt = tareaRepository.findById(id);
		if (tareaOpt.isPresent()) {
			Tarea tarea = tareaOpt.get();
			tarea.setNombre(nombre);
			tarea.setPrioridad(prioridad);
			return tareaRepository.save(tarea);
		}
		return null;
	}

	public boolean marcarComoCompletada(Long id) {
		Optional<Tarea> tareaOpt = tareaRepository.findById(id);
		if (tareaOpt.isPresent()) {
			Tarea tarea = tareaOpt.get();
			tarea.marcarComoCompletada();
			tareaRepository.save(tarea);
			return true;
		}
		return false;
	}

	public boolean eliminar(Long id) {
		if (tareaRepository.existsById(id)) {
			tareaRepository.deleteById(id);
			return true;
		}
		return false;
	}
}
