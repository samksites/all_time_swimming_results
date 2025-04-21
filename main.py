import copy

'''

'''

def pullresults(year,open_txt, yearly_results, gender):

    # opens the specific txt file
    f = open(open_txt,'r')
    lines = ''
    lst = []

    # Reads each line of the txt file.
    for line in f:
        
        # if the year variable is in this line read this line.
        if year in line:

            line = line[0:4] + ':  '
            
            # clean up lines
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
            # covid year so skip
            if year == '2020':
                year = str(int(year) + 1)

        
                    
        lines += line[:-1] + "; "
    # cleans up the lines
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

    # dictionary of all time total score of a team
    score_dict = {}

    # how man times a team appeared at NCAA
    appearance_dict = {}

    # sum of all of a teams finishing positions
    total_ranking_dict = {}

    
    # used to calculate the sum of a points, appearances and sum of finishing position. 
    def enterInfo(teams, points, place):
        for team in teams:
                
                if team[1] == " ":
                    
                    team = team[1:]
                # if this is the first time reading in a teams data initialize them. 
                if team not in score_dict:
                    score_dict.update({team: 0})
                    appearance_dict.update({team: 0})
                    total_ranking_dict.update({team:0})
                
                # sum up their results
                score_dict[team] += float(points)
                appearance_dict[team] += 1
                total_ranking_dict[team] += float(place)



    # Writes to either the mens or women's yearly txt file.
    f = open(yearly_results, 'w')
    f.write("NCAA " + gender + "Championship yearly results: \n")
    for l in lst:
        f.write(l + '\n')
    f.close()

    # for each line in the cleaned list of swimming results
    for line in lst:
        # if line is not empty
        if line != '':
            # take everything after the 5th character which is after the year
            line = line[5:]

            # split on the ; which gives you a ordered list based on points scored
            split_string = line.split(";")

            # loops through all the teams results
            for split in split_string:
                place = ''
                
                if split[2] == ' ':
                    
                    # gets the place of the teams
                    place = split[0:2]

                    # if teams tied gets all of them
                    teams = split[2:].split(",")
                    
                    # points scored is the last value in the teams list
                    points = teams[-1]
                    # removes the points value from the list
                    teams.pop(-1)

                    # calls the enterInfo method
                    enterInfo(teams, points, place)
                else:
                    # same as method above but shift one string over

                    place = split[0:3]
                    teams = split[3:].split(",")
                    points = teams[-1]
                    
                    teams.pop(-1)
                    enterInfo(teams, points, place)



    # orders the dictionaries 
    def fix_dics(dictionary, rev):

        sorted_not_dict = sorted(dictionary.items(), key=lambda x:x[1], reverse=rev)
        sorted_dict = dict(sorted_not_dict)

        return sorted_dict

    # clean up the score dic
    score_dict = fix_dics(score_dict,True)

    appearance_dict = fix_dics(appearance_dict, True)

    average_ranking_dict = copy.deepcopy(total_ranking_dict)

    for key in appearance_dict:
        average_ranking_dict[key] =  round(total_ranking_dict[key] / appearance_dict[key],1)

    average_ranking_dict = fix_dics(average_ranking_dict, False)

    return(score_dict,appearance_dict,average_ranking_dict, total_ranking_dict)


# Start of the application 
##########################

# calls the pullresults function and collects all the needed data for mens results
mens_score_dict,mens_appearance_dict,mens_average_ranking_dict, mens_total_rnaking_dict = pullresults('1937','input_data/mens_input_data.txt','results/mens_results_by_year.txt',"Men's")

# calls the pullresults function and collects all the needed data for womans results
womens_score_dict,womens_appearance_dict,womens_average_ranking_dict, woemsn_total_ranking_dict = pullresults('1982','input_data/womens_input_data.txt','results/womens_results_by_year.txt',"Women's")


# make deep copy for the combined results
combine_score_dict = copy.deepcopy(mens_score_dict)
combine_appearance_dict = copy.deepcopy(mens_appearance_dict)
combine_total_ranking_dict = copy.deepcopy(mens_total_rnaking_dict)



# combine the results
for key in womens_score_dict:
    if key not in combine_score_dict:
        combine_score_dict.update({key: womens_score_dict[key]})
        combine_appearance_dict.update({key: womens_appearance_dict[key]})
        combine_total_ranking_dict.update({key: woemsn_total_ranking_dict[key]})
    else:
        combine_score_dict[key] += womens_score_dict[key]
        combine_appearance_dict[key] += womens_appearance_dict[key]
        combine_total_ranking_dict[key] += woemsn_total_ranking_dict[key]



# average out the total rankings
for key in combine_total_ranking_dict:
    combine_total_ranking_dict[key] = round(combine_total_ranking_dict[key] / combine_appearance_dict[key], 2)

# sort the dictionaries 
combine_score_dict = sorted(combine_score_dict.items(), key=lambda x:x[1], reverse=True)
combine_score_dict = dict(combine_score_dict)


# whole following section writes the results to the output files

f = open('results/mens_and_womens_all_time.txt','w')
order = 1
f.write("Women's: \n")
for key in womens_score_dict:

    f.write(str(order) + '. Team ' + key +  ': Score ' + str(womens_score_dict[key]) + ', NCAA appearances ' + str(womens_appearance_dict[key]) + ', Average ranking ' + str(womens_average_ranking_dict[key]) + '\n')
    order += 1
f.write("\n _____________________________________________________________ \n \nMen's: \n")
order = 1
for key in mens_score_dict:

    f.write(str(order) + '. Team ' + key +  ': Score ' + str(mens_score_dict[key]) + ', NCAA appearances ' + str(mens_appearance_dict[key]) + ', Average ranking ' + str(mens_average_ranking_dict[key]) + '\n')
    order += 1
f.write("\n _____________________________________________________________ \n \nCombined: \n")
order = 1
for key in combine_score_dict:

    f.write(str(order) + '. Team ' + key +  ': Score ' + str(combine_score_dict[key]) + ', NCAA appearances ' + str(combine_appearance_dict[key]) + ', Average ranking ' + str(combine_total_ranking_dict[key]) + '\n')
    order += 1

f.close()