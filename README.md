# test_etl_etraining

Buen día

Aquí dejo las instrucciones para poder validar la prueba correctamente:

## COMENTARIO DE AJUSTE INICIAL
Inicial partto de que cuento con una pequeña diferencia en el archivo suministrado llamado "Casos_positivos_de_COVID-19-Cund-Boy.csv"

AL hacer un análisis previo de la base de datos, veo que quieren mostrar estadísticas a los contagios COVID de Cundinamarca y Boyaca (Municipios de Colombia)
Quieren hacerlo por status, Departamento, sexo y tipo de contagio. Pero, resulta, que la base está diferente a la necesidad creo tienen, dado que id_departamento muestra ZIPAQUIRA, SOPO, BOJACA (Es decir, municipios) y el que menciona como id_municipio muestra (CUNDINAMARCA Y BOYACA) el cuál, debería ser los departamentos.

Es decir, dentro de la base de datos los títulos se encuentran de la siguiente manera (Junto con los 3 primeros registros)

| id_case | id_municipality | name_municipality | id_department | name_department | age | gender | type_contagion | status | date_symptom | date_death | date_diagnosis | date_recovery |
|---------|-----------------|-------------------|---------------|-----------------|-----|--------|----------------|--------|--------------|------------|----------------|---------------|
| 489982  | 25              | CUNDINAMARCA      | 25899         | ZIPAQUIRA       | 22  | F      | Comunitaria    | Recuperado | 2/08/2020  |            | 18/08/2020     | 20/12/2020    |
| 5932109 | 25              | CUNDINAMARCA      | 25758         | SOPO            | 50  | M      | Comunitaria    | Recuperado | 18/01/2022 |            | 2/02/2022      | 5/02/2022     |
| 3036330 | 25              | CUNDINAMARCA      | 25099         | BOJACA          | 67  | M      | Comunitaria    | Recuperado | 4/05/2021  |            | 8/05/2021      | 18/05/2021    |

Pero, para mi concepto, según el análisis previo deberían ir de la siguiente manera

| id_case | id_department | name_department | id_municipality | name_municipality | age | gender | type_contagion | status | date_symptom | date_death | date_diagnosis | date_recovery |
|---------|---------------|-----------------|-----------------|-------------------|-----|--------|----------------|--------|--------------|------------|----------------|---------------|
| 489982  | 25            | CUNDINAMARCA    | 25899           | ZIPAQUIRA         | 22  | F      | Comunitaria    | Recuperado | 2/08/2020  |            | 18/08/2020     | 20/12/2020    |
| 5932109 | 25            | CUNDINAMARCA    | 25758           | SOPO              | 50  | M      | Comunitaria    | Recuperado | 18/01/2022 |            | 2/02/2022      | 5/02/2022     |
| 3036330 | 25            | CUNDINAMARCA    | 25099           | BOJACA            | 67  | M      | Comunitaria    | Recuperado | 4/05/2021  |            | 8/05/2021      | 18/05/2021    |

Ya con este cambio de columnas de la base, cuadra totalmente tanto la creación de la base de datos, como el análisis que se quiere realizar.

## PUNTO 1

en el archivo "Script MySQL.sql" dejé el código con los CREATE de la base de datos. Dejo en comentario la creación del SCHEMA utilizado "test" en caso de requerir su creación para pruebas.

Al generar el Diagrama ER mediante Ingeniería Inversa, arroja el resultado que se encuentra en PDF en "Diagrama ER.pdf" el cual, es igual al ejercicio solicitado.

## PUNTO 2

Este punto lo realice mediante un Entorno virtual llamado .venv
en .venv se encuentan todas las librerias (Usando Python 3.12) con el fin de instalar las librerias de requirements.txt

Versión original del requirements.txt
pandas
mysql-connector

Luego de ejecutar el comando pip freeze > requirements.txt se versiona cada una de las librerias

Luego de activar el entorno .venv, y tener la conexión de MySQL activa, se prosigue solamente a ejecutar el código, el cuál correra la función main() que contiene todo lo requerido en el punto 2
Es necesario destacar, que para este punto, es necesario haber creado previamente las tablas, con la información de "script MySQL.sql" usando en SCHEMA "test" 

Por último, como prueba de funcionamiento de la ETL, adjunto una pantalla llamada "Prueba funcionamiento ETL.png" el cuál contiene 
un SELECT de la tabla cases, como muestra de que efectivamente carga la información.



## PUNTO 3
Tablero de Power BI requiere la modificar la conexión MySQL teniendo en cuenta el cambio del host

Adicionalmente, debido a la conexión en MySQL con Power BI, se requiere el siguiente complemento
https://dev.mysql.com/downloads/file/?id=526912


Luego de aplicado el conector, dar en Obtener datos, Mas.., y al aparecer el recuadro con opciones de consulta dar en Base de datos MySQL

En los parámetros colocar:
Servidor: localhost
Base de datos: test

Al solicitar los permisos de acceso colocar "Credenciales de base de datos" y colocar la siguiente información
Usuario: root
Contraseña: 1234567890


Seleccionar todas las tablas del modelo y cargar.

Para que tuviera màs calidad la consulta la hice una por una mediante consulta avanzada, colocando SELECT * FROM table_name, con el fin de armar bien el Esquema en Power BI, como se puede ver en la imagen "Diagrama Modelo Power BI.png"
