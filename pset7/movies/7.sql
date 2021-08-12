SELECT title, rating
  FROM movies m
  JOIN ratings r
    ON r.movie_id = m.id
 WHERE m.year = 2010
 ORDER BY rating DESC, title ASC;