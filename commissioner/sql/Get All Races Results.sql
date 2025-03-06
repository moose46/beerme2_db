SELECT * FROM public.commissioner_raceresult rr, public.commissioner_driver driver
where rr.driver_id = driver.id
ORDER BY id ASC 