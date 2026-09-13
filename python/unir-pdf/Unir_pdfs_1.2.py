import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image
import img2pdf
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import subprocess
import os
import tempfile
import shutil
from pathlib import Path

class FileMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unificador de Archivos (PDFs e Imágenes)")
        self.root.geometry("700x500")
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Archivos a Unir", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Frame para la lista y scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Lista de archivos con scrollbar
        self.listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, width=80, height=15)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar drag and drop personalizado
        self.setup_drag_and_drop()
        
        # Frame para botones de control
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Botones para manipular archivos
        self.add_btn = ttk.Button(control_frame, text="Agregar Archivos", command=self.add_files)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.remove_btn = ttk.Button(control_frame, text="Quitar Seleccionado", command=self.remove_file)
        self.remove_btn.pack(side=tk.LEFT, padx=5)
        
        self.move_up_btn = ttk.Button(control_frame, text="↑ Subir", command=self.move_up)
        self.move_up_btn.pack(side=tk.LEFT, padx=5)
        
        self.move_down_btn = ttk.Button(control_frame, text="↓ Bajar", command=self.move_down)
        self.move_down_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame para botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        self.merge_btn = ttk.Button(action_frame, text="Unir Archivos", command=self.merge_files)
        self.merge_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(action_frame, text="Limpiar Lista", command=self.clear_list)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Lista de rutas de archivos
        self.files = []
        
        # Variables para drag and drop
        self.drag_data = {"index": None, "item": None}

    def setup_drag_and_drop(self):
        """Configura el drag and drop para reordenar elementos"""
        self.listbox.bind('<Button-1>', self.on_start_drag)
        self.listbox.bind('<B1-Motion>', self.on_drag)
        self.listbox.bind('<ButtonRelease-1>', self.on_drop)
        self.listbox.bind('<Leave>', self.on_drag_leave)
        self.listbox.bind('<Enter>', self.on_drag_enter)

    def on_start_drag(self, event):
        """Inicia el arrastre de un elemento"""
        index = self.listbox.nearest(event.y)
        if index < len(self.files):
            self.drag_data["index"] = index
            self.drag_data["item"] = self.files[index]

    def on_drag(self, event):
        """Durante el arrastre"""
        # Puedes añadir efectos visuales aquí si lo deseas
        pass

    def on_drop(self, event):
        """Cuando se suelta el elemento arrastrado"""
        if self.drag_data["index"] is not None:
            end_index = self.listbox.nearest(event.y)
            if 0 <= end_index < len(self.files) and self.drag_data["index"] != end_index:
                # Reordenar los archivos
                file = self.files.pop(self.drag_data["index"])
                self.files.insert(end_index, file)
                self.update_listbox()
                self.listbox.selection_set(end_index)
        self.drag_data = {"index": None, "item": None}

    def on_drag_leave(self, event):
        """Cuando el cursor sale del listbox durante el arrastre"""
        self.drag_data = {"index": None, "item": None}

    def on_drag_enter(self, event):
        """Cuando el cursor entra al listbox durante el arrastre"""
        pass

    def add_files(self):
        """Permite al usuario seleccionar archivos (PDFs e imágenes)"""
        file_types = [
            ("Todos los archivos compatibles", "*.pdf *.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("Archivos PDF", "*.pdf"),
            ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif")
        ]
        
        files = filedialog.askopenfilenames(title="Selecciona archivos", filetypes=file_types)
        if files:
            self.files.extend(files)
            self.update_listbox()

    def remove_file(self):
        """Elimina el archivo seleccionado de la lista"""
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.files.pop(index)
            self.update_listbox()

    def move_up(self):
        """Mueve un archivo seleccionado arriba en la lista"""
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] > 0:
            index = selected_index[0]
            self.files[index], self.files[index - 1] = self.files[index - 1], self.files[index]
            self.update_listbox()
            self.listbox.selection_set(index - 1)

    def move_down(self):
        """Mueve un archivo seleccionado abajo en la lista"""
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] < len(self.files) - 1:
            index = selected_index[0]
            self.files[index], self.files[index + 1] = self.files[index + 1], self.files[index]
            self.update_listbox()
            self.listbox.selection_set(index + 1)

    def clear_list(self):
        """Limpia toda la lista de archivos"""
        self.files = []
        self.update_listbox()

    def update_listbox(self):
        """Actualiza la lista de archivos en la interfaz"""
        self.listbox.delete(0, tk.END)
        for file_path in self.files:
            file_name = os.path.basename(file_path)
            self.listbox.insert(tk.END, file_name)

    def merge_files(self):
        """Une los archivos en el orden seleccionado"""
        if not self.files:
            messagebox.showerror("Error", "No hay archivos seleccionados.")
            return

        # Preguntar dónde guardar
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            filetypes=[("Archivos PDF", "*.pdf")], 
            title="Guardar PDF unificado"
        )
        if not output_path:
            return

        # Crear un directorio temporal para archivos intermedios
        temp_dir = tempfile.mkdtemp()
        try:
            # Convertir todos los archivos a PDF si es necesario
            pdf_files_to_merge = []
            
            for i, file_path in enumerate(self.files):
                file_ext = os.path.splitext(file_path)[1].lower()
                temp_pdf_path = os.path.join(temp_dir, f"temp_{i}.pdf")
                
                if file_ext == '.pdf':
                    # Si es PDF, usarlo directamente
                    pdf_files_to_merge.append(file_path)
                else:
                    # Si es imagen, convertir a PDF
                    try:
                        self.convert_image_to_pdf(file_path, temp_pdf_path)
                        pdf_files_to_merge.append(temp_pdf_path)
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo procesar {file_path}:\n{str(e)}")
                        return

            # Preguntar sobre compresión
            compress = messagebox.askyesno("Compresión", "¿Desea comprimir el PDF resultante?")
            
            if compress:
                # Mostrar opciones de compresión
                compression_level = self.ask_compression_level()
                if compression_level is None:
                    return  # Usuario canceló
                
                # Unir y comprimir
                self.merge_and_compress_pdfs(pdf_files_to_merge, output_path, compression_level)
            else:
                # Unir sin comprimir
                merger = PdfMerger()
                for pdf in pdf_files_to_merge:
                    merger.append(pdf)
                merger.write(output_path)
                merger.close()
                
            messagebox.showinfo("Éxito", f"Archivos unidos guardados en:\n{output_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al unir los archivos:\n{str(e)}")
        finally:
            # Limpiar directorio temporal
            shutil.rmtree(temp_dir, ignore_errors=True)

    def convert_image_to_pdf(self, image_path, output_pdf_path):
        """Convierte una imagen a PDF"""
        try:
            with Image.open(image_path) as img:
                # Convertir a RGB si es necesario (para formatos como PNG)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Guardar como PDF
                img.save(output_pdf_path, "PDF", resolution=100.0)
        except Exception as e:
            raise Exception(f"Error al convertir imagen a PDF: {str(e)}")

    def ask_compression_level(self):
        """Muestra un diálogo para seleccionar el nivel de compresión"""
        # Crear ventana de diálogo personalizada
        dialog = tk.Toplevel(self.root)
        dialog.title("Nivel de Compresión")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Seleccione el nivel de compresión:").pack(pady=10)
        
        # Variable para almacenar la selección
        compression_var = tk.StringVar(value="medium")
        
        # Opciones de compresión
        options = [
            ("Alta compresión (calidad baja)", "high"),
            ("Compresión media (calidad aceptable)", "medium"),
            ("Baja compresión (calidad alta)", "low"),
            ("Solo optimizar (sin pérdida)", "optimize")
        ]
        
        for text, value in options:
            ttk.Radiobutton(dialog, text=text, variable=compression_var, value=value).pack(anchor=tk.W, padx=20)
        
        # Botones
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        result = None
        
        def on_ok():
            nonlocal result
            result = compression_var.get()
            dialog.destroy()
        
        def on_cancel():
            nonlocal result
            result = None
            dialog.destroy()
        
        ttk.Button(btn_frame, text="Aceptar", command=on_ok).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=on_cancel).pack(side=tk.LEFT, padx=10)
        
        dialog.wait_window(dialog)
        return result

    def merge_and_compress_pdfs(self, pdf_files, output_path, compression_level):
        """Une y comprime PDFs según el nivel seleccionado"""
        # Mapeo de niveles de compresión a configuraciones de Ghostscript
        gs_settings = {
            "high": "/screen",     # Máxima compresión, calidad baja
            "medium": "/ebook",    # Compresión media, calidad aceptable
            "low": "/printer",     # Compresión baja, calidad alta
            "optimize": "/default" # Solo optimización, sin pérdida de calidad
        }
        
        # Primero unir todos los PDFs en un archivo temporal
        temp_merged = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_merged.close()
        
        try:
            merger = PdfMerger()
            for pdf in pdf_files:
                merger.append(pdf)
            merger.write(temp_merged.name)
            merger.close()
            
            # Comprimir con Ghostscript si está disponible
            if self.has_ghostscript():
                gs_command = [
                    "gs",
                    "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.4",
                    f"-dPDFSETTINGS={gs_settings[compression_level]}",
                    "-dNOPAUSE",
                    "-dQUIET",
                    "-dBATCH",
                    f"-sOutputFile={output_path}",
                    temp_merged.name
                ]
                
                try:
                    subprocess.run(gs_command, check=True, capture_output=True)
                except subprocess.CalledProcessError as e:
                    # Si falla Ghostscript, usar método alternativo
                    self.alternative_compression(temp_merged.name, output_path, compression_level)
            else:
                # Ghostscript no disponible, usar método alternativo
                self.alternative_compression(temp_merged.name, output_path, compression_level)
                
        finally:
            # Eliminar archivo temporal
            os.unlink(temp_merged.name)

    def has_ghostscript(self):
        """Verifica si Ghostscript está disponible en el sistema"""
        try:
            subprocess.run(["gs", "--version"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def alternative_compression(self, input_pdf, output_pdf, compression_level):
        """
        Método alternativo de compresión usando PyPDF2 cuando Ghostscript no está disponible
        """
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        
        # Ajustar nivel de compresión según la selección
        if compression_level == "high":
            # Compresión máxima (puede reducir calidad)
            for page in reader.pages:
                page.compress_content_streams()  # Compresión máxima
                writer.add_page(page)
        elif compression_level == "medium":
            # Compresión media
            for page in reader.pages:
                writer.add_page(page)
        elif compression_level == "low":
            # Compresión mínima (máxima calidad)
            for page in reader.pages:
                writer.add_page(page)
        else:  # optimize
            # Solo optimizar estructura
            for page in reader.pages:
                writer.add_page(page)
        
        # Guardar el PDF resultante
        with open(output_pdf, "wb") as f:
            writer.write(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMergerApp(root)
    root.mainloop()