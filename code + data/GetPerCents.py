with open('stat_data/statistics/stat_3.txt', 'r', encoding='utf8') as statistics:
    for s in statistics:
        s = s.split()
        if float(s[5]) >= 0.25:
            print(" ".join(v for v in s))
