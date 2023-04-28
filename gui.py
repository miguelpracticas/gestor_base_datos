# Aplicación creada en período de prácticas 

import tkinter as tk
from database import anadir_residente_db, obtener_residentes, busqueda_residente_db, eliminar_residente, obtener_datos, actualizar_datos_db, cerrar_db, importar_excel_db, exportar_excel_db, borrar_todo_db
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
import locale

class Residente:
    def __init__(self, nombre, edad, fecha_inscripcion):
        self.nombre = nombre
        self.edad = edad
        self.fecha_inscripcion = fecha_inscripcion

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configurar ventana 
        self.geometry("600x400")
        self.title("Gestor de Residentes")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=6)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        #* Menú
        self.menu_bar = tk.Menu(self)

        self.menu_archivo = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.menu_archivo.add_command(label="Importar de archivo Excel", command=self.importar_excel)
        self.menu_archivo.add_command(label="Exportar a Excel", command=self.exportar_a_excel)
        self.menu_archivo.add_command(label="Salir", command=self.cerrar_ventana)
        self.menu_edicion = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edicion", menu=self.menu_edicion)
        self.menu_edicion.add_command(label="Borrar todo", command=self.borrar_todos_residentes)

        self.config(menu=self.menu_bar)

        # Frame búsqueda
        self.frame_busqueda = tk.Frame(self)
        self.frame_busqueda.rowconfigure(0, weight=1)
        self.frame_busqueda.columnconfigure(0, weight=2)
        self.frame_busqueda.columnconfigure(1, weight=1)
        self.frame_busqueda.grid(row=0, column=0, sticky="nsew")

        self.entry_busqueda = tk.Entry(self.frame_busqueda, font=("Arial Black", 10), bg="#1e90b0")
        self.entry_busqueda.grid(row=0, column=0, sticky="nsew")
        self.boton_busqueda = tk.Button(self.frame_busqueda,font=("Arial", 14), text="🔎", bg="#1e81b0", command=lambda: self.busqueda_residente(self.entry_busqueda.get()))
        self.boton_busqueda.grid(row=0, column=1, sticky="nsew")

        # Frame de los botones
        self.frame_botones = tk.Frame(self)
        self.frame_botones.rowconfigure(0, weight=1)
        self.frame_botones.columnconfigure(0, weight=1)
        self.frame_botones.columnconfigure(1, weight=1)
        self.frame_botones.columnconfigure(2, weight=1) 
        self.frame_botones.columnconfigure(3, weight=1) 
        self.frame_botones.grid(row=2, column=0, sticky="nsew")
        
        # Creación de la lista
        self.lista_residentes = tk.Listbox(font=("Arial", 15), bg="#7fbfd0", selectbackground="#3d7979", highlightthickness=0, selectmode="single", activestyle="none", selectforeground="black")
        self.lista_residentes.grid(row=1, column=0, sticky="nsew")

        # Añadir botones para la lista
        self.boton_ver_residente = tk.Button(self.frame_botones, bg="#1e81b0", text="Ver información", command=self.ver_informacion_residente)
        self.boton_ver_residente.grid(row=0, column=0, sticky="nsew")
        
        self.boton_nuevo_residente = tk.Button(self.frame_botones, bg="#1e81b0", text="Añadir residente", command=self.nuevo_residente)
        self.boton_nuevo_residente.grid(row=0, column=1, sticky="nsew")

        self.boton_eliminar_residente = tk.Button(self.frame_botones, bg="#1e81b0", text="Eliminar residente", command=self.eliminar_residente)
        self.boton_eliminar_residente.grid(row=0, column=2, sticky="nsew")

        self.boton_editar_residente = tk.Button(self.frame_botones, bg="#1e81b0", text="Editar residente", command=self.editar_residente)
        self.boton_editar_residente.grid(row=0, column=3, sticky="nsew")

    def ver_informacion_residente(self):
        try:
            residente_seleccionado = self.lista_residentes.get(self.lista_residentes.curselection())
            self.ventana_ver_info = tk.Toplevel()
            self.ventana_ver_info.geometry("400x300")
            self.ventana_ver_info.title(f"Información de {residente_seleccionado}")
            self.ventana_ver_info.rowconfigure(0, weight=1)
            self.ventana_ver_info.rowconfigure(1, weight=1)
            self.ventana_ver_info.rowconfigure(2, weight=1)
            self.ventana_ver_info.columnconfigure(0, weight=1)
            self.ventana_ver_info.columnconfigure(1, weight=1)

            tk.Label(self.ventana_ver_info, text="Nombre completo").grid(row=0, column=0)
            self.nombre_label = tk.Label(self.ventana_ver_info, text=residente_seleccionado, highlightthickness=1, highlightbackground="black")
            self.nombre_label.grid(row=0, column=1)

            tk.Label(self.ventana_ver_info, text="Edad").grid(row=1, column=0)
            self.edad_label = tk.Label(self.ventana_ver_info, text=obtener_datos(residente_seleccionado)[2], highlightthickness=1, highlightbackground="black")
            self.edad_label.grid(row=1, column=1)

            tk.Label(self.ventana_ver_info, text="Fecha de Inscripción").grid(row=2, column=0)
            self.fecha_label = tk.Label(self.ventana_ver_info, text=obtener_datos(residente_seleccionado)[3], highlightthickness=1, highlightbackground="black")
            self.fecha_label.grid(row=2, column=1)

        except tk.TclError:
            messagebox.showerror(title="Error", message="No has seleccionado ningún residente")

    def nuevo_residente(self):

        #* Configurar ventana
        self.ventana_nuevo_residente = tk.Toplevel()
        self.ventana_nuevo_residente.title("Añadir residente")
        self.ventana_nuevo_residente.rowconfigure(0, weight=1)
        self.ventana_nuevo_residente.rowconfigure(1, weight=1)
        self.ventana_nuevo_residente.columnconfigure(0, weight=1)
        
        #* Frame datos del nuevo residente
        self.frame_datos = tk.Frame(self.ventana_nuevo_residente)
        self.frame_datos.grid(row=0, column=0)
        
        # Configurar frame
        self.frame_datos.rowconfigure(0, weight=1)
        self.frame_datos.rowconfigure(1, weight=1)
        self.frame_datos.rowconfigure(2, weight=1)
        self.frame_datos.columnconfigure(0, weight=1)
        self.frame_datos.columnconfigure(1, weight=1)
        self.frame_datos.grid(row=0, column=0, sticky="nsew")
        
        # Campos para el frame de datos
        self.nombre_completo_label = tk.Label(self.frame_datos, text="Nombre completo")
        self.nombre_completo_label.grid(row=0, column=0)
        self.nombre_completo_entry = tk.Entry(self.frame_datos)      # Nombre
        self.nombre_completo_entry.grid(row=0, column=1, sticky="nsew")

        self.edad_label = tk.Label(self.frame_datos, text="Edad")
        self.edad_label.grid(row=1, column=0)
        self.edad_entry = tk.Spinbox(self.frame_datos, from_=18, to=150)        # Edad
        self.edad_entry.grid(row=1, column=1)
        
        # Creación del fecha_entry y cambiar el idioma a Español
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8') # Cambio de idioma
        self.fecha_entry = DateEntry(self.frame_datos, locale='es_ES', date_pattern="dd/MM/yyyy")
        self.fecha_label = tk.Label(self.frame_datos, text="Fecha de inscripción")
        self.fecha_label.grid(row=2, column=0)
        self.fecha_entry.grid(row=2, column=1)

        # Frame botón
        self.frame_boton_anadir = tk.Frame(self.ventana_nuevo_residente)
        self.frame_boton_anadir.rowconfigure(0, weight=1)
        self.frame_boton_anadir.columnconfigure(0, weight=1)
        self.frame_boton_anadir.grid(row=1, column=0, sticky="nsew")

        # Función para recoger los datos de los entries y agregarlos a la base de datos
        def confirmar_residente():
            global residente

            if len(self.nombre_completo_entry.get()) <= 3:
                messagebox.showerror(title="Error", message="Introduce todos los campos")
                self.ventana_nuevo_residente.deiconify()
            else:
                residente = Residente(nombre=self.nombre_completo_entry.get(), edad=self.edad_entry.get(), fecha_inscripcion=self.fecha_entry.get())     
                print(residente.fecha_inscripcion)
                anadir_residente_db(residente.nombre, residente.edad, residente.fecha_inscripcion)  
                self.ventana_nuevo_residente.destroy()
                self.actualizar_lista()
                messagebox.showinfo(title="Residente creado", message="Residente añadido con éxito")
            
        self.boton_anadir = tk.Button(self.frame_boton_anadir, text="Confirmar", command=confirmar_residente)
        self.boton_anadir.grid(row=0, column=0, sticky="nsew") 
        self.ventana_nuevo_residente.mainloop()

    def editar_residente(self):
        try:
            residente_seleccionado = self.lista_residentes.get(self.lista_residentes.curselection())
            self.ventana_editar = tk.Toplevel()
            self.ventana_editar.geometry("400x300")
            self.ventana_editar.title(f"Editando a {residente_seleccionado}")
            self.ventana_editar.rowconfigure(0, weight=4)
            self.ventana_editar.rowconfigure(1, weight=1)
            self.ventana_editar.columnconfigure(0, weight=1)

            self.info_frame = tk.Frame(self.ventana_editar)
            self.info_frame.grid(row=0, column=0, sticky="nsew")

            self.info_frame.rowconfigure(0, weight=1)
            self.info_frame.rowconfigure(1, weight=1)
            self.info_frame.rowconfigure(2, weight=1)
            self.info_frame.columnconfigure(0, weight=1)
            self.info_frame.columnconfigure(1, weight=1)

            tk.Label(self.info_frame, text="Nombre").grid(row=0, column=0)
            self.nuevo_nombre = tk.Entry(self.info_frame)
            self.nuevo_nombre.grid(row=0, column=1)

            tk.Label(self.info_frame, text="Edad").grid(row=1, column=0)
            self.nueva_edad = tk.Entry(self.info_frame)
            self.nueva_edad.grid(row=1, column=1)

            tk.Label(self.info_frame, text="Fecha de inscripción").grid(row=2, column=0)
            self.nueva_fecha = DateEntry(self.info_frame, locale="es_ES", date_pattern="dd/MM/yyyy")
            self.nueva_fecha.grid(row=2, column=1)

            self.boton_frame = tk.Frame(self.ventana_editar)
            self.boton_frame.grid(row=1, column=0, sticky="nsew")
            self.boton_frame.rowconfigure(0, weight=1)
            self.boton_frame.columnconfigure(0, weight=1)

            # Añadir los datos a los entries
            self.nuevo_nombre.insert(0, obtener_datos(residente_seleccionado)[1])
            self.nueva_edad.insert(0, obtener_datos(residente_seleccionado)[2])
            self.nueva_fecha.delete(0, tk.END)
            self.nueva_fecha.insert(0, obtener_datos(residente_seleccionado)[3])

            self.boton_guardar_cambios = tk.Button(self.boton_frame,
                                                    text="Guardar cambios",
                                                    command=lambda: self.actualizar_datos(self.nuevo_nombre.get(), self.nueva_edad.get(), self.nueva_fecha.get(), residente_seleccionado))
            self.boton_guardar_cambios.grid(row=0, column=0, sticky="nsew")

        except tk.TclError:
            messagebox.showerror(title="Error", message="Selecciona un residente")
            return 0;

    def eliminar_residente(self):
        try:
            seleccion = self.lista_residentes.curselection()
            residente_seleccionado = self.lista_residentes.get(seleccion)

            if messagebox.askyesno(title="Eliminar residente", message=f"¿Deseas eliminar al residente {residente_seleccionado} de la base de datos?"):
                eliminar_residente(nombre_completo=residente_seleccionado)
            else:
                pass

        except tk.TclError:
            messagebox.showerror(title="Error", message="Selecciona un residente")

        finally:
            self.actualizar_lista()

    def actualizar_lista(self):
        self.lista_residentes.delete(0, tk.END)
        for residente in obtener_residentes():
            self.lista_residentes.insert(tk.END, ' '.join(residente))

    def busqueda_residente(self, query):
        self.lista_residentes.delete(0, tk.END)
        for residente in busqueda_residente_db(query):
            self.lista_residentes.insert(tk.END, ' '.join(residente))

    def actualizar_datos(self, nombre_completo_nuevo, edad_nueva, fecha_nueva, nombre_completo_anterior):
        if messagebox.askyesno(title="Confirmación", message="¿Deseas cambiar los datos?"):
            actualizar_datos_db(nombre_completo_nuevo, edad_nueva, fecha_nueva, nombre_completo_anterior)
            self.ventana_editar.destroy()
            self.actualizar_lista()
        else:
            pass

    def importar_excel(self):
        ruta_archivo_excel = filedialog.askopenfilename()
        importar_excel_db(ruta_archivo=ruta_archivo_excel)
        self.actualizar_lista()
        messagebox.showinfo(title="Datos importados", message="Datos importados con éxito")

    def exportar_a_excel(self):
        ruta_archivo_excel = filedialog.askopenfilename()
        exportar_excel_db(ruta_archivo=ruta_archivo_excel)
    
    def cerrar_ventana(self):
        self.destroy()
        cerrar_db() 

    def borrar_todos_residentes(self):
        if messagebox.askokcancel(title="Borrar todos los datos", message="¿Deseas borrar todos los datos de la base de datos?"):
            borrar_todo_db()
            self.actualizar_lista()
        else:
            pass
        
if __name__ == '__main__':
    app = App()
    app.actualizar_lista()
    app.protocol("WM_DELETE_WINDOW", app.cerrar_ventana)
    app.mainloop()