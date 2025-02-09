create table FORMATION
(
    ID_FORMATION    NUMBER        not null
        constraint PK_ID_FORMATION
            primary key,
    TITRE_FORMATION VARCHAR2(300) not null,
    KEYWORDS        VARCHAR2(400),
    ID_SOUS_DOMAINE NUMBER
)
/

