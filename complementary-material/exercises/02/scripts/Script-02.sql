SELECT DISTINCT b.artist
	,b.song
FROM PUBLIC."Billboard" b
ORDER BY b.artist
	,b.song;

SELECT b.artist
	,count(1) AS "#"
FROM PUBLIC."Billboard" b
GROUP BY b.artist
ORDER BY "#" DESC;

SELECT b.song
	,count(1) AS "#"
FROM PUBLIC."Billboard" b
GROUP BY b.song
ORDER BY "#" DESC;

SELECT DISTINCT b1.artist
	,b2.qty_artist
	,b1.song
	,b3.qty_song
FROM PUBLIC."Billboard" b1
LEFT JOIN (
	SELECT b.artist
		,count(1) AS "qty_artist"
	FROM PUBLIC."Billboard" b
	GROUP BY b.artist
	) b2 ON (b1.artist = b2.artist)
LEFT JOIN (
	SELECT b.song
		,count(1) AS "qty_song"
	FROM PUBLIC."Billboard" b
	GROUP BY b.song
	) b3 ON (b1.song = b3.song)
ORDER BY b1.artist
	,b1.song;