"""
Use this file to provide your solutions for exercise 1-1 c.
"""
def levenshtein_distance(s1: str, s2: str) -> int:
    d = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]
    for i in range(len(s1) + 1):
        d[i][len(s2)] = len(s1) - i

    for j in range(len(s2) + 1):
        d[len(s1)][j] = len(s2) - j
 
    for i in range(len(s1) -1, -1, -1):
        for j in range(len(s2) -1, -1, -1):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i+1][j] + 1, d[i][j+1] + 1, d[i + 1][j + 1] + cost)

    return d[0][0]

