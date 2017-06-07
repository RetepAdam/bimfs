SELECT n.* FROM nba_totals AS n JOIN dl_totals AS d ON n.player = d.player AND n.yr = d.yr AND n.age = d.age;

SELECT n.player, COUNT(DISTINCT n.yr) FROM nba_totals AS n JOIN dl_totals AS d ON n.player = d.player AND n.yr = d.yr AND n.age = d.age GROUP BY n.player ORDER BY n.player;
