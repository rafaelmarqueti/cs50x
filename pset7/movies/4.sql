SELECT count(*)
  FROM movies m
  JOIN ratings r
    ON r.movie_id = m.id
 WHERE r.rating = 10.0;