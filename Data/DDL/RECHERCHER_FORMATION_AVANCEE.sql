create PROCEDURE rechercher_formation_avancee(
    p_chaine VARCHAR2,         -- Input search keyword
    p_offset NUMBER DEFAULT 0, -- Pagination offset
    p_limit NUMBER DEFAULT 10, -- Pagination limit
    p_result OUT SYS_REFCURSOR -- Output cursor
) AS
    v_tokens SYS.ODCIVARCHAR2LIST; -- Tokenized words from input
    v_regex_pattern VARCHAR2(4000); -- Regex for unordered word matching
BEGIN
    -- Tokenize input into individual words
    SELECT CAST(COLLECT(REGEXP_SUBSTR(p_chaine, '[^ ]+', 1, LEVEL)) AS SYS.ODCIVARCHAR2LIST)
    INTO v_tokens
    FROM DUAL
    CONNECT BY REGEXP_SUBSTR(p_chaine, '[^ ]+', 1, LEVEL) IS NOT NULL;

    -- Generate a regex pattern for unordered word matching
    SELECT '.' || LISTAGG(COLUMN_VALUE, '.') WITHIN GROUP (ORDER BY COLUMN_VALUE) || '.*'
    INTO v_regex_pattern
    FROM TABLE(v_tokens);

    -- Open a cursor to perform the robust search
    OPEN p_result FOR
    WITH RankedResults AS (
        SELECT
            ID_FORMATION,
            DOMAINE_CATGEGORIE,
            SOUS_DOMAINE_CATEGORIE,
            FORMATION_COURS,
            KEYWORDS,
            -- Relevance scoring
            CASE
                WHEN LOWER(FORMATION_COURS) = LOWER(p_chaine) THEN 100  -- Exact match on course name
                WHEN LOWER(DOMAINE_CATGEGORIE) = LOWER(p_chaine) THEN 90 -- Exact match in domain
                WHEN LOWER(SOUS_DOMAINE_CATEGORIE) = LOWER(p_chaine) THEN 80 -- Exact match in subdomain
                WHEN LOWER(FORMATION_COURS) LIKE '%' || LOWER(p_chaine) || '%' THEN 70 -- Partial match
                WHEN REGEXP_LIKE(LOWER(FORMATION_COURS), LOWER(v_regex_pattern)) THEN 65 -- Unordered word matching
                WHEN EXISTS (
                    SELECT 1 FROM TABLE(v_tokens)
                    WHERE LOWER(FORMATION_COURS) LIKE '%' || LOWER(COLUMN_VALUE) || '%'
                ) THEN 60 -- Token-based partial matching
                WHEN UTL_MATCH.EDIT_DISTANCE_SIMILARITY(LOWER(FORMATION_COURS), LOWER(p_chaine)) > 85 THEN 50 -- Typo handling
                WHEN metaphone(FORMATION_COURS) = metaphone(p_chaine) THEN 40  -- Phonetic similarity
                WHEN LOWER(KEYWORDS) LIKE '%' || LOWER(p_chaine) || '%' THEN 30 -- Match in keywords
                ELSE 0  -- Default relevance
            END AS pertinence
        FROM formations
        WHERE 
            LOWER(FORMATION_COURS) LIKE '%' || LOWER(p_chaine) || '%'
            OR REGEXP_LIKE(LOWER(FORMATION_COURS), LOWER(v_regex_pattern))
            OR EXISTS (
                SELECT 1 FROM TABLE(v_tokens)
                WHERE LOWER(FORMATION_COURS) LIKE '%' || LOWER(COLUMN_VALUE) || '%'
            )
            OR UTL_MATCH.EDIT_DISTANCE_SIMILARITY(LOWER(FORMATION_COURS), LOWER(p_chaine)) > 60
            OR metaphone(FORMATION_COURS) = metaphone(p_chaine)
            OR LOWER(KEYWORDS) LIKE '%' || LOWER(p_chaine) || '%'
    )
    SELECT ID_FORMATION, DOMAINE_CATGEGORIE, SOUS_DOMAINE_CATEGORIE, FORMATION_COURS, KEYWORDS
    FROM RankedResults
    ORDER BY pertinence DESC, ID_FORMATION
    OFFSET p_offset ROWS FETCH NEXT p_limit ROWS ONLY;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No results found for search: ' || p_chaine);
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error occurred: ' || SQLERRM);
END;
/

