Usé algunos ejemplos que encontré en internet para aplicar el css, me enredé un poco. Me imagino que tengo mucho codigo repetido. Las validaciones
fueron divertidas (excepto la foto, la maldigo). 

Para implementar la seleccion multiple de deportes/fotos/tipos de artesania usé un multiple que permitia seleccionar mas de una apretando el control y el click.

Agregar artesano los agrega bien, no se si se me pasó alguna validación.

Cree y verifiqué en su mayoria con una base de datos local hecha con MySqL Workbench.

Usé esto para agrandar la columna de email, mi email tenia 32 char y solo aceptaban 30
ALTER TABLE tarea2.artesano MODIFY COLUMN email VARCHAR(50);
Mismo caso para hincha
ALTER TABLE tarea2.hincha MODIFY COLUMN email VARCHAR(50);

ejecuto con python app.py, tanto dentro como fuera del venv

Agregar hincha agrega bien, se muestran bien cada uno y su información, quizas con algunos retoques se veria mejor el tema de mostrar la lista de cosas.
Casi borro todo el programa al intentar cambiarle el nombre a la carpeta, pero me va bien.