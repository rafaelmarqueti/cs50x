SELECT m.title
  FROM movies m
  JOIN stars s
    ON s.movie_id = m.id
  JOIN people p
    ON p.id = s.person_id
 WHERE (p.name = 'Johnny Depp'
    OR p.name = 'Helena Bonham Carter')
 GROUP BY m.id
HAVING count(p.id) = 2
 ORDER BY m.id;