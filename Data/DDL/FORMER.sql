create table FORMER
(
    ID_FORMATION         NUMBER not null
        constraint FORMER_FK1
            references FORMATION
                on delete cascade,
    ID_FORMATEUR         NUMBER not null
        constraint FORMER_FK2
            references FORMATEUR,
    ADRESSE              VARCHAR2(150),
    NUMERO               VARCHAR2(25),
    SITE_WEB             VARCHAR2(285),
    DESCRIPTION          CLOB,
    EMAIL                VARCHAR2(20),
    NIVEAU_INSTRUCTION   VARCHAR2(20),
    ID_COLLABORATEUR     NUMBER
        constraint FKCOLLABORATEUR
            references COLLABORATEUR,
    ID_FOURNISSEUR       NUMBER
        constraint FKFOURNISSEUR
            references FOURNISSEUR,
    ID_EDITEUR           NUMBER
        constraint FKEDITEUR
            references EDITEUR,
    MEILLEUR_AVIS        FLOAT,
    NB_ETUDIANT          NUMBER,
    PIRE_AVIS            FLOAT,
    IS_PAYANT            NUMBER(1) default 0
        check (is_payant IN (0, 1)),
    PRIX_APRES_REDUCTION FLOAT,
    NB_AVIS              NUMBER,
    AVIS                 FLOAT,
    CODE_POSTAL          VARCHAR2(10)
        references VILLE,
    constraint PKFORMERALL
        primary key (ID_FORMATION, ID_FORMATEUR)
)
/

