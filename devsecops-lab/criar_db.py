import sqlite3

conn = sqlite3.connect("banco.db")

cursor = conn.cursor()

cursor.execute("""
DROP TABLE IF EXISTS alunos
""")

cursor.execute("""
DROP TABLE IF EXISTS usuarios
""")

cursor.execute("""
CREATE TABLE usuarios(

id INTEGER PRIMARY KEY AUTOINCREMENT,

usuario TEXT,

senha TEXT,

perfil TEXT

)
""")

cursor.execute("""
CREATE TABLE alunos(

id INTEGER PRIMARY KEY,

nome TEXT,

curso TEXT,

nota REAL

)
""")

cursor.executemany(
"""
INSERT INTO usuarios(usuario,senha,perfil)
VALUES(?,?,?)
""",
[
("admin","admin123","admin"),
("professor","prof123","professor"),
("joao","123456","aluno")
]
)

cursor.executemany(
"""
INSERT INTO alunos
VALUES(?,?,?,?)
""",
[
(1,"Ana","IA",8.5),
(2,"Carlos","IA",6.2),
(3,"Mariana","Ciência de Dados",9.1),
(4,"Pedro","Computação",7.4)
]
)

cursor.execute("""
CREATE TABLE comentarios(

id INTEGER PRIMARY KEY AUTOINCREMENT,

autor TEXT,

comentario TEXT

)
""")

cursor.executemany(
"""
INSERT INTO comentarios(autor,comentario)
VALUES(?,?)
""",
[
("Ana","Gostei muito da disciplina."),
("Carlos","Excelente conteúdo.")
]
)

conn.commit()

conn.close()

print("Banco criado.")