import sqlite3
import hashlib

conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        usuario TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY,
        titulo TEXT UNIQUE NOT NULL,
        descripcion TEXT,
        vencimiento DATE,
        estado INTEGER DEFAULT 0,
        id_usuario INTEGER,
        FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
)''')

conn.commit()

def registrar_usuario(usuario, contrasena, email):
    hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

    cursor.execute('''
    INSERT INTO usuarios (usuario, contrasena, email) 
    VALUES (?, ?, ?)''', (usuario, hash_contrasena, email))
    conn.commit()

def iniciar_sesion(usuario, contrasena):
    hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

    cursor.execute('''
        SELECT id FROM usuarios
        WHERE usuario = ? and contrasena = ?''', (usuario, hash_contrasena))

    id_usuario = cursor.fetchone()

    if id_usuario:
        print("Bienvenido al sistema!")
        return id_usuario[0]
    else:
        print("Credenciales invalidas!")
        return None

def agregar_tarea(titulo, descripcion, vencimiento, id_usuario):
    cursor.execute('''
        INSERT INTO tareas (titulo, descripcion, vencimiento, id_usuario)
        VALUES (?, ?, ?, ?)''', (titulo, descripcion, vencimiento, id_usuario))

    conn.commit()
def mostrar_lista_todo(id_usuario):
    cursor.execute('''
        SELECT id, titulo, descripcion, vencimiento, estado
        FROM tareas
        WHERE id_usuario = ? ''', (id_usuario))

    tareas = cursor.fetchall()

    if tareas:
        print("Listado de Tareas:")
        for tarea in tareas:
            print(f"Tarea: {tarea[0]}, Titulo: {tarea[1]}, Descripcion: {tarea[2]}, Vencimiento: {tarea[3]}, Estado: {'Completada' if tarea[4] else 'Incompleta'}")
        else:
            print("Felicidades! No hay tareas")

if __name__ == "__main__":
    registrar_usuario('petra', 'abc123', 'petra@ejemplo.com')
    id_usuario = iniciar_sesion('petra', 'abc123')

    if id_usuario:
        agregar_tarea('Parcial de Ciencias', 'Terminar de estudiar', '2024-01-23', id_usuario)
        agregar_tarea('Aprender AI', 'Estudiar AI', '2024-02-15', id_usuario)
        mostrar_lista_todo(id_usuario)

    conn.close()