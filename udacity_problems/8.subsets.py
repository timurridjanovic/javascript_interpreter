# Bonus Practice: Subsets

# This assignment is not graded and we encourage you to experiment. Learning is
# fun!

# Write a procedure that accepts a list as an argument. The procedure should
# print out all of the subsets of that list.

#iterative solution
   
def listSubsets(list, subsets=[[]]):
    if len(list) == 0:
        return subsets
    element = list.pop()
    
    for i in xrange(len(subsets)):
        subsets.append(subsets[i] + [element])
    return listSubsets(list, subsets)

print listSubsets([1, 2, 3, 4, 5])



#recursive solution


def sublists(big_list, selected_so_far):
    if big_list == []:
        print selected_so_far
    else:
        current_element = big_list[0]
        rest_of_big_list = big_list[1:]
        sublists(rest_of_big_list, selected_so_far + [current_element])
        sublists(rest_of_big_list, selected_so_far)
    
    
dinner_guests = ["LM", "ECS", "SBA"]
sublists(dinner_guests, [])
