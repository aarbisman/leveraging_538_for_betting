def get_dicts():
    name_to_abr = {"Diamondbacks":"ARI",\
               "Braves":"ATL",\
               "Orioles":"BAL",\
               "Red Sox":"BOS",
               "Cubs":"CHC",\
               "White Sox":"CHW",
               "Reds":"CIN",\
               "Indians":"CLE",
               "Rockies":"COL",\
               "Tigers":"DET",
               "Marlins":"MIA",\
               "Astros":"HOU",
               "Royals":"KCR",\
               "Angels":"LAA",
               "Dodgers":"LAD",\
               "Brewers":"MIL",    
               "Twins":"MIN",    
               "Mets":"NYM",\
               "Yankees":"NYY",\
               "Athletics":"OAK",\
               "Phillies":"PHI",\
               "Pirates":"PIT",\
               "Padres":"SDP",\
               "Giants":"SFG",\
               "Mariners":"SEA",\
               "Cardinals":"STL",\
               "Rays":"TBR",\
               "Rangers":"TEX",\
               "Blue Jays":"TOR",\
               "Nationals":"WSH"}
    
    abr_to_id = {
    "ARI":1,\
    "ATL":2,\
    "BAL":3,\
    "BOS":4,\
    "CHC":5,\
    "CHW":6,\
    "CIN":7,\
    "CLE":8,\
    "COL":9,\
    "DET":10,\
    "MIA":11,\
    "HOU":12,\
    "KCR":13,\
    "LAA":14,\
    "LAD":15,\
    "MIL":16,\
    "MIN":17,\
    "NYM":18,\
    "NYY":19,\
    "OAK":20,\
    "PHI":21,\
    "PIT":22,\
    "SDP":23,\
    "SFG":24,\
    "SEA":25,\
    "STL":26,\
    "TBR":27,\
    "TEX":28,\
    "TOR":29,\
    "WSH":30}
    
    return name_to_abr, abr_to_id