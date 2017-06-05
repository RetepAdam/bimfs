# Galvanize DSI Capstone Project

Timeline: <br />
5/22/17 - Began constructing bball_ref scrapers. Grabbed basketballCrawler but may not be useful.<br />
5/23/17 - Finished scrapers and merged into one file.<br />
6/2/17 - Created lineup data scraper.<br />
6/3/17 - Scraped all 5-man lineup data.<br />

GOAL: <br />
My goal is to break players down into collections of specific skills and then cluster them based on proficiency and then use the information gained from analyzing those clusters to measure/predict the effectiveness of lineups based on the player types involved and try to gauge how easily teams might be able to replace certain player archetypes. <br />

REFERENCES: <br />
Using cosine similarity to compare college prospects to NBA players: https://github.com/bernej/NBA-Draft-2017-Player-Comparison-Generator <br />
From 5 to 13: Redefining the Positions in Basketball: http://www.sloansportsconference.com/content/the-13-nba-positions-using-topology-to-identify-the-different-types-of-players/ <br />
A cluster analysis of NBA players: http://www.sloansportsconference.com/wp-content/uploads/2012/02/44-Lutz_cluster_analysis_NBA.pdf <br />
Justin Willard's study on positional clustering (will be able to use him as a resource): http://fansided.com/2015/09/29/nba-positions-by-clustering/ <br />

OUTLINE: <br />
1. Scrape basketball-reference (already done) and other sites like NBA.com/stats, nbawowy and Synergy (as necessary) to aggregate stats/metrics required to adequately reflect specific player skills. basketball-reference should get most of it done, but NBA stats and Synergy might be more useful for shooting splits.
2. Use hierarchical (seems better suited, given the task) or K-means (eh) clustering to group players based on proficiency for each skill.
3. Here’s where I have a few different ideas. The simplest way to proceed from there would probably be to plug the clustering into lineup data (from basketball-reference or nbawowy) to evaluate lineup configurations, determine how teams deploy combinations of skill sets and see if any particular combinations routinely outperform the others.
4. Having accomplished that, the next thing I would want to look at would be fungibility of specific skills. In other words, how easily are teams able to replace a member of a given cluster. I could probably just tackle this by seeing where players of each type come from and calling it a day, but if I really want to dive into it (and I do, if I have enough time), it would be prudent to try to build a model that would be able to forecast NBA performance by specific skill based on statistics from their previous league. e.g. Can you find strong rebounders pretty cheaply and easily via the D-League or international leagues, or do you have to invest significantly dra  capital to acquire those guys? This could probably be its own Capstone project, but given that it’s somewhat built on the framework provided above and I’d probably need to tinker around with it for a while, I’m not sure I’d want to have this as the headlining component of mine unless I know I have it right.
5. Another thing I ought to be able to do (and a lot more easily than the last bit) is if the lineup analysis reveals anything interesting, I should be able to turn around and do something straightforward like put together a list of free agents the Nuggets ought to target this summer. Can’t hurt, right?
