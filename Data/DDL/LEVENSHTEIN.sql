create FUNCTION levenshtein(s1 IN VARCHAR2, s2 IN VARCHAR2) RETURN NUMBER IS
    TYPE t_arr IS TABLE OF NUMBER INDEX BY BINARY_INTEGER;
    v_cost      NUMBER;
    v_len_s1    NUMBER := LENGTH(s1);
    v_len_s2    NUMBER := LENGTH(s2);
    v_matrix    t_arr;
BEGIN
    IF v_len_s1 = 0 THEN
        RETURN v_len_s2;
    ELSIF v_len_s2 = 0 THEN
        RETURN v_len_s1;
    END IF;

    -- Initialiser la matrice
    FOR i IN 0..v_len_s1 LOOP
        v_matrix(i) := i;
    END LOOP;

    FOR j IN 1..v_len_s2 LOOP
        v_matrix(0) := j;
        FOR i IN 1..v_len_s1 LOOP
            v_cost := CASE WHEN SUBSTR(s1, i, 1) = SUBSTR(s2, j, 1) THEN 0 ELSE 1 END;
            v_matrix(i) := LEAST(v_matrix(i - 1) + 1,  -- Suppression
                                 v_matrix(i) + 1,    -- Insertion
                                 v_matrix(i - 1) + v_cost); -- Substitution
        END LOOP;
    END LOOP;

    RETURN v_matrix(v_len_s1);
END;
/

