-- Active: 1740417427513@@127.0.0.1@5432@beer_me@public
select
	driver.name,
	avg(finish_pos) avg_finish,
	count(*),
	team.name
from
	commissioner_driver driver,
	commissioner_raceresult raceresult,
	commissioner_race race,
	commissioner_team team
where
	driver.id = raceresult.driver_id
	and raceresult.finish_pos > 2
	and race.race_date > '2025-01-01',
	and team.id = driver.team_id
GROUP BY
	driver.name, team.name
ORDER BY
	avg_finish