WITH cte_billboard
AS (
	SELECT DISTINCT b.artist
		,b.song
	FROM PUBLIC."Billboard" b
	ORDER BY b.artist
		,b.song
	)
SELECT *
	,row_number() OVER (
		ORDER BY artist
			,song
		) AS "row_number"
	,row_number() OVER (PARTITION BY artist) AS "row_number_artist"
	,rank() OVER (
		PARTITION BY artist ORDER BY artist
			,song
		) AS "rank"
	,lag(song, 1) OVER (
		PARTITION BY artist ORDER BY artist
			,song
		) AS "lag_song"
	,lead(song, 1) OVER (
		PARTITION BY artist ORDER BY artist
			,song
		) AS "lead_song"
	,first_value(song) OVER (
		PARTITION BY artist ORDER BY artist
			,song
		) AS "first_song"
	,last_value(song) OVER (
		PARTITION BY artist ORDER BY artist
			,song range BETWEEN unbounded preceding
				AND unbounded following
		) AS "last_song"
FROM cte_billboard;