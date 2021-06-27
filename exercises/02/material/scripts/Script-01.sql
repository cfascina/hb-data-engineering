create table public."Billboard" (
	 "date" date null,
	 "rank" int4 null,
	 song varchar(300) null,
	 artist varchar(300) null,
	 "last-week" int4 null,
	 "peak-rank" int4 null,
	 "weeks-on-board" int4 null
);

--327K
select count(1) from public."Billboard";

select 
	b.artist
	,b.song
	,count(*) as "#"
from public."Billboard" b 
where b.artist = 'Chuck Berry'
group by b.artist, b.song
order by "#" desc;

select 
	b.artist
	,b.song
	,count(*) as "#"
from public."Billboard" b 
where 
	b.artist in ('Chuck Berry', 'Frankie Vaughan')
group by b.artist, b.song
order by "#" desc;
