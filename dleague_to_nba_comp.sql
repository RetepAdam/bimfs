CREATE TABLE nba_totals
(player TEXT, pos TEXT, age FLOAT, team TEXT, g INT, gs INT, mp FLOAT, m_fg INT, a_fg INT, p_fg FLOAT, m_3p INT, a_3p INT, p_3p FLOAT, m_2p INT, a_2p INT, p_2p FLOAT, p_efg FLOAT, ft_m INT, ft_a INT, ft_p FLOAT, orb INT, drb INT, trb INT, ast INT, stl INT, blk INT, tov INT, pf INT, pts INT, yr INT);

COPY nba_totals FROM '/Users/Peter/desktop/galvanize/bimfs/data/player_totals.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE dl_totals
(player TEXT, team TEXT, age FLOAT, g INT, gs INT, mp FLOAT, m_fg INT, a_fg INT, p_fg FLOAT, m_3p INT, a_3p INT, p_3p FLOAT, m_2p INT, a_2p INT, p_2p FLOAT, p_efg FLOAT, ft_m INT, ft_a INT, ft_p FLOAT, orb INT, drb INT, trb INT, ast INT, stl INT, blk INT, tov INT, pf INT, pts INT, yr INT);

COPY dl_totals FROM '/Users/Peter/desktop/galvanize/bimfs/data/player_NBADL_totals.csv' DELIMITER ',' CSV HEADER;
