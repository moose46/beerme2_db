WITH
	WINNER AS (
		SELECT
			FINISH_POS AS FINISH_POS_WINNER,
			BET.RACE_ID,
			PLAYER_ID
		FROM
			COMMISSIONER_RACERESULT RACERESULT,
			COMMISSIONER_BET BET
		WHERE
			BET.DRIVER_ID = RACERESULT.DRIVER_ID
			AND BET.RACE_ID = RACERESULT.RACE_ID
			AND FINISH_POS = (
				SELECT
					MIN(FINISH_POS)
				FROM
					COMMISSIONER_RACERESULT R,
					COMMISSIONER_BET B
				WHERE
					B.RACE_ID = R.RACE_ID
					AND R.DRIVER_ID = B.DRIVER_ID
					AND RACERESULT.RACE_ID = B.RACE_ID
			)
		GROUP BY
			1,
			2,
			3
	),
	LOOSER AS (
		SELECT
			FINISH_POS AS FINISH_POS_LOOSER,
			BET.RACE_ID,
			PLAYER_ID
		FROM
			COMMISSIONER_RACERESULT RACERESULT,
			COMMISSIONER_BET BET
		WHERE
			BET.DRIVER_ID = RACERESULT.DRIVER_ID
			AND BET.RACE_ID = RACERESULT.RACE_ID
			AND FINISH_POS = (
				SELECT
					MAX(FINISH_POS)
				FROM
					COMMISSIONER_RACERESULT R,
					COMMISSIONER_BET B
				WHERE
					B.RACE_ID = R.RACE_ID
					AND R.DRIVER_ID = B.DRIVER_ID
					AND RACERESULT.RACE_ID = B.RACE_ID
			)
		GROUP BY
			1,
			2,
			3
	)
SELECT player.name,
	SUM(WINNER.PLAYER_ID),
	SUM(LOOSER.PLAYER_ID)
FROM
	WINNER,
	LOOSER, commissioner_player player
WHERE
	WINNER.RACE_ID = PLAYER.ID
	AND LOOSER.PLAYER_ID != PLAYER.ID
	group by 1
	-- AND WINNER.DRIVER_ID != LOOSER.DRIVER_ID