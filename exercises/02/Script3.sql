WITH cte_artist
AS (
	SELECT b.artist
		,count(1) AS "qty_artist"
	FROM PUBLIC."Billboard" b
	GROUP BY b.artist
	ORDER BY b.artist DESC
	)
	,cte_song
AS (
	SELECT b.song
		,count(1) AS "qty_song"
	FROM PUBLIC."Billboard" b
	GROUP BY b.song
	ORDER BY b.song DESC
	)
SELECT DISTINCT b1.artist
	,b2.qty_artist
	,b1.song
	,b3.qty_song
FROM PUBLIC."Billboard" b1
LEFT JOIN cte_artist AS b2 ON (b1.artist = b2.artist)
LEFT JOIN cte_song AS b3 ON (b1.song = b3.song)
ORDER BY b1.artist
	,b1.song;