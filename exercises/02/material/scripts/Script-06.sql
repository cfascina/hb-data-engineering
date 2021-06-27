CREATE TABLE tb_web_site AS (
	WITH cte_artist_first_time AS (
		SELECT b."date"
			,b."rank"
			,b.artist
			,row_number() OVER (
				PARTITION BY b.artist ORDER BY b.artist
					,b."date"
				) AS "row_number"
		FROM PUBLIC."Billboard" b
		ORDER BY b.artist, b."date"
		) SELECT cda."date"
	,cda."rank"
	,cda.artist FROM cte_artist_first_time AS cda WHERE cda."row_number" = 1
);
	
select count(1) from tb_web_site;

create table tb_artist as (
	SELECT b."date"
			,b."rank"
			,b.artist
			,b.song
		FROM PUBLIC."Billboard" b
		where b.artist = 'AC/DC'
		ORDER BY b.artist, b.song, b."date"
);

--drop table tb_artist;

select * from tb_artist;

create view vw_aft as (
	WITH cte_aft AS (
		select
			ta."date"
			,ta."rank"
			,ta.artist
			,row_number() OVER (
				PARTITION BY ta.artist ORDER BY ta.artist, ta."date"
			) AS "row_number"
			FROM tb_artist as ta 
			ORDER BY ta.artist, ta."date"
	)
	SELECT 
		aft."date"
		,aft."rank"
		,aft.artist FROM cte_aft AS aft WHERE aft."row_number" = 1
);

--drop view vw_aft;

select * from vw_aft;

insert into tb_artist (
	SELECT b."date"
			,b."rank"
			,b.artist
			,b.song
		FROM PUBLIC."Billboard" b
		where b.artist like 'Elvis%'
		ORDER BY b.artist, b.song, b."date"
);

select * from vw_aft;

create view vw_sft as (
	WITH cte_sft AS (
		select
			ta."date"
			,ta."rank"
			,ta.song 
			,row_number() OVER (
				PARTITION BY ta.artist, ta.song ORDER BY ta.artist, ta.song, ta."date"
			) AS "row_number"
			FROM tb_artist as ta 
			ORDER BY ta.artist, ta.song, ta."date"
	)
	SELECT 
		sft."date"
		,sft."rank"
		,sft.artist
		,sft.song 
	FROM cte_sft AS sft WHERE sft."row_number" = 1
);

select * from vw_sft;

insert into tb_artist (
	SELECT b."date"
			,b."rank"
			,b.artist
			,b.song
		FROM PUBLIC."Billboard" b
		where b.artist like 'Adele%'
		ORDER BY b.artist, b.song, b."date"
);

select * from vw_aft;
select * from vw_sft;

drop view vw_sft;

create or replace view vw_sft as (
	WITH cte_sft AS (
		select
			ta."date"
			,ta."rank"
			,ta.song 
			,row_number() OVER (PARTITION BY ta.song ORDER BY ta.song, ta."date") AS "row_number"
			FROM tb_artist as ta 
			ORDER BY ta.song, ta."date"
	)
	SELECT 
		sft."date"
		,sft."rank"
		,sft.song 
	FROM cte_sft AS sft WHERE sft."row_number" = 1
);

select * from vw_sft;
