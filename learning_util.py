import numpy as np

def random_ssn(number=None, unique=False):
    if number is None or number == 1:
        temp_numbers=np.random.randint(low=0,high=9,size=9)
        temp_string="%d%d%d-%d%d-%d%d%d%d" % (
            temp_numbers[0],
            temp_numbers[1],
            temp_numbers[2],
            temp_numbers[3],
            temp_numbers[4],
            temp_numbers[5],
            temp_numbers[6],
            temp_numbers[7],
            temp_numbers[8]
        )
        return(temp_string)
    else:
        if unique:
            return(None)
        else:
            temp_list=[random_ssn() for x in range(0,number)]
            return(temp_list)