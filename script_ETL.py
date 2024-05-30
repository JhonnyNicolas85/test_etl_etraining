import pandas as pd
import mysql.connector
from mysql.connector import errorcode

#Función para extrae la data completa del csv
def extract_data(name_archive):
    df = pd.read_csv(name_archive,delimiter=";",header=0)
    return df

#Función para transformar la data de forma limpia, sin eliminar NaN
def transform_data(df):
    date_columns = ['date_symptom', 'date_death', 'date_diagnosis', 'date_recovery']
    for column in date_columns:
        df[column] = pd.to_datetime(df[column], format='%d/%m/%Y', errors='coerce')
        df[column] = df[column].where(df[column].notna(), None) #Para la inserción reemplazar por None
    
    return df

#Función de creación de conexión con
def create_connection():
    try:
        connection = mysql.connector.connect(
            user='root',
            password='1234567890',
            host='localhost',
            database='test'
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu usuario o contraseña")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)
        return None

#Función para checkear valores globales de municipios (En caso de no encontrarlo, agregarlo)
def check_and_insert_municipalities(data, connection):

    cursor = connection.cursor()
    unique_municipalities = data[['id_municipality', 'name_municipality', 'id_department']].drop_duplicates().dropna()
    for _, row in unique_municipalities.iterrows():
        cursor.execute("SELECT COUNT(*) FROM municipality WHERE id_municipality = %s", (row['id_municipality'],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO municipality (id_municipality, name, id_department) VALUES (%s, %s, %s)",
                           (row['id_municipality'], row['name_municipality'], row['id_department']))
    
    connection.commit()
    cursor.close()
    print('Base de municipios poblada con éxito')

#Función para checkear valores globales de departamentos (En caso de no encontrarlo, agregarlo)
def check_and_insert_departments(data, connection):
    cursor = connection.cursor()
    unique_departments = data[['id_department', 'name_department']].drop_duplicates().dropna()

    for _, row in unique_departments.iterrows():
        cursor.execute("SELECT COUNT(*) FROM department WHERE id_department = %s", (row['id_department'],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO department (id_department, name) VALUES (%s, %s)",
                           (row['id_department'], row['name_department']))

    connection.commit()
    cursor.close()
    print('Base de departamentos poblada con éxito')

#Función para checkear valores globales de genders (En caso de no encontrarlo, agregarlo)
def check_and_insert_genders(data, connection):
    cursor = connection.cursor()
    unique_genders = data[['gender']].drop_duplicates().dropna()
    for _, row in unique_genders.iterrows():
        cursor.execute("SELECT COUNT(*) FROM gender WHERE name = %s", (row['gender'],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO gender (name) VALUES (%s)", (row['gender'],))

    connection.commit()
    cursor.close()
    print('Base de genders poblada con éxito')

#Función para checkear valores globales de type_contagion (En caso de no encontrarlo, agregarlo)
def check_and_insert_type_contagion(data, connection):
    cursor = connection.cursor()
    unique_type_contagion = data[['type_contagion']].drop_duplicates().dropna()
    for _, row in unique_type_contagion.iterrows():
        cursor.execute("SELECT COUNT(*) FROM type_contagion WHERE name = %s", (row['type_contagion'],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO type_contagion (name) VALUES (%s)", (row['type_contagion'],))

    connection.commit()
    cursor.close()
    print('Base de type contagion poblada con éxito')

#Función para checkear valores globales de status (En caso de no encontrarlo, agregarlo)
def check_and_insert_status(data, connection):
    cursor = connection.cursor()
    unique_status = data[['status']].drop_duplicates().dropna()
    for _, row in unique_status.iterrows():
        cursor.execute("SELECT COUNT(*) FROM status WHERE name = %s", (row['status'],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO status (name) VALUES (%s)", (row['status'],))

    connection.commit()
    cursor.close()
    print('Base de status poblada con éxito')

#Función especial para buscar el ID autogenerado de los valores que se encuentren en la tabla cases para inserción
def get_id_by_name(connection, table, name_column, name_value, id_column):
    if pd.isna(name_value):
        return None
    cursor = connection.cursor()
    cursor.execute(f"SELECT {id_column} FROM {table} WHERE {name_column} = %s", (name_value,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

 #Función de cargue de la información global (De todas las bases de datos)   

#Función para cargar los datos en MySQL
def load_data(df,table_name):
    
    conn = create_connection()
    if conn is None:
        return

    # Funciones con el fin de poblar las bases de datos.
    check_and_insert_departments(df, conn)
    check_and_insert_municipalities(df, conn)
    check_and_insert_genders(df, conn)
    check_and_insert_type_contagion(df, conn)
    check_and_insert_status(df, conn)

    cursor = conn.cursor()
    insert_count = 0 #Responde cuantos datos se ingresan
    update_count = 0 #Responde cuantos datos se actualizan

    for _, row in df.iterrows():
        id_gender = get_id_by_name(conn, 'gender', 'name', row['gender'], 'id_gender')
        id_type_contagion = get_id_by_name(conn, 'type_contagion', 'name', row['type_contagion'], 'id_type_contagion')
        id_status = get_id_by_name(conn, 'status', 'name', row['status'], 'id_status')

        if any(pd.isna([id_gender, id_type_contagion, id_status])):
            continue

        cursor.execute("SELECT COUNT(*) FROM cases WHERE id_case = %s", (row['id_case'],))
        if cursor.fetchone()[0] == 0:
            cursor.execute(f"""
                INSERT INTO {table_name} (
                    id_case, id_municipality, age, id_gender, id_type_contagion, id_status, 
                    date_symptom, date_death, date_diagnosis, date_recovery
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                row['id_case'], row['id_municipality'], row['age'], id_gender, id_type_contagion, 
                id_status, row['date_symptom'], row['date_death'], row['date_diagnosis'], row['date_recovery']
            ))
            insert_count += 1
        else:
            cursor.execute(f"""
                UPDATE {table_name} SET
                    id_municipality = %s, age = %s, id_gender = %s, id_type_contagion = %s, id_status = %s, 
                    date_symptom = %s, date_death = %s, date_diagnosis = %s, date_recovery = %s
                WHERE id_case = %s""", (
                row['id_municipality'], row['age'], id_gender, id_type_contagion, 
                id_status, row['date_symptom'], row['date_death'], row['date_diagnosis'], row['date_recovery'],
                row['id_case']
            ))
            update_count += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f'Base de datos cargada con éxito. Insertados: {insert_count}, Actualizados: {update_count}')
    return 0

#Función para ejecutar la ETL globalmente (Es necesario tener la conexión test activa (Leer README.txt))
def main():
    csv_path = 'Documentos\Casos_positivos_de_COVID-19-Cund-Boy MODIFICADO.csv'
    df_data = extract_data(csv_path)
    df_data_transf = transform_data(df_data)
    load_data(df_data_transf,'cases')
    return 0

main()


