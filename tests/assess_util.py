# Testing/performance
import timeit
import src

test_iterations = 1000

print("Random SSN, 10, non-unique, w/ dashes")
print(src.random_ssn(10))
t = timeit.Timer(stmt="util.random_ssn(10)", setup="import util")
print(f"Average runtime (n={test_iterations} times): %f\n" % t.timeit(test_iterations))

print("Random SSN, 10, unique, w/ dashes")
print(src.random_ssn(10, unique=True))
t = timeit.Timer(stmt="util.random_ssn(10, unique=True)", setup="import util")
print(f"Average runtime (n={test_iterations} times): %f\n" % t.timeit(test_iterations))

print("Random SSN, 10, non-unique, w/o dashes")
print(src.random_ssn(10, dashes=False))
t = timeit.Timer(stmt="util.random_ssn(10, dashes=False)", setup="import util")
print(f"Average runtime (n={test_iterations} times): %f\n" % t.timeit(test_iterations))

print("Random SSN, 10, unique, w/o dashes")
print(src.random_ssn(10, unique=True, dashes=False))
t = timeit.Timer(stmt="util.random_ssn(10, unique=True, dashes=False)", setup="import util")
print(f"Average runtime (n={test_iterations} times): %f" % t.timeit(test_iterations))

