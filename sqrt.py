#!/usr/bin/env python

from collections import Counter

def sqrt(N, num_digits=100):
        """
            computes the square root of n by trial and error
            for n >= 0

            We want to build E[k], an estimation of sqrt(N)*10^k

            given (k,N),  E[k] < sqrt(N)*10^k

            To find the next digit in the appromixation of sqr(N), it is
            equivalent to:
            
            find the largest integer D[k+1] such that:

            10*E[k] + D[k+1] < sqrt(N)*10^(k+1)

            with D[k+1] in [0..9]

            (10*E[k] + D[k+1])^2 < N*10^(k+2)

            D[k+1]^2 + 20*E[k]*D[k+1] + 100*E[k]*E[k] - N*10^(k+2) < 0

            E[k+1] = 10*E[k] + D[k+1]

            To find E[0], proceed exponentially, either doubleing or halving at
            each iteration, until you find the integer such that:
                E[0]^2 < N < (E[0]+1)^2


        """
        if N < 0:
            raise ValueError('invalid input: negative number')
        if N == 0:
            return 0

        if N == 1:
            return 1

        D = []
        e0 = 0
        old_e0_squared = 0
        while old_e0_squared < N:
            new_e0 = e0 + 1
            new_e0_squared = new_e0 * new_e0
            if new_e0_squared > N:
                break
            e0 = new_e0
            old_e0_squared = new_e0_squared
        E = e0
        D += [e0]

        if old_e0_squared != N:
            N_10_k2 = N*100
            k = 1
            while k < num_digits:
                C = 100*E*E - N_10_k2
                E20 = 20*E
                for x in range(9, -1, -1):
                    eq = x*x + E20*x + C
                    if eq <= 0:
                        E = 10*E + x
                        D += [x]
                        break
                N_10_k2 *= 100
                k += 1

        return (E,D)

def random(n):
    k = 0
    E = 2
    digits = []
    bucket_size = 200
    while k<n:
            for x in range(9, -1, -1):
                eq = x*x + 20*E*x + 100*E*E - bucket_size  
                if eq <= 0:
                    E = 10*E + x
                    break
            bucket_size *= 100
            k += 1
            digits += [x]
    return digits

def variability(digit, min_digits, max_digits):
    var = []
    for digits in range(min_digits, max_digits, 10):
        p = Counter(sqrt(2, digits)[1])
        var.append( (p[digit] - (digits//10))/(digits//10) )

    return list(range(min_digits, max_digits, 10)), var


#print(sqrt(2))
#print( sqrt( 11 ) )
#print( sqrt( 123 ) )

#print('probability per digit:')
#print( Counter(sqrt(2, 1000)[1]))
#print( Counter(sqrt(2, 10000)[1]))

#print( random(50) )
#print( [ x for x in islice(random(), start=0, stop=10) ] )
