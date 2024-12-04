import pandas as pd
from app import connect_to_oracle

data = pd.read_csv("./formateurs.csv")

conn = connect_to_oracle()

cursor = conn.cursor()

for index, row in data.iterrows():
    cursor.execute("INSERT INTO FORMATEURS (NOM_FORMATEUR, ADRESSE, NUMERO, SITE_WEB, FORMATION_ID) VALUES (:1, :2, :3, :4, :5)", [row.formateur, row.adresse, row.numero, row.site, row.formation_ID])
    cursor.close()

conn.close()

