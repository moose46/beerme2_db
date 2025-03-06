SELECT race.name, driver.name,rr.finish_pos, race.race_date
FROM public.commissioner_raceresult rr, public.commissioner_driver driver, public.commissioner_race race
where rr.driver_id = driver.id and rr.race_id = race.id and race_date = '2024-03-10'
ORDER BY rr.id ASC 