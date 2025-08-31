# CSP300 - SOFTWARE LAB – III
# Assignment-2: Halloween Candy Problem

def find_cnt():
    """
    This function iterates through numbers less than 200 to find a number
    that satisfies all the given conditions from the candy problem.
    """
  
    for cnt in range(1, 200):
        
        # Condition 1: Divided by 5, remainder is 2
        condition1 = (cnt % 5 == 2)
        
        # Condition 2: Divided by 6, remainder is 3
        condition2 = (cnt % 6 == 3)
        
        # Condition 3: Divided by 7, remainder is 2
        condition3= (cnt % 7 == 2)
        
       
        if condition1 and condition2 and condition3:
            print(f"Found the answer! There are {cnt} pieces of candy in the bowl!!!!!")
            return cnt
            
    # This part will only be reached if no answer is found under 200.
    print("Could not find an answer that satisfies the conditions under 200.")
    return None

# Run the function to find the answer.
find_cnt()

