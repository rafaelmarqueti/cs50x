SELECT name
  FROM people p
  JOIN stars s
    ON s.person_id = p.id
  JOIN movies m
    ON s.movie_id = m.id
 WHERE m.year = 2004
 GROUP BY p.id
 ORDER BY p.birth;