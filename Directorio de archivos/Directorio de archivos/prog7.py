import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import shutil

# Función para construir el árbol de archivos y carpetas recursivamente
def build_tree(dir_path, parent): #identificador del elemento padre del arbol 
    """
    Construye el árbol de archivos y carpetas de manera recursiva.

    Args:
        dir_path (str): Ruta del directorio a explorar.
        parent (str): Identificador del elemento padre en el árbol.
    """
    for path in os.scandir(dir_path): #itera sobre todos los elementos
        if path.is_file(): #verifica si es archivo
            tree.insert(parent, "end", text=path.name, values=(path.path,), tags=("file",)) #inserta un nuevo elemento en el arbol 
        elif path.is_dir(): #identifica si es un directorio 
            folder = tree.insert(parent, "end", text=path.name, values=(path.path,), tags=("folder",))
            build_tree(path.path, folder) # se llama recursivamente

# Función para realizar la búsqueda de archivos y carpetas
def search_items():
    """
    Realiza la búsqueda de archivos y carpetas en el sistema de archivos.

    Obtiene el término de búsqueda ingresado por el usuario y construye el árbol
    mostrando solo los elementos que coinciden con el término.
    """
    search_term = search_entry.get() # obtiene el termino de busqueda
    tree.delete(*tree.get_children()) #borra todo los elementos del arbol
    build_tree(r'C:\Users\miche\OneDrive\Documentos\Escritorio\Universidad\estructura de datos\Proyectos', "") # recontruye el arbol inical
    search_tree_items(tree, "", search_term) # Realiza la búsqueda y muestra solo los elementos que coinciden con el término de búsqueda

def search_tree_items (tree, parent, search_term): #busqueda general 
     # si en la anterior funcion se encuentran varias carpetas viene a esta para mostrar lo demas 

     for child in tree.get_children(parent):
        item_text = tree.item(child, "text")
        if search_term.lower() in item_text.lower():
            tree.item(child, open=True)
            search_tree_items(tree, child, search_term)
        else:
            tree.detach(child)

# Función para crear una nueva carpeta o archivo
def create_item():
    """
    Crea una nueva carpeta o archivo en la ruta actual del árbol.
    """
    selected_item = tree.focus() #obtiene el elemento seleccionado
    item_tags = tree.item(selected_item)["tags"] #obtiene las etiquetas del elemento seleccionado   
    if "folder" in item_tags: #verifica si es carpeta 
        current_path = tree.item(selected_item)["values"][0] #ruta
        new_item_name = tk.simpledialog.askstring("Crear", "Ingrese el nombre del nuevo elemento:")
        if new_item_name: #verificaciuon de nombre 
            new_item_path = os.path.join(current_path, new_item_name) #crea la ruta del nuevo elemento
            if new_item_name.endswith("/"):
                os.makedirs(new_item_path) #crea carpeta
                tree.insert(selected_item, "end", text=new_item_name, values=(new_item_path,), tags=("folder",))
                print(f"Carpeta creada: {new_item_name}")
            else:
                with open(new_item_path + ".txt", "w") as file: #crea archivo vacio
                    file.write("")  # Escribe contenido vacío para crear el archivo
                tree.insert(selected_item, "end", text=new_item_name, values=(new_item_path + ".txt",), tags=("file",))
                print(f"Archivo creado: {new_item_name}.txt")
    elif "file" in item_tags: #verifica si es archivo
        current_path = os.path.dirname(tree.item(selected_item)["values"][0]) #obtiene la ruta del directorio del archivo
        new_item_name = tk.simpledialog.askstring("Crear", "Ingrese el nombre del nuevo elemento:")
        if new_item_name: #verifica el nombre
            new_item_path = os.path.join(current_path, new_item_name)
            with open(new_item_path + ".txt", "w") as file:
                file.write("")  # Escribe contenido vacío para crear el archivo
            tree.insert(selected_item, "end", text=new_item_name, values=(new_item_path + ".txt",), tags=("file",))
            print(f"Archivo creado: {new_item_name}.txt")

#-------------------------------------------------------------------------------------------------------------
# Función para eliminar un archivo o carpeta
def delete_item():
    """
    Elimina el archivo o carpeta seleccionado del árbol.
    """
    selected_item = tree.focus()# Obtiene el elemento actualmente seleccionado en el árbol.
    item_tags = tree.item(selected_item)["tags"]  # Obtiene las etiquetas (tags) asociadas al elemento seleccionado.
    if "file" in item_tags or "folder" in item_tags:  # Verifica si el elemento seleccionado es un archivo o una carpeta.
       
        response = messagebox.askyesno("Eliminar", "¿Estás seguro de que deseas eliminar este elemento?") # Solicita confirmación 
        if response:  # Verifica la respuesta del usuario.
            # Obtiene la ruta del archivo o carpeta a eliminar.
            path = tree.item(selected_item)["values"][0]
            if os.path.isfile(path): # Verifica si la ruta corresponde a un archivo.
                os.remove(path)  # Elimina el archivo.
            elif os.path.isdir(path): # Verifica si la ruta corresponde a una carpeta.
                os.rmdir(path)# Elimina la carpeta.

            tree.delete(selected_item) # Elimina el elemento del árbol.
            print("Elemento eliminado")# Imprime un mensaje indicando que el elemento fue eliminado.


# Función para copiar un archivo o carpeta
def copy_item():
    """
    Copia el archivo o carpeta seleccionado.
    """
    global copied_item # Declara la variable global para almacenar el elemento copiado.
    selected_item = tree.focus() #obtiene el elemento seleccionado
    item_tags = tree.item(selected_item)["tags"] #obtiene las etiquetas del elemento seleccionado
    if "file" in item_tags or "folder" in item_tags: 
        copied_item = tree.item(selected_item)["values"][0] # Almacena la ruta del archivo o carpeta en la variable global.
        print("Elemento copiado")

# Función para pegar el archivo o carpeta copiado
def paste_item():
    """
    Pega el archivo o carpeta previamente copiado en la ubicación actual del árbol.
    """
    global copied_item # Declara la variable global que almacena el elemento copiado.

    # Verifica si hay un elemento copiado.
    if copied_item:
        selected_item = tree.focus()  # Obtiene el elemento seleccionado.
        item_tags = tree.item(selected_item)["tags"] # Obtiene las etiquetas (tags) asociadas al elemento seleccionado.
        if "folder" in item_tags: # Verifica si el elemento seleccionado es una carpeta.
            destination_folder = tree.item(selected_item)["values"][0]# Obtiene la ruta de la carpeta destino.
            destination_path = os.path.join(destination_folder, os.path.basename(copied_item)) # Construye la ruta completa del destino.

            # Verifica si el elemento copiado es un archivo.
            if os.path.isfile(copied_item):
                shutil.copy2(copied_item, destination_path)   # Copia el archivo al destino.
                tree.insert(selected_item, "end", text=os.path.basename(copied_item), values=(destination_path,), tags=("file",))# Inserta el nuevo archivo en el árbol.
                print("Elemento pegado")

            # Verifica si el elemento copiado es una carpeta.
            elif os.path.isdir(copied_item):
                shutil.copytree(copied_item, destination_path)# Copia la carpeta al destino.
                # Inserta la nueva carpeta en el árbol.
                tree.insert(selected_item, "end", text=os.path.basename(copied_item), values=(destination_path,), tags=("folder",))
                print("Elemento pegado")

        # Reinicia la variable global que almacena el elemento copiado.
        copied_item = ""

        
# Función para renombrar un archivo o carpeta
def rename_item():
    selected_item = tree.focus() # Obtiene el elemento actualmente seleccionado en el árbol.
    item_tags = tree.item(selected_item)["tags"] # Obtiene las etiquetas (tags) asociadas al elemento seleccionado.

    if "folder" in item_tags: # Verifica si el elemento seleccionado es una carpeta
        folder_path = tree.item(selected_item)["values"][0]# Obtiene la ruta de la carpeta a renombrar.
        current_name = os.path.basename(folder_path) # Obtiene el nombre actual de la carpeta.
        new_name = simpledialog.askstring("Renombrar Carpeta", "Ingrese el nuevo nombre de la carpeta:", initialvalue=current_name)
        # Verifica si se ingresó un nuevo nombre.
        if new_name:
            new_folder_path = os.path.join(os.path.dirname(folder_path), new_name) # Construye la nueva ruta de la carpeta.
            try:
                os.rename(folder_path, new_folder_path) # Intenta renombrar la carpeta.
                tree.item(selected_item, text=new_name, values=(new_folder_path,)) # Actualiza el texto y los valores del elemento en el árbol.
                messagebox.showinfo("Renombrar Carpeta", "La carpeta se ha renombrado correctamente.")

            except Exception as e:
                messagebox.showerror("Renombrar Carpeta", f"No se pudo renombrar la carpeta:\n{str(e)}")# Muestra un mensaje de error si no se pudo renombrar la carpeta.

    # Si el elemento seleccionado no es una carpeta, asume que es un archivo.
    else:
        file_path = tree.item(selected_item)["values"][0]# Obtiene la ruta del archivo a renombrar.
        current_name = os.path.basename(file_path)# Obtiene el nombre actual del archivo.
        new_name = simpledialog.askstring("Renombrar Archivo", "Ingrese el nuevo nombre del archivo:", initialvalue=current_name)
        # Verifica si se ingresó un nuevo nombre.
        if new_name:
            new_file_path = os.path.join(os.path.dirname(file_path), new_name) # Construye la nueva ruta del archivo.
            try:
                os.rename(file_path, new_file_path)# Intenta renombrar el archivo.
                tree.item(selected_item, text=new_name, values=(new_file_path,)) # Actualiza el texto y los valores del elemento en el árbol.
                messagebox.showinfo("Renombrar Archivo", "El archivo se ha renombrado correctamente.")

            except Exception as e:
                # Muestra un mensaje de error si no se pudo renombrar el archivo.
                messagebox.showerror("Renombrar Archivo", f"No se pudo renombrar el archivo:\n{str(e)}")

# Crear la ventana principal
window = tk.Tk()
window.title("Explorador de Archivos")

# Crear el árbol y el scrollbar
tree = ttk.Treeview(window)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)

# Agregar una barra de búsqueda
search_entry = ttk.Entry(window)
search_entry.pack(pady=5)

search_button = ttk.Button(window, text="Buscar", command=search_items)
search_button.pack(pady=5)

# Agregar botones para crear, eliminar, copiar y pegar
create_button = ttk.Button(window, text="Crear", command=create_item)
create_button.pack(pady=5)

delete_button = ttk.Button(window, text="Eliminar", command=delete_item)
delete_button.pack(pady=5)

copy_button = ttk.Button(window, text="Copiar", command=copy_item)
copy_button.pack(pady=5)

paste_button = ttk.Button(window, text="Pegar", command=paste_item)
paste_button.pack(pady=5)

# Variable global para almacenar la ruta del elemento copiado
copied_item = ""

# Agregar el botón de renombrar
action_frame = ttk.Frame(window)
action_frame.pack(pady=10)
rename_button = ttk.Button(action_frame, text="Renombrar", command=rename_item)
rename_button.pack(side=tk.LEFT, padx=5)



# Construir el árbol inicial
build_tree(r'C:\Users\miche\OneDrive\Documentos\Escritorio\Universidad\estructura de datos\Proyectos', "")

# Ejecutar el bucle principal del programa
window.mainloop()