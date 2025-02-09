create table HISTORY_SEARCH
(
    ID_HIST_S        NUMBER generated as identity
        constraint PKHIST
            primary key,
    ID_CLIENT        NUMBER
        constraint FKHISTCLI
            references CLIENTS,
    ID_FORMATION     NUMBER
        constraint FKHISTFOR
            references FORMATION,
    DATE_TIME_SEARCH TIMESTAMP(6)
)
/

