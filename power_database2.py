import pandas as pd
import cx_Oracle

def connect_to_oracle():
    try:
        cx_Oracle.init_oracle_client(lib_dir="/Users/youssefchaabi/instantclient_19_16")
    except:
        print("An exception occurred")
    # Remplace les valeurs ci-dessous par tes propres paramètres de connexion
    dsn = cx_Oracle.makedsn("localhost", "1521", service_name="XEPDB1")
    conn = cx_Oracle.connect(user="SEFORMER", password="153300", dsn=dsn)
    return conn

file = open('code_insertion.sql', 'w')
data = pd.read_csv("./formateurs.csv")

conn = connect_to_oracle()

cursor = conn.cursor()
i=0
for index, row in data.iterrows():
    cursor = conn.cursor()
    print(i, "-------", row.id_formateur, row.adresse, row.numero, row.site, row.formation_ID)
    values = [
        row['formation_ID'],
        row['id_formateur'],
        None if pd.isna(row['adresse']) else row['adresse'],
        None if pd.isna(row['numero']) else row['numero'],
        None if pd.isna(row['site']) else row['site']
    ]
    
    '''item = "INSERT INTO FORMER (ID_FORMATION, ID_FORMATEUR, ADRESSE, TELEPHONE, SITE_WEB) VALUES (" + \
           str(values[0]) + ", " + str(values[1]) + ", '" + str(values[2]) + "', '" + str(values[3]) + "', '" + str(values[4]) + "');\n"
    
    # Écrire dans le fichier
    with open("insert_statements.sql", "a") as file:
        file.write(item)'''
    cursor.execute("INSERT INTO FORMER (ID_FORMATION, ID_FORMATEUR, ADRESSE, TELEPHONE, SITE_WEB) VALUES (:1, :2, :3, :4, :5)", values)
    cursor.close()
    i=i+1
    
conn.commit()
conn.close()
