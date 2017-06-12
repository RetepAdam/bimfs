# Galvanize DSI Capstone Project
### Goal
My goal is to break players down into collections of specific skills and then cluster them based on proficiency and then use the information gained from analyzing those clusters to measure/predict the effectiveness of lineups based on the player types involved and try to gauge how easily teams might be able to replace certain player archetypes. <br />

### References
Using cosine similarity to compare college prospects to NBA players: https://github.com/bernej/NBA-Draft-2017-Player-Comparison-Generator <br />
How Do NCAA Statistics Translate to the NBA?: http://basketball-statistics.com/howdoncaastatisticstranslatetothenba.html <br />
Predictions are Hard, Especially about Three Point Shooting: http://counting-the-baskets.typepad.com/my-blog/2014/09/prediction-are-hard-especially-about-three-point-shooting.html <br />
Determinants of NBA Player Salaries: http://thesportjournal.org/article/determinants-of-nba-player-salaries/ <br />

### Outline
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
FG% <br />
XGB: 0.277918393284 <br />
RF: 0.331002324825 <br />
Linear: 0.301271730086 <br />
OLS R2: 0.461564878761 <br />

2P% <br />
XGB: 0.0492092031499 <br />
RF: 0.234490087463 <br />
Linear: -0.0524030590275 <br />
OLS R2: 0.215660655293 <br />

3P% <br />
XGB: 0.323608132063 <br />
RF: 0.251868276008 <br />
Linear: 0.362539029147 <br />
OLS R2: 0.349651060921 <br />

FT% <br />
XGB: 0.239002800556 <br />
RF: 0.173869541818 <br />
Linear: -0.112468247057 <br />
OLS R2: 0.237034943436 <br />

eFG% <br />
XGB: 0.0746905244666 <br />
RF: 0.143307500877 <br />
Linear: 0.102052178243 <br />
OLS R2: 0.279358289102 <br />

FG/36 <br />
XGB: 0.205916405301 <br />
RF: 0.310713995463 <br />
Linear: 0.315636494847 <br />
OLS R2: 0.27582529054 <br />

FGA/36 <br />
XGB: 0.190805088731 <br />
RF: 0.250261704821 <br />
Linear: 0.360153907338 <br />
OLS R2: 0.310364146509 <br />

2P/36 <br />
XGB: 0.394955622197 <br />
RF: 0.404702242014 <br />
Linear: 0.372488251806 <br />
OLS R2: 0.42326713376 <br />

2PA/36 <br />
XGB: 0.276024932285 <br />
RF: 0.32848209916 <br />
Linear: 0.260658676098 <br />
OLS R2: 0.375118882183 <br />

3P/36 <br />
XGB: 0.551778169988 <br />
RF: 0.570499392693 <br />
Linear: 0.609233095001 <br />
OLS R2: <strong>0.666265110472</strong> <br />

3PA/36 <br />
XGB: 0.506029809777 <br />
RF: 0.540593236001 <br />
Linear: 0.548663117427 <br />
OLS R2: <strong>0.661021266751</strong> <br />

FT/36 <br />
XGB: -0.162126297385 <br />
RF: -0.248540786327 <br />
Linear: -0.292280592641 <br />
OLS R2: 0.166380256555 <br />

FTA/36 <br />
XGB: -0.07062224559 <br />
RF: -0.0862557355467 <br />
Linear: -0.105017906081 <br />
OLS R2: 0.220135305459 <br />

ORB/36 <br />
XGB: 0.643865200891 <br />
RF: 0.65324329811 <br />
Linear: 0.614267470364 <br />
OLS R2: <strong>0.702508138322</strong> <br />

DRB/36 <br />
XGB: 0.65746464092160473 <br />
RF: 0.61195244994 <br />
Linear: 0.650972682479 <br />
OLS R2: <strong>0.677409522905</strong> <br />

TRB/36 <br />
XGB: 0.74905353563572674 <br />
RF: 0.704125368806 <br />
Linear: 0.738194909152 <br />
OLS R2: <strong>0.770250786813</strong> <br />

AST/36 <br />
XGB: 0.692624450409 <br />
RF: 0.646250455571 <br />
Linear: 0.627395684621 <br />
OLS R2: <strong>0.673976267069</strong> <br />

STL/36 <br />
XGB: 0.238584337343 <br />
RF: 0.276704392605 <br />
Linear: 0.0677439046654 <br />
OLS R2: 0.40525647905 <br />

BLK/36 <br />
XGB: 0.693912740706 <br />
RF: 0.640056993721 <br />
Linear: 0.603397791923 <br />
OLS R2: <strong>0.71778489302</strong> <br />

TOV/36 <br />
XGB: 0.261822596021 <br />
RF: 0.280506018469 <br />
Linear: 0.047958879389 <br />
OLS R2: 0.348854640011 <br />

PF/36 <br />
XGB: 0.255267195781 <br />
RF: 0.344897763958 <br />
Linear: 0.158769584323 <br />
OLS R2: 0.383640324989 <br />

PTS/36 <br />
XGB: 0.0648422939816 <br />
RF: 0.220222314281 <br />
Linear: 0.252679257239 <br />
OLS R2: 0.214701674064 <br />

TS% <br />
XGB: 0.210364731606 <br />
RF: 0.207551275517 <br />
Linear: 0.041475439805 <br />
OLS R2: 0.235686527845 <br />

FTr <br />
XGB: 0.185349262179 <br />
RF: 0.255148923744 <br />
Linear: 0.0743561365622 <br />
OLS R2: 0.36785770657 <br />

3PAr <br />
XGB: 0.478243736117 <br />
RF: 0.553298237326 <br />
Linear: 0.519841808623 <br />
OLS R2: <strong>0.669128922823</strong> <br />

The Adjusted R2s range from 0.166 (FT/36) to 0.770 (TRB/36). With the relatively limited sample sizes I'm working off of, I'm careful not to place too much stock in the Random Forest & Linear Regression accuracy scores, since this can be pretty wildly variable depending on the train/test split (which I have been keeping static). However, the name of the game is prediction, so the goal is to increase the consistency of the model, which may just come down to being able to increase the sample space without introducing more noise.


By adjusting feature space to eliminate extraneous features, able to improve Adj. R2...

3P%: .350 --> .396
[10, 13, 14, 19, 20, 22, 24, 26, 27, 30, 33, 34, 35, 37, 43, 47, 48, 50, 51, 53, 54, 55, 59, 60, 61, 62, 63]

TRB/36: .770 --> .787
[10, 15, 16, 22, 23, 25, 27, 33, 35, 36, 37, 40, 41, 42, 44, 45, 46, 47, 48, 50, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62]

BLK/36: .718 --> .746
[3, 6, 7, 8, 16, 40, 41, 51, 53, 56, 60, 61, 62]

FT%: .238 --> .282
[2, 9, 10, 14, 16, 19, 28, 29, 32, 34, 37, 38, 39, 40, 41, 44, 45, 50, 51, 53, 55, 57, 58, 60]

3PAr: .669 --> .691
[6, 7, 9, 10, 13, 14, 17, 19, 23, 25, 26, 27, 30, 33, 34, 36, 38, 39, 48, 49, 51, 52, 53, 56, 57]
