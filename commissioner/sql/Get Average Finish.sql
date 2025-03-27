-- Active: 1740417427513@@127.0.0.1@5432@beer_me@public
select
	driver.name,
	-- raceresult.finish_pos,
	round(avg(raceresult.start_pos),1) avg_start,
	round(avg(finish_pos),1) avg_finish,
	count(*) as "races",
	team.name,
	raceresult.manufacturer,
	track.name track_name
	-- ,race.road_course
from
	commissioner_driver driver,
	commissioner_raceresult raceresult,
	commissioner_race race,
	commissioner_team team,
	commissioner_track track
where
	-- raceresult.finish_pos <= 10
	raceresult.race_id = race.id
	-- and race.race_date = '2024-04-07'
	and race.track_id = track.id 
	and raceresult.driver_id = driver.id
	and team.id = driver.team_id
	and track.id = 27
	-- and "races" > 2
	-- and raceresult.finish_pos > 5
GROUP BY
	driver.name,
	-- race.race_date,
	team.name,
	raceresult.manufacturer,
	track.name
	-- ,race.road_course
	-- start_pos,
	-- finish_pos
ORDER BY
	avg_finish, avg_start
