def is_nomn_accs_other(answer):
    return answer in ['NOUN & sing & accs', 'NOUN & sing & nomn', 'Other']


with open('pools/pools.txt', 'r') as fin:
    counter = 0
    total_lines = 0

    for string in fin:
        string = string.split("\t")

        if string[1].strip() == 'NOUN&sing&nomn@NOUN&sing&accs' and string[2].strip() == "9":
            index = string[0]
            file_name = 'pools/pool_' + index + '.tab'

            with open(file_name, 'r', encoding='utf8') as f:
                for s in f:

                    this_string = s
                    total_lines += 1
                    s = s.strip().split("\t")

                    flag = True

                    start = 0
                    while True:
                        if is_nomn_accs_other(s[start]):
                            break
                        start += 1

                    end = len(s) - 1
                    while True:
                        if is_nomn_accs_other(s[end]):
                            break
                        end -= 1

                    for i in range(start + 1, end):
                        if s[i].strip() != "" and s[i] != s[start]:
                            flag = False
                            break

                    if flag:
                        counter += 1

print('counter = ', counter)
float(counter) * 100 / total_lines
