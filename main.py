import copy

##
def main(year,open_txt, yearly_results, gender):
    f = open(open_txt,'r')
    lines = ''
    lst = []


    for line in f:

        if year in line:
            line = line[0:4] + ':  '
            
            
            lines = lines.replace("\n", " ")
            lines = lines.replace("\\", ".2")
            lines = lines.replace(".5", "½")
            lines = lines.replace(".2", " 1/5")
            lines = lines.replace("(tie)", "")
            lines = lines.replace("St.", "St")
            lines = lines.replace(".", "")
            lines = lines.replace("½", ".5")
            lines = lines.replace("1/5", ".2")
            
            lst.append(lines[0:5] + lines[7:-2])
            
            lines = ''
            year = str(int(year) + 1)
            if year == '2020':
                year = str(int(year) + 1)

        
                    
        lines += line[:-1] + "; "

    lines = lines.replace("\n", " ")
    lines = lines.replace("\\", ".2")
    lines = lines.replace(".5", "½")
    lines = lines.replace(".2", " 1/5")
    lines = lines.replace("(tie)", "")
    lines = lines.replace("St.", "St")
    lines = lines.replace(".", "")
    lines = lines.replace("½", ".5")
    lines = lines.replace("1/5", ".2")
    
    lst.append(lines[0:5] + lines[7:-2])
    f.close()

    lst.pop(0)


    score_dict = {}

    apperance_dict = {}

    total_ranking_dict = {}


    def enterInfo(teams, points, place):
        for team in teams:
                
                if team[1] == " ":
                    
                    team = team[1:]
                
                if team not in score_dict:
                    score_dict.update({team: 0})
                    apperance_dict.update({team: 0})
                    total_ranking_dict.update({team:0})
                
                score_dict[team] += float(points)
                apperance_dict[team] += 1
                total_ranking_dict[team] += float(place)

    f = open(yearly_results, 'w')
    f.write("NCAA " + gender + "Championship yearly results: \n")
    for l in lst:
        f.write(l + '\n')
    f.close()

    
    for line in lst:
        if line != '':
            line = line[5:]
            split_string = line.split(";")
            for split in split_string:
                place = 0
                
                if split[2] == ' ':
                    
                    place = split[0:2]
                    teams = split[2:].split(",")
                    points = teams[-1]
                    teams.pop(-1)
                    enterInfo(teams, points, place)
                else:
                    place = split[0:3]
                    teams = split[3:].split(",")
                    points = teams[-1]
                    
                    teams.pop(-1)
                    enterInfo(teams, points, place)




    def fix_dics(dictionary, rev):

        sorted_not_dict = sorted(dictionary.items(), key=lambda x:x[1], reverse=rev)
        sorted_dict = dict(sorted_not_dict)

        return sorted_dict


    score_dict = fix_dics(score_dict,True)

    apperance_dict = fix_dics(apperance_dict, True)

    average_ranking_dict = copy.deepcopy(total_ranking_dict)

    for key in apperance_dict:
        average_ranking_dict[key] =  round(total_ranking_dict[key] / apperance_dict[key],1)

    average_ranking_dict = fix_dics(average_ranking_dict, False)

    return(score_dict,apperance_dict,average_ranking_dict, total_ranking_dict)



mens_score_dict,mens_apperance_dict,mens_average_ranking_dict, mens_total_rnaking_dict = main('1937','input_data/mens_input_data.txt','results/mens_results_by_year.txt',"Men's")

womens_score_dict,womens_apperance_dict,womens_average_ranking_dict, woemsn_total_ranking_dict = main('1982','input_data/womens_input_data.txt','results/womens_results_by_year.txt',"Women's")


combine_score_dict = copy.deepcopy(mens_score_dict)
combine_apperance_dict = copy.deepcopy(mens_apperance_dict)
combine_total_ranking_dict = copy.deepcopy(mens_total_rnaking_dict)




for key in womens_score_dict:
    if key not in combine_score_dict:
        combine_score_dict.update({key: womens_score_dict[key]})
        combine_apperance_dict.update({key: womens_apperance_dict[key]})
        combine_total_ranking_dict.update({key: woemsn_total_ranking_dict[key]})


for key in combine_score_dict:
    if key in womens_score_dict:
        combine_score_dict[key] += womens_score_dict[key]
        combine_apperance_dict[key] += womens_apperance_dict[key]
        combine_total_ranking_dict[key] += woemsn_total_ranking_dict[key]



for key in combine_total_ranking_dict:
    combine_total_ranking_dict[key] = round(combine_total_ranking_dict[key] / combine_apperance_dict[key], 2)

combine_score_dict = sorted(combine_score_dict.items(), key=lambda x:x[1], reverse=True)
combine_score_dict = dict(combine_score_dict)


f = open('results/mens_and_womens_all_time.txt','w')
order = 1
f.write("Women's: \n")
for key in womens_score_dict:

    f.write(str(order) + '. Team ' + key +  ': Score ' + str(womens_score_dict[key]) + ', NCAA apperances ' + str(womens_apperance_dict[key]) + ', Average ranking ' + str(womens_average_ranking_dict[key]) + '\n')
    order += 1
f.write("\n _____________________________________________________________ \n \nMen's: \n")
order = 1
for key in mens_score_dict:

    f.write(str(order) + '. Team ' + key +  ': Score ' + str(mens_score_dict[key]) + ', NCAA apperances ' + str(mens_apperance_dict[key]) + ', Average ranking ' + str(mens_average_ranking_dict[key]) + '\n')
    order += 1
f.write("\n _____________________________________________________________ \n \nCombined: \n")
order = 1
for key in combine_score_dict:

    f.write(str(order) + '. Team ' + key +  ': Score ' + str(combine_score_dict[key]) + ', NCAA apperances ' + str(combine_apperance_dict[key]) + ', Average ranking ' + str(combine_total_ranking_dict[key]) + '\n')
    order += 1

f.close()