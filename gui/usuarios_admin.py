from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PySide6.QtUiTools import QUiLoader

from data.usuario_data import UsuarioData

class Usuarios():
    def __init__(self,volver_callback=None):
        loader = QUiLoader()
        self.ventana = loader.load("gui/usuarios_admin.ui")

        #acceso a datos 
        self.usuario_data = UsuarioData()
        self.initGUI()
        self.cargarUsuarios() #trae los datos desde la base de datos a la interfaz
        self.ventana.show()
        self.volver_callback = volver_callback

    #INIALIZACION DE BOTONES
    def initGUI(self):
        self.ventana.btn_registrar.clicked.connect(self.crearUsuario)
        self.ventana.btn_eliminar.clicked.connect(self.eliminarUsuario)
        self.ventana.btn_volver.clicked.connect(self.volver)

    #CARGAR USUARIOS EN TABLA
    def cargarUsuarios(self):
        usuarios = self.usuario_data.obtener_usuarios()
        self.ventana.tabla_usuarios.setRowCount(len(usuarios))

        for fila, usuario in enumerate(usuarios):
            self.ventana.tabla_usuarios.setItem(
                fila,0, QTableWidgetItem(str(usuario.id)))
            self.ventana.tabla_usuarios.setItem(
                fila,1, QTableWidgetItem(str(usuario.nombre)))
            self.ventana.tabla_usuarios.setItem(
                fila,2, QTableWidgetItem(str(usuario.usuario)))
            self.ventana.tabla_usuarios.setItem(
                fila,3, QTableWidgetItem(str(usuario.rol)))
    
    #CREAR USUARIO 
    def crearUsuario(self):
        nombre = self.ventana.txt_nombre.text()
        usuario = self.ventana.txt_usuario.text()
        clave = self.ventana.txt_clave.text()
        rol = self.ventana.combo_rol.currentText()

        if nombre == "" or usuario == "" or clave =="":
            QMessageBox.warning( 
                self.ventana, "Error", "Complete todos los campos"
            )
            return
        
        #crear usuario
        self.usuario_data.crear_usuario(
            nombre, usuario, clave, rol)
        
        QMessageBox.information(
            self.ventana, "OK", "Usuario creado correctamente"
        )

        #limpio imputs
        self.ventana.txt_nombre.clear()
        self.ventana.txt_usuario.clear()
        self.ventana.txt_clave.clear()

        #recargar tabla
        self.cargarUsuarios()
    
    #ELIMINAR USUARIO
    def eliminarUsuario(self): 
        fila = self.ventana.tabla_usuarios.currentRow()
        
        if fila < 0:
            QMessageBox.warning(
                self.ventana, "Error", "Seleccione un usuario"
            )
            return
        
        id_usuario = self.ventana.tabla_usuarios.item(fila,0).text()
        self.usuario_data.eliminar_usuario(id_usuario)
        QMessageBox.information(
            self.ventana, "OK", "Usuario eliminado")      
        self.cargarUsuarios()
    
    def volver(self):
        self.ventana.close()
        if self.volver_callback:
            self.volver_callback()
            
