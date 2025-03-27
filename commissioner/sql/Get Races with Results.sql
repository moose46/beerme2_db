select
	track.name,
	race_date
from
	commissioner_race race,
	commissioner_raceresult results,
	commissioner_track track
where
	race.track_id = track.id and
	race.id not in (
		select
			race_id
		from
			commissioner_raceresult results
		where
			results.race_id = race.id
	)
	and race.race_date <= now()
group by
	track.name,
	race_date
order by race.race_date desc