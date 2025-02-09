create table FORMATEUR
(
    ID_FORMATEUR      NUMBER        not null
        constraint FORMATEUR_PK
            primary key,
    NOM_FORMATEUR     VARCHAR2(300) not null,
    IMAGE             VARCHAR2(300),
    AVIS_MOYEN        FLOAT,
    NB_TOTAL_AVIS     NUMBER,
    NB_TOTAL_ETUDIANT NUMBER,
    SITE_WEB          VARCHAR2(300),
    DESCRIPTION       CLOB
)
/

