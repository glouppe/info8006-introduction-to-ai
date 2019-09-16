def mean(lst):
	# FASTER!!!!!
    return sum(lst)/len(lst)

def mean_2(lst):
	sum_ = 0
	counter = 0
	for i in lst:
		sum_ += i
		counter += 1
	return sum_/counter

# Main Function
if __name__ == '__main__':
    lst = [2, 4, 5, 1]
    print(mean(lst))
    print(mean_2(lst))
