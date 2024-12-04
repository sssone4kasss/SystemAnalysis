from math import log2

def calculate_counts():
    counts_ab = {}
    counts_a = {}
    counts_b = {}
    
    for i in range(1, 7):
        for j in range(1, 7):
            sum_val = i + j
            prod_val = i * j
            
            if (sum_val, prod_val) not in counts_ab:
                counts_ab[(sum_val, prod_val)] = 1
            else:
                counts_ab[(sum_val, prod_val)] += 1
                
            if sum_val not in counts_a:
                counts_a[sum_val] = 1
            else:
                counts_a[sum_val] += 1
                
            if prod_val not in counts_b:
                counts_b[prod_val] = 1
            else:
                counts_b[prod_val] += 1
    
    return counts_ab, counts_a, counts_b

def calculate_probabilities(counts):
    probabilities = {}
    total_count = 36
    
    for key, count in counts.items():
        probabilities[key] = count / total_count
        
    return probabilities

def calculate_entropy(probabilities):
    entropy = 0.0
    
    for probability in probabilities.values():
        if probability > 0:
            entropy -= probability * log2(probability)
    
    return entropy

def round_values(values):
    return [round(value, 2) for value in values]

def main():
    counts_ab, counts_a, counts_b = calculate_counts()
    
    probability_ab = calculate_probabilities(counts_ab)
    probability_a = calculate_probabilities(counts_a)
    probability_b = calculate_probabilities(counts_b)
    
    entropy_ab = calculate_entropy(probability_ab)
    entropy_a = calculate_entropy(probability_a)
    entropy_b = calculate_entropy(probability_b)
    
    entropy_b_given_a = entropy_ab - entropy_a
    information_a_about_b = entropy_b - entropy_b_given_a
    
    return round_values([entropy_ab, entropy_a, entropy_b, entropy_b_given_a, information_a_about_b])

if __name__ == "__main__":
    print(main())
