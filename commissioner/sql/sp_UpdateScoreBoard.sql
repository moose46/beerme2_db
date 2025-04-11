CREATE
OR REPLACE PROCEDURE UPDATEDATESCOREBOARD () LANGUAGE PLPGSQL AS $$
declare
bets RECORD;
begin
		raise notice 'Boo!';
		for bets in
		select
			BET.ID as bet_id,
			FINISH_POS,
			BET.RACE_ID,
			BET.PLAYER_ID
		FROM
			COMMISSIONER_RACERESULT RACERESULTS,
			COMMISSIONER_BET BET
		WHERE
			BET.DRIVER_ID = RACERESULTS.DRIVER_ID
			AND BET.RACE_ID = RACERESULTS.RACE_ID
			AND FINISH_POS = (
				SELECT
					MIN(FINISH_POS)
				FROM
					COMMISSIONER_RACERESULT R,
					COMMISSIONER_BET B
				WHERE
					B.RACE_ID = R.RACE_ID
					AND R.DRIVER_ID = B.DRIVER_ID
					AND RACERESULTS.RACE_ID = B.RACE_ID
			)
		GROUP BY
			1,
			2,
			3,
			4
			loop
			raise notice 'bet_id=%, finish_pos=%, race_id=%, player_id=%',bets.bet_id, bets.finish_pos, bets.race_id, bets.player_id;
			end loop;
			raise notice 'Boo Hoo!';
end;$$