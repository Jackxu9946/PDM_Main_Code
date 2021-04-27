import psycopg2
from datetime import datetime
import ast
import json
from matplotlib import pyplot as plt
import csv
import numpy as np


conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)
cur = conn.cursor()

filename = "C:/Users/JackXu/Desktop/SchoolWork/Spring_2021/PDM/RAW_recipes.csv"

#Get a list of all the recipe_id in the database
def get_all_current_recipe():
    cur.execute("Select recipe_id from public.recipe")
    all_recipe_id = cur.fetchall()
    formated_list = []
    for recipe_id in all_recipe_id:
        recipe_id = recipe_id[0]
        formated_list.append(recipe_id)
    return  formated_list

#Go through the excel spreadsheet and populate the nutritional information
def populate_nutritional_info():
    all_recipe_id = get_all_current_recipe()
    counter = 0
    with open(filename, 'r', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            recipe_id = int(row[1])
            if (counter >= len(all_recipe_id)):
                break
            if (recipe_id in all_recipe_id):
                nutritional_info = row[6]
                cur.execute("UPDATE public.recipe SET nutrition = %s where recipe_id = %s", (nutritional_info, recipe_id))
                conn.commit()
                counter += 1
                #print("Ya yeet")

calorie_level = ["Low", "Medium", "High"]
#Low = 0-500
#Medium = 500-2000
#High > 2000
dictionary_calorie_level = {'Low': [46, 58, 59, 62, 118, 150, 167, 170, 242, 243, 325, 355, 356, 429, 436, 508, 524, 547, 557, 585, 632, 824, 825, 1236, 1317, 1320, 1420, 1557, 1712, 2056, 2155, 2284, 2325, 2518, 2540, 2561, 2684, 2712, 2945, 3161, 3165, 3242, 3254, 3328, 3371, 3441, 3496, 3689, 3729, 3739, 3748, 3776, 3779, 3788, 3801, 3805, 3806, 3871, 3900, 3910, 4044, 4133, 4157, 4345, 4395, 4407, 4478, 4489, 4533, 4588, 4764, 4779, 4838, 4880, 4966, 5008, 5025, 5030, 5060, 5178, 5179, 5234, 5270, 5276, 5289, 5293, 5455, 8470, 8476, 8488, 8548, 8559, 8562, 8565, 8606, 8674, 8827, 8842, 9684, 9686, 9858, 9875, 9913, 10627, 10829, 11040, 11127, 11164, 11179, 11324, 11361, 11384, 11427, 11512, 12252, 12496, 12557, 12672, 12997, 13341, 14216, 14742, 14949, 15202, 15209, 15211, 15487, 16364, 16391, 16451, 16736, 16856, 17382, 17831, 17963, 18067, 18095, 18224, 18398, 18476, 19104, 19618, 19627, 19631, 20324, 20688, 20800, 20823, 20981, 21025, 21132, 21227, 21339, 21395, 21570, 21691, 21816, 21859, 21926, 22059, 22224, 22290, 22322, 22337, 22363, 22442, 22637, 22742, 22949, 23303, 23353, 23423, 23431, 23499, 23561, 23757, 23771, 23850, 23932, 24307, 24447, 24503, 24516, 24549, 24631, 24636, 24657, 24701, 24959, 26263, 26768, 27005, 27485, 28356, 28385, 28497, 28848, 28880, 28937, 28945, 29106, 29137, 29172, 29550, 29835, 29977, 30198, 30300, 30473, 30775, 30780, 30910, 30978, 31008, 31146, 31587, 31748, 31777, 32001, 32772, 33141, 33149, 33166, 33167, 33452, 34012, 34264, 35014, 35018, 35595, 35632, 35653, 35788, 35800, 36009, 36107, 36244, 36247, 36434, 36482, 36636, 36675, 36748, 36839, 37073, 37090, 37152, 37225, 37279, 37313, 37401, 37725, 38039, 38216, 38240, 38374, 38404, 38607, 38798, 38811, 38812, 38856, 39338, 39571, 39642, 39705, 40204, 40658, 40788, 40800, 40804, 40865, 40918, 41452, 41953, 41954, 42043, 42070, 42072, 42570, 44141, 45120, 45530, 46022, 46553, 46571, 46921, 46973, 47444, 47691, 48156, 48296, 48997, 49023, 50259, 50431, 51947, 52443, 52448, 52574, 53940, 54025, 54447, 55364, 55437, 59046, 59310, 63469, 63915, 64162, 64652, 65041, 65936, 66853, 67415, 67577, 67693, 69168, 69309, 70590, 70878, 70890, 70919, 71046, 71833, 72049, 72065, 72606, 72905, 73685, 73687, 76915, 77203, 79944, 80022, 80100, 80767, 84274, 84801, 87802, 88418, 88537, 89121, 89507, 90092, 91938, 93908, 94153, 95158, 95355, 95640, 95821, 97155, 98268, 98464, 100892, 101260, 101264, 106545, 107851, 109428, 109793, 111045, 111487, 113458, 116376, 116672, 117716, 117758, 118667, 119084, 119632, 120783, 121154, 121156, 122613, 122615, 122780, 122915, 123540, 123542, 124174, 124641, 126833, 128389, 128450, 135216, 136330, 137010, 138406, 138500, 138842, 139407, 140850, 142309, 144175, 144958, 148927, 151367, 153430, 157276, 157880, 160310, 162801, 164178, 165096, 179945, 184356, 192887, 196210, 197091, 211510, 218390, 239958, 248572, 255098, 260956, 287051, 295063, 298029, 304171, 307887, 317798, 343461, 344278, 392262, 416887], 'Medium': [63, 66, 67, 115, 153, 154, 472, 496, 504, 570, 614, 638, 653, 661, 1823, 1883, 1923, 2923, 3211, 3258, 3326, 3572, 3925, 4028, 4205, 4297, 4344, 4527, 4563, 4570, 5174, 8448, 8584, 8975, 9803, 12539, 12601, 12737, 13586, 14499, 18307, 18373, 18394, 18465, 19897, 20680, 21176, 21302, 22320, 22482, 22642, 23498, 24017, 24193, 24572, 24678, 25259, 25744, 25837, 26791, 28215, 28545, 28731, 29939, 30706, 32361, 32459, 33081, 33561, 34244, 36796, 39136, 40228, 40306, 40358, 40478, 41180, 42068, 42745, 43424, 45017, 46417, 46982, 48279, 52080, 52495, 54356, 54989, 55263, 57251, 57857, 60453, 60780, 64784, 66559, 70134, 71797, 71998, 72600, 73570, 74157, 76887, 79826, 80165, 82108, 84068, 84124, 84797, 92877, 93073, 93093, 96282, 99020, 102864, 103406, 107852, 114022, 120377, 123900, 130766, 134453, 139399, 157287, 164290, 173937, 176593, 243092], 'High': [647, 2866, 2994, 3225, 3347, 3667, 3838, 4528, 5197, 9305, 15869, 20143, 20537, 24414, 40858, 41018, 54932, 64336, 77976, 106299]}

def make_recipe_calorie_pi_char():
    all_recipe_id = get_all_current_recipe()
    for recipe_id in all_recipe_id:
        #Get the current calorie value
        cur.execute("select nutrition from public.recipe where recipe_id = %s", (recipe_id,))
        nutrition = cur.fetchall()
        nutrition = nutrition[0][0]
        if (nutrition != None):
            nutrition = ast.literal_eval(nutrition)
            calorie_num = float(nutrition[0])
            if (calorie_num <= 500):
                dictionary_calorie_level["Low"].append(recipe_id)
            elif (calorie_num > 500 and calorie_num <= 2000):
                dictionary_calorie_level["Medium"].append(recipe_id)
            else:
                dictionary_calorie_level["High"].append(recipe_id)


# data = []
# calorie_level_label = ["Low(0-499)","Medium(500-1999)","High(>=2000)"]
# for level in calorie_level:
#     data.append(len(dictionary_calorie_level[level]))
# fig = plt.figure()
# fig.suptitle("Percentage Of Recipe By Calorie Amount")
# plt.legend(["Low(0-499)", "Medium(500-1999)", "High(>=2000)"])
# plt.pie(data, labels=calorie_level_label)
# plt.show()
# dictionary_calorie_to_nutrition = {"Low":[0,0,0,0,0,0],"Medium":[0,0,0,0,0,0], "High":[0,0,0,0,0,0]}
# low_calorie_nutrition_break_down = [0,0,0,0,0]
# medium_calorie_nutrition_break_down = [0,0,0,0,0]
# high_calorie_nutrition_break_down = [0,0,0,0,0]

def find_calorie_nutrition_breakdown(level):
    all_recipe_id = dictionary_calorie_level[level]
    temp_list = dictionary_calorie_to_nutrition[level]
    for recipe_id in all_recipe_id:
        cur.execute("select nutrition from public.recipe where recipe_id = %s", (recipe_id,))
        nutrition = cur.fetchall()
        nutrition = nutrition[0][0]
        if (nutrition != None):
            nutrition = ast.literal_eval(nutrition)
            nutrition = nutrition[1:]
            for index in range(len(nutrition)):
                value = float(nutrition[index])
                temp_list[index] += value
    dictionary_calorie_to_nutrition[level] = temp_list

#Organization = ["Total Fat", "Sugar", "Sodium", "Protein", "Saturated Fat", Carbohydrates"]
#find_calorie_nutrition_breakdown("Low")
#find_calorie_nutrition_breakdown("Medium")
#find_calorie_nutrition_breakdown("High")
dictionary_calorie_to_nutrition = {'Low': [6451.0, 18286.0, 6318.0, 7853.0, 7460.0, 3341.0], 'Medium': [8336.0, 21038.0, 5348.0, 6986.0, 10816.0, 3488.0], 'High': [5186.0, 18474.0, 2518.0, 3274.0, 7385.0, 2328.0]}
dictionary_calorie_to_nutrition_average = {'Low': [15.107728337236534, 42.824355971896956, 14.796252927400468, 18.39110070257611, 17.470725995316158, 7.8243559718969555], 'Medium': [65.63779527559055, 165.6535433070866, 42.110236220472444, 55.00787401574803, 85.16535433070867, 27.46456692913386], 'High': [259.3, 923.7, 125.9, 163.7, 369.25, 116.4]}

#print(dictionary_calorie_to_nutrition)
for key in dictionary_calorie_to_nutrition:
    current_nutrition_list = dictionary_calorie_to_nutrition[key]
    num = len(dictionary_calorie_level[key])
    average_nutrition_list = [x / num for x in current_nutrition_list]
    dictionary_calorie_to_nutrition_average[key] = average_nutrition_list
    #print(dictionary_calorie_to_nutrition_average)
#print(dictionary_calorie_to_nutrition_average)
# nutrition_label = ["Total Fat", "Sugar", "Sodium", "Protein", "Saturated Fat", "Carbohydrates"]
# fig_0 = plt.figure(0)
# fig_0.suptitle('Nutrition Breakdown For All Low Calories Recipe By PDV(Percentage Daily Value)', fontsize=10)
# plt.pie(dictionary_calorie_to_nutrition_average["Low"],labels=nutrition_label,autopct='%1.1f%%')
# fig_1 = plt.figure(1)
# fig_1.suptitle('Nutrition Breakdown For All Medium Calories Recipe By PDV(Percentage Daily Value)', fontsize=10)
# plt.pie(dictionary_calorie_to_nutrition_average["Medium"],labels=nutrition_label,autopct='%1.1f%%')
# fig_2 =plt.figure(2)
# fig_2.suptitle('Nutrition Breakdown For All High Calories Recipe By PDV(Percentage Daily Value)', fontsize=10)
# plt.pie(dictionary_calorie_to_nutrition_average["High"],labels=nutrition_label,autopct='%1.1f%%')
# plt.show()
# for level in dictionary_calorie_level:
#     current_recipe_id = dictionary_calorie_level[level]
#     current_calorie_count = 0
#     for recipe in current_recipe_id:
#         cur.execute("select nutrition from public.recipe where recipe_id = %s", (recipe,))
#         nutrition = cur.fetchall()
#         nutrition = nutrition[0][0]
#         if (nutrition != None):
#             nutrition = ast.literal_eval(nutrition)
#             #print(nutrition)
#             current_calorie_count += float(nutrition[0])
#     total_calories_by_level[level] = current_calorie_count
#     print(total_calories_by_level)

dictionary_calorie_level = {'Low': [46, 58, 59, 62, 118, 150, 167, 170, 242, 243, 325, 355, 356, 429, 436, 508, 524, 547, 557, 585, 632, 824, 825, 1236, 1317, 1320, 1420, 1557, 1712, 2056, 2155, 2284, 2325, 2518, 2540, 2561, 2684, 2712, 2945, 3161, 3165, 3242, 3254, 3328, 3371, 3441, 3496, 3689, 3729, 3739, 3748, 3776, 3779, 3788, 3801, 3805, 3806, 3871, 3900, 3910, 4044, 4133, 4157, 4345, 4395, 4407, 4478, 4489, 4533, 4588, 4764, 4779, 4838, 4880, 4966, 5008, 5025, 5030, 5060, 5178, 5179, 5234, 5270, 5276, 5289, 5293, 5455, 8470, 8476, 8488, 8548, 8559, 8562, 8565, 8606, 8674, 8827, 8842, 9684, 9686, 9858, 9875, 9913, 10627, 10829, 11040, 11127, 11164, 11179, 11324, 11361, 11384, 11427, 11512, 12252, 12496, 12557, 12672, 12997, 13341, 14216, 14742, 14949, 15202, 15209, 15211, 15487, 16364, 16391, 16451, 16736, 16856, 17382, 17831, 17963, 18067, 18095, 18224, 18398, 18476, 19104, 19618, 19627, 19631, 20324, 20688, 20800, 20823, 20981, 21025, 21132, 21227, 21339, 21395, 21570, 21691, 21816, 21859, 21926, 22059, 22224, 22290, 22322, 22337, 22363, 22442, 22637, 22742, 22949, 23303, 23353, 23423, 23431, 23499, 23561, 23757, 23771, 23850, 23932, 24307, 24447, 24503, 24516, 24549, 24631, 24636, 24657, 24701, 24959, 26263, 26768, 27005, 27485, 28356, 28385, 28497, 28848, 28880, 28937, 28945, 29106, 29137, 29172, 29550, 29835, 29977, 30198, 30300, 30473, 30775, 30780, 30910, 30978, 31008, 31146, 31587, 31748, 31777, 32001, 32772, 33141, 33149, 33166, 33167, 33452, 34012, 34264, 35014, 35018, 35595, 35632, 35653, 35788, 35800, 36009, 36107, 36244, 36247, 36434, 36482, 36636, 36675, 36748, 36839, 37073, 37090, 37152, 37225, 37279, 37313, 37401, 37725, 38039, 38216, 38240, 38374, 38404, 38607, 38798, 38811, 38812, 38856, 39338, 39571, 39642, 39705, 40204, 40658, 40788, 40800, 40804, 40865, 40918, 41452, 41953, 41954, 42043, 42070, 42072, 42570, 44141, 45120, 45530, 46022, 46553, 46571, 46921, 46973, 47444, 47691, 48156, 48296, 48997, 49023, 50259, 50431, 51947, 52443, 52448, 52574, 53940, 54025, 54447, 55364, 55437, 59046, 59310, 63469, 63915, 64162, 64652, 65041, 65936, 66853, 67415, 67577, 67693, 69168, 69309, 70590, 70878, 70890, 70919, 71046, 71833, 72049, 72065, 72606, 72905, 73685, 73687, 76915, 77203, 79944, 80022, 80100, 80767, 84274, 84801, 87802, 88418, 88537, 89121, 89507, 90092, 91938, 93908, 94153, 95158, 95355, 95640, 95821, 97155, 98268, 98464, 100892, 101260, 101264, 106545, 107851, 109428, 109793, 111045, 111487, 113458, 116376, 116672, 117716, 117758, 118667, 119084, 119632, 120783, 121154, 121156, 122613, 122615, 122780, 122915, 123540, 123542, 124174, 124641, 126833, 128389, 128450, 135216, 136330, 137010, 138406, 138500, 138842, 139407, 140850, 142309, 144175, 144958, 148927, 151367, 153430, 157276, 157880, 160310, 162801, 164178, 165096, 179945, 184356, 192887, 196210, 197091, 211510, 218390, 239958, 248572, 255098, 260956, 287051, 295063, 298029, 304171, 307887, 317798, 343461, 344278, 392262, 416887], 'Medium': [63, 66, 67, 115, 153, 154, 472, 496, 504, 570, 614, 638, 653, 661, 1823, 1883, 1923, 2923, 3211, 3258, 3326, 3572, 3925, 4028, 4205, 4297, 4344, 4527, 4563, 4570, 5174, 8448, 8584, 8975, 9803, 12539, 12601, 12737, 13586, 14499, 18307, 18373, 18394, 18465, 19897, 20680, 21176, 21302, 22320, 22482, 22642, 23498, 24017, 24193, 24572, 24678, 25259, 25744, 25837, 26791, 28215, 28545, 28731, 29939, 30706, 32361, 32459, 33081, 33561, 34244, 36796, 39136, 40228, 40306, 40358, 40478, 41180, 42068, 42745, 43424, 45017, 46417, 46982, 48279, 52080, 52495, 54356, 54989, 55263, 57251, 57857, 60453, 60780, 64784, 66559, 70134, 71797, 71998, 72600, 73570, 74157, 76887, 79826, 80165, 82108, 84068, 84124, 84797, 92877, 93073, 93093, 96282, 99020, 102864, 103406, 107852, 114022, 120377, 123900, 130766, 134453, 139399, 157287, 164290, 173937, 176593, 243092], 'High': [647, 2866, 2994, 3225, 3347, 3667, 3838, 4528, 5197, 9305, 15869, 20143, 20537, 24414, 40858, 41018, 54932, 64336, 77976, 106299]}
dictionary_calorie_to_nutrition_average = {'Low': [15.107728337236534, 42.824355971896956, 14.796252927400468, 18.39110070257611, 17.470725995316158, 7.8243559718969555], 'Medium': [65.63779527559055, 165.6535433070866, 42.110236220472444, 55.00787401574803, 85.16535433070867, 27.46456692913386], 'High': [259.3, 923.7, 125.9, 163.7, 369.25, 116.4]}
dictionary_calorie_to_nutrition = {'Low': [6451.0, 18286.0, 6318.0, 7853.0, 7460.0, 3341.0], 'Medium': [8336.0, 21038.0, 5348.0, 6986.0, 10816.0, 3488.0], 'High': [5186.0, 18474.0, 2518.0, 3274.0, 7385.0, 2328.0]}
total_calories_by_level = {'Low': 96163.60000000006, 'Medium': 104462.7, 'High': 64794.69999999999}

PDV_PER_CALORIE_BY_LEVEL = {}
for level in dictionary_calorie_to_nutrition:
    #PDV/CALORIES
    current_nutrition_list = dictionary_calorie_to_nutrition[level]
    num = total_calories_by_level[level]
    nutrition_PDV_PER_CALORIES = [x / num for x in current_nutrition_list]
    PDV_PER_CALORIE_BY_LEVEL[level] = nutrition_PDV_PER_CALORIES
print(PDV_PER_CALORIE_BY_LEVEL)

X = ["Total Fat", "Sugar", "Sodium", "Protein", "Saturated Fat", "Carbohydrates"]
X_axis = np.arange(len(X))

plt.bar(X_axis - .2, PDV_PER_CALORIE_BY_LEVEL["Low"], 0.2, label = "Low")
plt.bar(X_axis , PDV_PER_CALORIE_BY_LEVEL["Medium"], 0.2, label = "Medium")
plt.bar(X_axis + .2, PDV_PER_CALORIE_BY_LEVEL["High"], 0.2, label = "High")
plt.xticks(X_axis,X)
plt.xlabel("Nutrition Category")
plt.ylabel("Percentage Daily Value Per Calories(PDV/Calories)")
plt.title("Percentage Daily Value For Each Calories Group")
plt.legend()
plt.show()

