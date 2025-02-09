create table SOUS_DOMAINE
(
    ID_SOUS_DOMAINE  NUMBER generated as identity
        primary key,
    ID_DOMAINE       NUMBER
        references DOMAINE,
    NOM_SOUS_DOMAINE VARCHAR2(100) not null
)
/

