import numpy as np

def random_ssn(number=None, unique=False):
    if number is None or number == 1:
        temp_string="%d%d%d-%d%d-%d%d%d%d" % (
            np.random.randint(low=0,high=9,size=None),
            np.random.randint(low=0,high=9,size=None),
            np.random.randint(low=0,high=9,size=None),
            np.random.randint(low=0,high=9,size=None),
            np.random.randint(low=0,high=9,size=None),
            np.random.randint(low=0,high=9,size=None),
            np.random.randint(low=0,high=9,size=None),
            np.random.randint(low=0,high=9,size=None),
            np.random.randint(low=0,high=9,size=None)
        )
        return(temp_string)
    else:
        if unique:
            return(None)
        else:
            temp_list=[random_ssn() for x in range(0,number)]
            return(temp_list)