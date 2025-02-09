create FUNCTION METAPHONE(p_input VARCHAR2) RETURN VARCHAR2 IS
    l_result VARCHAR2(4000); -- Résultat final
BEGIN
    -- Vérifier si l'entrée est NULL
    IF p_input IS NULL THEN
        RETURN NULL;
    END IF;

    -- Convertir en majuscules pour un traitement uniforme
    l_result := UPPER(p_input);

    -- Suppression des caractères non alphabétiques
    l_result := REGEXP_REPLACE(l_result, '[^A-Z]', '');

    -- Règles de transformation phonétique
    l_result := REPLACE(l_result, 'PH', 'F');
    l_result := REPLACE(l_result, 'GH', 'G');
    l_result := REPLACE(l_result, 'KN', 'N');
    l_result := REPLACE(l_result, 'GN', 'N');
    l_result := REPLACE(l_result, 'WR', 'R');
    l_result := REPLACE(l_result, 'WH', 'W');
    l_result := REPLACE(l_result, 'QU', 'Q');

    -- Remplacements pour les voyelles
    l_result := REPLACE(l_result, 'A', '');
    l_result := REPLACE(l_result, 'E', '');
    l_result := REPLACE(l_result, 'I', '');
    l_result := REPLACE(l_result, 'O', '');
    l_result := REPLACE(l_result, 'U', '');
    l_result := REPLACE(l_result, 'Y', '');

    -- Simplifications supplémentaires
    l_result := REGEXP_REPLACE(l_result, 'CH', 'X'); -- Simplifier 'CH'
    l_result := REGEXP_REPLACE(l_result, 'SCH', 'S'); -- Simplifier 'SCH'
    l_result := REGEXP_REPLACE(l_result, '[^A-Z]', ''); -- Supprimer tout autre caractère non alphabétique

    -- Gérer les cas où le résultat est vide ou NULL après traitement
    IF l_result IS NULL OR l_result = '' THEN
        RETURN 'X'; -- Retour par défaut
    END IF;

    RETURN l_result;
END;
/

