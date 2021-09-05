import numpy as np

def compareTwoMat(mat1, mat2):

	bool_iseq = np.array_equal(mat1, mat2)
	print("Is equal? " + str(bool_iseq))
	
	abs_err = np.abs(mat1- mat2)
	rel_err = abs_err/mat1
	print("Absolute error: " + str(np.max(abs_err)))
	print("Relative error: " + str(np.max(rel_err)))