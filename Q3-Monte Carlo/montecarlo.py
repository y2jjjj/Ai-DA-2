import numpy as np

# Define probabilities
P_A = {True: 0.8, False: 0.2}  # P(Aptitude Skills)
P_C = {True: 0.5, False: 0.5}  # P(Coding Skills)

# P(G | A, C) - Grade given Aptitude and Coding Skills
P_G_given_A_C = {
    (True, True): {True: 0.9, False: 0.1},
    (True, False): {True: 0.7, False: 0.3},
    (False, True): {True: 0.6, False: 0.4},
    (False, False): {True: 0.3, False: 0.7},
}

# P(J | G) - Go for Job given Grade
P_J_given_G = {
    True: {True: 0.8, False: 0.2},
    False: {True: 0.2, False: 0.8},
}

# P(S | G) - Start a Startup given Grade
P_S_given_G = {
    True: {True: 0.7, False: 0.3},
    False: {True: 0.3, False: 0.7},
}

def monte_carlo_simulation(num_samples=10000):
    # Evidence: Let's compute P(J=True | A=True)
    evidence_A = True  # Aptitude Skills = Yes
    target_J = True    # Go for Job = Yes

    count_target_given_evidence = 0
    count_evidence = 0

    for _ in range(num_samples):
        # Sample Aptitude Skills (A)
        A = evidence_A  # Fix evidence

        # Sample Coding Skills (C)
        C = np.random.rand() < P_C[True]

        # Sample Grade (G) given A and C
        G = np.random.rand() < P_G_given_A_C[(A, C)][True]

        # Sample Go for Job (J) given Grade
        J = np.random.rand() < P_J_given_G[G][True]

        # Check if evidence is true
        if A:
            count_evidence += 1
            if J == target_J:
                count_target_given_evidence += 1

    # Compute conditional probability
    if count_evidence == 0:
        return 0  # Avoid division by zero
    return count_target_given_evidence / count_evidence

# Run simulation
estimated_probability = monte_carlo_simulation()
print(f"Estimated P(J=True | A=True): {estimated_probability}")
