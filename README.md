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
2. My goal is to determine the fungibility of specific skills. In other words, how easily are teams able to replace certain specific skills. In order to do this, I will build a model that would be able to forecast NBA performance by specific skill based on statistics from their previous league. e.g. Can you find strong rebounders pretty cheaply and easily via the D-League or international leagues, or do you have to invest significantly dra  capital to acquire those guys?
3. After creating the model, the next step will be to determine how much teams routinely spend for each specific skill on the open market by modeling salary against performance in each skill area.

### Data Collection

The entirety of the information used to build the initial model has been scraped from Basketball-Reference.com and Sports-Reference.com. I also been sent TPA (Total Points Added) metric data from Adam Fromal of NBA-Math, which I will use to assist in generalized defensive modeling outside of simple box score projection.

### Data Prep

Most of the data came packaged the way I needed it, but I did have to do some minor feature engineering to account for playing time. For college players, I added stats per 40 minutes. For NBA players, I used stats per 36. In order to get college career data compiled, I took individual seasons and summed the raw stats while taking weighted averages for cumulative metrics like PER and BPM. Since the scraped NBA data did not have any identifying features to resolve situations where there were duplicate names (in addition to some players having transferred), I relied on comparing final college season to first NBA season to make sure I was looking at the right player, and in the cases of multiple players with the same names, resolved a handful of issues manually by simply checking their Sports-Reference page and seeing if it was linked to an NBA-level Basketball-Reference page. There were maybe 10-15 of these that needed resolving.

### Data Analysis

So far, I have been using the OLS Summary and Random Forest feature importances to determine which features are creating the bulk of the signal for each individual category, with the strongest single statistic translation by far (so far) being BLK/40 to BLK/36. <br />
<br />
I've found that increasing a minutes threshold for the NBA level (100, 150, 500, 1000 minutes, etc.) has helped improve signal, but I don't want to lose out on sample size by setting higher standards (plus, there will be a little bit of survivorship bias), so two ways that I may be able to increase my sample space are to revise my NBA pool to players in their first season of playing a certain number of minutes rather than outright rookie year. This is justifiable since some of the rookies in the pool anyway are overaged, having taken the long way around to the NBA. The other way would be to simply have my college data go even futher back. The biggest issue with this is that Minutes Played data only goes back reliably to 2009-10, so I will be unable to engineer the per-minute features for some players, and many of those rank highly in importance. However, I could potentially get around this issue by just dropping players for whom that type of feature engineering is not possible. Without knowing the reasons behind why or why not a player's minutes would have been tracked (perhaps major conference players have their minutes data listed while minor conference players don't?), it's hard to know whether or not this may introduce an element of bias to the analysis, but a larger sample space would likely be worth what is probably a very minor trade-off. At the very least, if that separation can be recognized, I could split the model along those lines if need be.

### Model Selection

Initially, to get a solid baseline, I have been using Linear Regression and Random Forest, plus feeding in all the data to get a sense of the basic OLS Adjusted R2 for each statistical category. <br />
<br />
The Adjusted R2s range from 0.166 (FT/36) to 0.770 (TRB/36). With the relatively limited sample sizes I'm working off of, I'm careful not to place too much stock in the Random Forest & Linear Regression accuracy scores, since this can be pretty wildly variable depending on the train/test split (which I have been keeping static). However, the name of the game is prediction, so the goal is to increase the consistency of the model, which may just come down to being able to increase the sample space without introducing more noise.
