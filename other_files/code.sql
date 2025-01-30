CREATE SEQUENCE SEQ_ID_FORMATEUR
START WITH 1 -- premier ID
INCREMENT BY 1; -- incrémentation par 1

ALTER TABLE FORMATIONS
ADD CONSTRAINT pk_id_formation PRIMARY KEY (ID_FORMATION);
-- Création de la table FORMATEURS
CREATE TABLE FORMATEURS (
    ID_FORMATEUR NUMBER PRIMARY KEY, -- ID principal
    ADRESSE VARCHAR2(255),           -- Adresse
    NUMERO VARCHAR2(15),             -- Numéro de téléphone
    SITE_WEB VARCHAR2(255),          -- Site web / lien
    FORMATION_ID NUMBER,             -- Clé étrangère vers la table FORMATIONS
    CONSTRAINT fk_formation
        FOREIGN KEY (FORMATION_ID)
        REFERENCES FORMATIONS(ID_FORMATION)
);

-- Ajout d'un trigger pour l'auto-incrémentation de ID_FORMATEUR
CREATE OR REPLACE TRIGGER trg_auto_increment_formateur
BEFORE INSERT ON FORMATEURS
FOR EACH ROW
BEGIN
    IF :NEW.ID_FORMATEUR IS NULL THEN
        SELECT SEQ_ID_FORMATEUR.NEXTVAL INTO :NEW.ID_FORMATEUR FROM DUAL;
    END IF;
END;


-- pour selectionné les formations qui ont pas des formateurs
select *
from FORMATIONS
where FORMATION_COURS not in
      (select FORMATIONS.FORMATION_COURS as FORMATION_COURS
       from FORMATIONS, FORMATEURS
       where FORMATIONS.ID_FORMATION = FORMATEURS.FORMATION_ID)


DECLARE
    CURSOR data IS SELECT NOM_FORMATEUR, ID_FORMATEUR FROM FORMATEURS ORDER BY NOM_FORMATEUR;
    tempvar FORMATEURS.ID_FORMATEUR%TYPE;
BEGIN
    FOR le_id IN data LOOP

        SELECT MIN(ID_FORMATEUR) into tempvar FROM FORMATEURS WHERE NOM_FORMATEUR = le_id.NOM_FORMATEUR;
        DBMS_OUTPUT.put_line('UPDATE FORMATEURS SET TEMP_ID = '|| tempvar ||' where ID_FORMATEUR = '|| le_id.ID_FORMATEUR ||' ;');
    END LOOP;
END;


INSERT INTO FORMER(ID_FORMATION, ID_FORMATEUR, ADRESSE, TELEPHONE, SITE_WEB) VALUES (233,(SELECT ID_FORMATEUR FROM FORMATEURS WHERE NOM_FORMATEUR='ESSEC Business School'),'en ligne','0570708909','https://www.coursera.org/learn/fondamentaux-negociation');
