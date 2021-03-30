import csv
list_of_recipe_id = [46,115,118,150,153,154,167,170,242,243,325,355,356,429,436,472,496,504,508,524,547,557,570,585,614,632,638,647,653,661,824,825,1236,1317,1320,1420,1557,1712,1823,1883,1923,2056,2155,2284,2325,2518,2540,2561,2684,2712,2866,2923,2945,2994,3161,3165,3211,3225,3242,3254,3258,3326,3328,3347,3371,3441,3496,3572,3667,3689,3729,3739,3748,3776,3779,3788,3801,3805,3806,3838,3871,3900,3910,3925,4028,4044,4133,4157,4205,4297,4344,4345,4395,4407,4478,4489,4527,4528,4533,4563,4570,4588,4764,4779,4838,4880,4966,5008,5025,5030,5060,5174,5178,5179,5197,5234,5270,5276,5289,5293,5455,8448,8470,8476,8488,8548,8559,8562,8565,8584,8606,8674,8827,8842,8975,9305,9684,9686,9803,9858,9875,9913,10627,10829,11040,11127,11164,11179,11324,11361,11384,11427,11512,12252,12496,12539,12557,12601,12672,12737,12997,13341,13586,14216,14499,14742,14949,15202,15209,15211,15487,15869,16364,16391,16451,16736,16856,17382,17831,17963,18067,18095,18224,18307,18373,18394,18398,18465,18476,19104,19618,19627,19631,19897,20143,20324,20537,20680,20688,20800,20823,20981,21025,21132,21176,21227,21302,21339,21395,21570,21691,21816,21859,21926,22059,22224,22290,22320,22322,22337,22363,22442,22482,22637,22642,22742,22949,23303,23353,23423,23431,23498,23499,23561,23757,23771,23850,23932,24017,24193,24307,24414,24447,24503,24516,24549,24572,24631,24636,24657,24678,24701,24959,25259,25744,25837,26263,26768,26791,27005,27485,28215,28356,28385,28497,28545,28731,28848,28880,28937,28945,29106,29137,29172,29550,29835,29939,29977,30198,30300,30473,30706,30775,30780,30910,30978,31008,31146,31587,31748,31777,32001,32361,32459,32772,33081,33141,33149,33166,33167,33452,33561,34012,34244,34264,35014,35018,35595,35632,35653,35788,35800,36009,36107,36244,36247,36434,36482,36636,36675,36748,36796,36839,37073,37090,37152,37225,37279,37313,37401,37725,38039,38216,38240,38374,38404,38607,38798,38811,38812,38856,39136,39338,39571,39642,39705,40204,40228,40306,40358,40478,40658,40788,40800,40804,40858,40865,40918,41018,41180,41452,41953,41954,42043,42068,42070,42072,42570,42745,43424,44141,45017,45120,45530,46022,46417,46553,46571,46921,46973,46982,47444,47691,48156,48279,48296,48997,49023,50259,50431,51947,52080,52443,52448,52495,52574,53940,54025,54356,54447,54932,54989,55263,55364,55437,57251,57857,59046,59310,60453,60780,63469,63915,64162,64336,64652,64784,65041,65936,66559,66853,67415,67577,67693,69168,69309,70134,70590,70878,70890,70919,71046,71797,71833,71998,72049,72065,72600,72606,72905,73570,73685,73687,74157,76887,76915,77203,77976,79826,79944,80022,80100,80165,80767,82108,84068,84124,84274,84797,84801,87802,88418,88537,89121,89507,90092,91938,92877,93073,93093,93908,94153,95158,95355,95640,95821,96282,97155,98268,98464,99020,100892,101260,101264,102864,103406,106299,106545,107851,107852,109428,109793,111045,111487,113458,114022,116376,116672,117716,117758,118667,119084,119632,120377,120783,121154,121156,122613,122615,122780,122915,123540,123542,123900,124174,124641,126833,128389,128450,130766,134453,135216,136330,137010,138406,138500,138842,139399,139407,140850,142309,144175,144958,148927,151367,153430,157276,157287,157880,160310,162801,164178,164290,165096,173937,176593,179945,184356,192887,196210,197091,211510,218390,239958,243092,248572,255098,260956,287051,295063,298029,304171,307887,317798,343461,344278,392262,416887]
print(len(list_of_recipe_id))

#Copy all the csv value into a new file
raw_recipe = "/Users/xinruzou/Downloads/archive/RAW_recipes.csv"

pp_recipe_new = "new_recipe_raw.csv"
pp_recipe_new_open = open(pp_recipe_new, 'w', encoding='utf8')
pp_recipe_new_writer = csv.writer(pp_recipe_new_open)

counter = 0
raw_csv_open = open(raw_recipe, 'r', encoding="utf8")
raw_reader = csv.reader(raw_csv_open)
next(raw_reader)

for rows in raw_reader:
    if (counter >= len(list_of_recipe_id)):
        break
    id = int(rows[1])
    if (id in list_of_recipe_id):
        pp_recipe_new_writer.writerow(rows)
        print(rows)
        counter += 1







