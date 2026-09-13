package com.smarttask.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.smarttask.model.Tarea;

@Repository
public interface TareaRepository extends JpaRepository<Tarea, Long> {
}
