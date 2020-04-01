parts_of_speech = [['Geox', 'NOUN'], ['Patr', 'NOUN'], ['Abbr', 'NOUN'], ['Name', 'NOUN'], ['Fixd', 'NOUN'], ['NOUN'],
                   ['VERB'], ['INFN'], ['Anum', 'ADJF'], ['ADJF'], ['ADJS'], ['PREP'], ['ADVB'], ['PRCL'], ['NPRO'],
                   ['PRED'], ['CONJ'], ['COMP'], ['PRTF'], ['PRTS'], ['INTJ'], ['GRND'], ['NUMR']]

characteristics = ['has_context', 'is_first', 'is_last', 'is_capitalized', 'hyphen', 'is_last_in_clause', 'is_Geox',
                   'is_Abbr', 'is_Name', 'is_Fixd', 'in_quot', 'prev_is_number']
for pos in parts_of_speech:
    characteristics.append('prev_is_' + pos[0])

characteristics.extend(['nv_one', 'nv_three', 'nv_five', 'nv_ten'])

import itertools


def count_in_combinations(num, limit):
    counter = 0
    comb = [list(x) for x in itertools.combinations(characteristics, num)]

    wrong = [0] * len(comb)
    total = [0] * len(comb)
    examples = [0] * len(comb)

    with open('table.txt', 'r', encoding='utf8') as table:
        for s in table:
            counter += 1
            print(counter)

            s = s.strip().split("\t")

            temp = {}
            for i in range(5, len(s)):
                temp[characteristics[i - 5]] = int(s[i])

            for i in range(len(comb)):
                flag = True

                for v in comb[i]:
                    if temp[v] != 1:
                        flag = False
                        break

                if flag:
                    wrong[i] += int(s[4])
                    total[i] += int(s[3]) + int(s[4])
                    examples[i] += 1

    stat_file = 'stat_data/statistics/stat_' + str(num) + '.txt'

    with open(stat_file, 'w', encoding='utf8') as data_file:
        for i in range(len(comb)):

            res = " ".join(v for v in comb[i])

            res += " " + str(wrong[i]) + " " + str(total[i])
            if wrong[i] != 0:
                res += " " + str(wrong[i] / total[i])
            else:
                res += " " + '0'

            res += " " + str(examples[i])
            res += "\n"

            if examples[i] < limit:
                continue

            data_file.write(res)
            if wrong[i] != 0 and wrong[i] / total[i] > 0.4:
                print(res)

    per_cents = [0] * 101

    with open(stat_file, 'r', encoding='utf8') as statistics:
        for s in statistics:
            s = s.split()
            per_cents[int(float(s[num + 2]))] += 1

    percent_file = 'stat_data/percents/percent_' + str(num) + '.txt'

    with open(percent_file, 'w', encoding='utf8') as percents:
        for i in range(len(per_cents)):
            percents.write(str(i) + "\t" + str(per_cents[i]) + "\n")


count_in_combinations(3, 0)
