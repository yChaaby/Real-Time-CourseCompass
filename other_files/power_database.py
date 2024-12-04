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


data = pd.read_csv("./formateurs.csv")

conn = connect_to_oracle()

cursor = conn.cursor()
i=0
for index, row in data.iterrows():
    cursor = conn.cursor()
    print(i, "-------", row.formateur, row.adresse, row.numero, row.site, row.formation_ID)
    values = [
        row['formateur'],
        None if pd.isna(row['adresse']) else row['adresse'],
        None if pd.isna(row['numero']) else row['numero'],
        None if pd.isna(row['site']) else row['site'],
        None if pd.isna(row['formation_ID']) else row['formation_ID']
    ]
    cursor.execute("INSERT INTO FORMATEURS (NOM_FORMATEUR, ADRESSE, NUMERO, SITE_WEB, FORMATION_ID) VALUES (:1, :2, :3, :4, :5)", values)
    cursor.close()
    i=i+1
    
conn.commit()
conn.close()
