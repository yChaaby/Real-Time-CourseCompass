create PROCEDURE recherche_formation (
    p_mot_cle IN VARCHAR2
) AS
    CURSOR cur_formation IS
        SELECT ID_FORMATION, FORMATION_COURS, UTL_MATCH.JARO_WINKLER_SIMILARITY(UPPER(p_mot_cle), UPPER(FORMATION_COURS)) as k
        FROM FORMATIONS;

    v_id_formation FORMATIONS.ID_FORMATION%TYPE;
        k integer;
    v_formation_cours FORMATIONS.FORMATION_COURS%TYPE;
BEGIN
    DBMS_OUTPUT.PUT_LINE('hehewjdhs');
    -- Ouvrir et parcourir le curseur
    OPEN cur_formation;

    -- Boucle FETCH pour afficher les résultats
    LOOP
        FETCH cur_formation INTO v_id_formation, v_formation_cours, k;
        EXIT WHEN cur_formation%NOTFOUND;

        -- Afficher les résultats
        DBMS_OUTPUT.PUT_LINE('ID_FORMATION: ' || v_id_formation);
        DBMS_OUTPUT.PUT_LINE('Formation_Cours: ' || v_formation_cours ); -- Limiter à 100 caractères
        DBMS_OUTPUT.PUT_LINE('SCORE: ' || k);
        DBMS_OUTPUT.PUT_LINE('-------------------------');
    END LOOP;

    -- Fermer le curseur
    CLOSE cur_formation;
END recherche_formation;
/

