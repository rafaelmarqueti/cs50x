SELECT name
  FROM people p
  JOIN directors d
    ON d.person_id = p.id
  JOIN movies m
    ON d.movie_id = m.id
  JOIN ratings r
     ON r.movie_id = m.id
 WHERE r.rating >= 9.0
 ORDER BY p.birth;