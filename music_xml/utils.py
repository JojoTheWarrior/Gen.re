# input_list = ['c', 'a', 'a3b#4e2', 'a4a#5', 'a4','b-4']


# turns training data set to the more flexible list set
def turn_to_training(input_list):
    output_list = []
    for item in input_list:
        if len(item) == 2 or len(item) == 1:
            output_list.append([item])
        else:
            temp = []
            var = ""
            for letter in item:
                if letter.isalpha() and var != "":
                    if letter != var: # that means that it is on the next note
                        temp.append(var) # 
                        var = letter # reset the var to the next note
                else:
                    var = var + letter

            temp.append(var)
            output_list.append(temp)
    return output_list
 
