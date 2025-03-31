-- Active: 1740417427513@@127.0.0.1@5432@beer_me@public
SELECT
	DRIVER.NAME,
	-- raceresult.finish_pos,
	ROUND(AVG(RACERESULT.START_POS), 1) AVG_START,
	ROUND(AVG(FINISH_POS), 1) AVG_FINISH,
	COUNT(*) AS "races",
	cast(DRIVER.SALARY as money),
	-- finish_pos,
	-- select count(*) from raceresult where race_id = 9 and finish_pos = 1 and raceresult.driver_id = 1 as wins
	TEAM.NAME,
	RACERESULT.MANUFACTURER
	,TRACK.NAME TRACK_NAME
	-- ,race.road_course
FROM
	COMMISSIONER_DRIVER DRIVER,
	COMMISSIONER_RACERESULT RACERESULT,
	COMMISSIONER_RACE RACE,
	COMMISSIONER_TEAM TEAM,
	COMMISSIONER_TRACK TRACK
WHERE
	-- raceresult.finish_pos <= 10
	RACERESULT.RACE_ID = RACE.ID
	-- and race.race_date = '2025-03-30'
	AND RACE.TRACK_ID = TRACK.ID
	AND RACERESULT.DRIVER_ID = DRIVER.ID
	AND TEAM.ID = DRIVER.TEAM_ID
	AND TRACK.ID = 7
	-- and raceresult.finish_pos
	-- and "races" > 2
	-- AND RACERESULT.FINISH_POS <= 10
GROUP BY
	DRIVER.NAME,
	-- race.race_date,
	TEAM.NAME,
	RACERESULT.MANUFACTURER,
	TRACK.NAME,
	SALARY
	-- ,race.road_course
	-- start_pos,
	-- finish_pos
ORDER BY
	AVG_FINISH,
	AVG_START