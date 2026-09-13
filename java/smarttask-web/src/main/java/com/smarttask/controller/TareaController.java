package com.smarttask.controller;

import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.smarttask.model.Tarea;
import com.smarttask.service.TareaService;

@Controller
@RequestMapping("/tareas")
public class TareaController {

	@Autowired
	private TareaService tareaService;

	@GetMapping
	public String listar(Model model) {
		model.addAttribute("tareas", tareaService.listarTodas());
		return "tareas/lista";
	}

	@GetMapping("/nuevo")
	public String nuevoFormulario(Model model) {
		model.addAttribute("modo", "crear");
		return "tareas/form";
	}

	@PostMapping("/guardar")
	public String guardar(@RequestParam String nombre, @RequestParam String prioridad, @RequestParam String tipo,
			RedirectAttributes redirectAttributes) {

		if (nombre == null || nombre.trim().isEmpty()) {
			redirectAttributes.addFlashAttribute("error", "El nombre de la tarea no puede estar vacío.");
			return "redirect:/tareas/nuevo";
		}

		if ("urgente".equalsIgnoreCase(tipo)) {
			tareaService.crearTareaUrgente(nombre, prioridad);
		} else {
			tareaService.crearTareaNormal(nombre, prioridad);
		}

		redirectAttributes.addFlashAttribute("success", "¡Tarea creada exitosamente!");
		return "redirect:/tareas";
	}

	@GetMapping("/editar/{id}")
	public String editarFormulario(@PathVariable Long id, Model model) {
		Optional<Tarea> tarea = tareaService.obtenerPorId(id);

		if (tarea.isPresent()) {
			model.addAttribute("modo", "editar");
			model.addAttribute("tarea", tarea.get());
			return "tareas/form";
		}

		return "redirect:/tareas";
	}

	@PostMapping("/actualizar/{id}")
	public String actualizar(@PathVariable Long id, @RequestParam String nombre, @RequestParam String prioridad,
			RedirectAttributes redirectAttributes) {

		if (nombre == null || nombre.trim().isEmpty()) {
			redirectAttributes.addFlashAttribute("error", "El nombre de la tarea no puede estar vacío.");
			return "redirect:/tareas/editar/" + id;
		}

		Tarea actualizada = tareaService.actualizar(id, nombre, prioridad, "");

		if (actualizada != null) {
			redirectAttributes.addFlashAttribute("success", "¡Tarea actualizada exitosamente!");
		} else {
			redirectAttributes.addFlashAttribute("error", "No se encontró la tarea especificada.");
		}

		return "redirect:/tareas";
	}

	@GetMapping("/completar/{id}")
	public String marcarCompletada(@PathVariable Long id, RedirectAttributes redirectAttributes) {
		if (tareaService.marcarComoCompletada(id)) {
			redirectAttributes.addFlashAttribute("success", "¡Tarea marcada como completada!");
		} else {
			redirectAttributes.addFlashAttribute("error", "No se encontró la tarea especificada.");
		}
		return "redirect:/tareas";
	}

	@GetMapping("/eliminar/{id}")
	public String eliminar(@PathVariable Long id, RedirectAttributes redirectAttributes) {
		if (tareaService.eliminar(id)) {
			redirectAttributes.addFlashAttribute("success", "¡Tarea eliminada correctamente!");
		} else {
			redirectAttributes.addFlashAttribute("error", "No se encontró la tarea especificada.");
		}
		return "redirect:/tareas";
	}

}