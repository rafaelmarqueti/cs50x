SELECT name
  FROM people p
  JOIN stars s
    ON s.person_id = p.id
 WHERE s.movie_id IN (
    SELECT movie_id
      FROM stars s
      JOIN people p
        ON p.id = s.person_id
    WHERE p.name = 'Kevin Bacon'
      AND p.birth = 1958
 ) AND NOT name = 'Kevin Bacon';