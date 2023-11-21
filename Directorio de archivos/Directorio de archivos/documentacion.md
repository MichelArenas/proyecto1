## DOCUMENTACIÓN

1. Importaciones:

    1.1 os: Proporciona funciones para interactuar con el sistema operativo, como explorar directorios y manipular archivos.
    2.2 tkinter: Proporciona clases y métodos para crear la interfaz gráfica de usuario.
    ttk: Módulo complementario de Tkinter que proporciona widgets adicionales y estilos mejorados.
    2.3 messagebox: Proporciona funciones para mostrar cuadros de diálogo de mensaje.
    2.4 simpledialog: Proporciona funciones para mostrar cuadros de diálogo de entrada simple.

2. Función build_tree(dir_path, parent):

    2.1 Construye de manera recursiva el árbol de archivos y carpetas.
    2.2 Recibe la ruta de un directorio dir_path y el identificador del elemento padre en el árbol parent.
    2.3 Utiliza os.scandir() para explorar el contenido del directorio.
    2.4 Inserta elementos en el árbol utilizando el método insert() del widget Treeview.

3. Función search_items():

    3.1 Realiza la búsqueda de archivos y carpetas en el sistema de archivos.
    3.2 Obtiene el término de búsqueda ingresado por el usuario.
    3.3 Borra todos los elementos del árbol y luego llama a build_tree() con el término de búsqueda como directorio raíz.

4. Función create_item():

    4.1 Crea una nueva carpeta o archivo en la ubicación actual del árbol.
    4.2 Obtiene el elemento seleccionado en el árbol.
    4.3 Si el elemento seleccionado es una carpeta, solicita al usuario un nombre para la nueva carpeta y crea la carpeta utilizando os.makedirs().
    4.4 Si el elemento seleccionado es un archivo, solicita al usuario un nombre para el nuevo archivo y crea el archivo utilizando open().

5. Función delete_item():

    5.1 Elimina el archivo o carpeta seleccionado del árbol y del sistema de archivos.
    5.2 Obtiene el elemento seleccionado en el árbol.
    5.3 Si el elemento seleccionado es un archivo, utiliza os.remove() para eliminar el archivo.
    5.4 Si el elemento seleccionado es una carpeta, utiliza os.rmdir() para eliminar la carpeta.

6. Función copy_item():

    6.1 Copia el archivo o carpeta seleccionado.
    6.2 Obtiene el elemento seleccionado en el árbol y guarda su ruta en la 6.6.3 variable global copied_item.

7. Función paste_item():

    7.1 Pega el archivo o carpeta previamente copiado en la ubicación actual del árbol.
    7.2 Obtiene el elemento seleccionado en el árbol.
    7.3 Si el elemento seleccionado es una carpeta, utiliza shutil.copy2() para copiar el archivo o shutil.copytree() para copiar la carpeta.

8. Función rename_item():

    8.1 Renombra un archivo o carpeta.
    8.2 Obtiene el elemento seleccionado en el árbol y determina si es una carpeta o un archivo.
    8.3 Solicita al usuario un nuevo nombre y utiliza os.rename() para cambiar el nombre del archivo o carpeta.

9. Creación de la ventana principal y configuración de la interfaz:

    9.1 Se crea una instancia de la clase Tk() para crear la ventana principal.
    9.2 Se configuran el título y el tamaño de la ventana.
    9.3 Se crean los elementos de la interfaz gráfica, como el árbol, el scrollbar y los botones.
    9.4 Se define una variable global copied_item para almacenar la ruta del elemento copiado.

10. Construcción del árbol inicial:

    10.1 Se llama a build_tree() con la ruta del directorio inicial y un identificador vacío para construir el árbol al iniciar el programa.

11. Bucle principal del programa:

    11.1 Se ejecuta el bucle principal de la aplicación llamando al método mainloop() de la ventana principal. Esto permite que la interfaz de usuario sea interactiva y responda a las acciones del usuario.