create table RECOMMENDATION
(
    IDRECOMMENDATION NUMBER generated as identity,
    IDHIST           NUMBER
        constraint FKRECHIST
            references HISTORY_SEARCH,
    SCORE            FLOAT
)
/

