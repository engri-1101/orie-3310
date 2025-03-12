def compute_S(teams,seeds,seed,team_region,regions):
    # creating the sets S
    # in the first round [0] faces [1]
    # and in general in the first round [i] faces [i+1] for even i

    # 2D array to store values for S_kl for the DP
    S = [[set() for l in range(6+1)] for k in range(len(teams)+1)]
    tmp_S = [[set() for l in range(6+1)] for k in range(len(teams)+1)]

    # boundary conditions: we know who each team faces in the first round
    for n in teams:
        # even n faces n + 1, odd faces n - 1 as described above
        if (n % 2 == 0):
            tmp_S[n][1].add(n+1)

        else:
            tmp_S[n][1].add(n-1)

    # computing the rest of the values 
    for l in range(2,7):
        step = 2**(l)
        for n in teams:
            group = n//step
            for i in range(step):
                tmp_S[n][l].update(tmp_S[group*step +i][l-1]) 

    # initially we store in S_kl all the teams team k might have faced up to and including round l
    # To get the required sets, we will just look as the difference of S_{kl}, S_{k(l-1)} 
    # as that will be exactly the teams that are competing to play againgst k for round l

    for l in range(1,7):
        for n in teams:
            S[n][l] = list(tmp_S[n][l] - tmp_S[n][l-1] - set([n]))


    return S