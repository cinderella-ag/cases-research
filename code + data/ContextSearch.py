parts_of_speech = [['Geox', 'NOUN'], ['Patr', 'NOUN'], ['Abbr', 'NOUN'], ['Name', 'NOUN'], ['Fixd', 'NOUN'], ['NOUN'],
                   ['VERB'], ['INFN'], ['Anum', 'ADJF'], ['ADJF'], ['ADJS'], ['PREP'], ['ADVB'], ['PRCL'], ['NPRO'],
                   ['PRED'], ['CONJ'], ['COMP'], ['PRTF'], ['PRTS'], ['INTJ'], ['GRND'], ['NUMR']]
dictionary = {}

for pos in parts_of_speech:
    file_name = 'dicts/' + pos[0] + '.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        temp = set()
        for s in f:
            temp.update(tuple(s.split("\t")))
        dictionary[pos[0]] = temp


def get_word(sentence):  # поиск целевого слова в предложении
    word_amount = 0
    is_first = 0
    is_last = 0
    index = 0

    for i in range(len(sentence)):
        if sentence[i].isalpha():
            word_amount += 1

        elif len(sentence[i]) > 4 and sentence[i][0] == '[' and sentence[i][1] == '[' and sentence[i][
            len(sentence[i]) - 2] == ']' and sentence[i][
            len(sentence[i]) - 1] == ']':

            word_amount += 1
            word = sentence[i][2:len(sentence[i]) - 2]
            index = i

            is_last = word_amount
            if word_amount == 1:
                is_first = 1

    if is_last == word_amount:
        is_last = 1
    else:
        is_last = 0

    is_capitalized = 0
    if word[0].isupper():
        is_capitalized = 1

    return word, is_first, is_last, is_capitalized, index


def check_answers(s):  # подсчет числа (не)верных ответов
    right = 0
    wrong = 0
    for i in range(4, len(s) - 1):
        if s[i] != "":
            if s[i] == s[len(s) - 1]:
                right += 1
            else:
                wrong += 1

    return right, wrong


def quotations(sentence): # слово - в словосочетании в кавычках?
    index = get_word(sentence)[4]

    start = index - 3
    if start < 0:
        start = 0
    end = index + 3
    if end > len(sentence):
        end = len(sentence)

    before = 0
    after = 0

    for i in range(start, index):
        if sentence[i] == '"' or sentence[i] == '«':
            before += 1
        elif sentence[i] == '"' or sentence[i] == '»':
            before -= 1

    for i in range(index, end):
        if sentence[i] == '"' or sentence[i] == '«':
            after += 1
        elif sentence[i] == '"' or sentence[i] == '»':
            after -= 1

    if before == 1 and after == 1:
        return 1
    return 0


def number(sentence):  # предыдущий токен - число?
    index = get_word(sentence)[4]
    if index == 0:
        return 0

    letters = 0
    numbers = 0
    for i in range(len(sentence[index - 1])):
        if sentence[index - 1][i].isalpha():
            letters += 1
        elif sentence[index - 1][i].isnumeric():
            numbers += 1

    if letters <= 3 and numbers > 0:
        return 1

    return 0


def has_hyphen(word):  # в слове есть дефис?
    for c in word:
        if c == '-':
            return 1
    return 0


def last_in_clause(sentence):  # слово - последнее в клаузе?
    index = get_word(sentence)[4]
    punct_marks = set()
    punct_marks.update(tuple([chr(44), chr(59), chr(58), chr(46), chr(63), chr(33), chr(8211), '?!', '...']))

    if index == len(sentence) - 1 or sentence[index + 1] not in punct_marks:
        return 0
    return 1


def nearest_verb(sentence):  # следующий глагол - одно из следующих 1/3/5/10 слов?
    index = get_word(sentence)[4]
    if index == len(sentence):
        return 0

    t = index + 1
    counter = 0

    one = 0
    three = 0
    five = 0
    ten = 0

    while t < len(sentence) and counter <= 10:
        if sentence[t].isalpha():
            counter += 1

            if this_part_of_speech(sentence[t], 'VERB') or this_part_of_speech(sentence[t], 'INFN'):
                ten = 1
                if counter <= 5:
                    five = 1
                    if counter <= 3:
                        three = 1
                        if counter == 1:
                            one = 1
                break
        t += 1

    return one, three, five, ten


def prev_word(sentence):  # поиск предыдущего слова
    index = get_word(sentence)[4]
    prev = ''
    for i in range(index - 1, -1, -1):
        if sentence[i].isalpha():
            prev = sentence[i]
            break
    return prev


def what_part_of_speech(word):  # какая часть речи данное слово
    res = {}

    capitalized = ''
    for c in word:
        symb = c
        if symb.islower():
            symb = symb.capitalize()
        capitalized += symb

    e_options = e_search(capitalized)

    for pos in parts_of_speech:
        res[pos[0]] = 0
        for opt in e_options:
            if opt in dictionary[pos[0]]:
                res[pos[0]] = 1

    return res


def this_part_of_speech(word, part_of_speech):  # слово - данная часть речи?
    capitalized = ''
    for c in word:
        symb = c
        if symb.islower():
            symb = symb.capitalize()
        capitalized += symb

    e_options = e_search(capitalized)

    for opt in e_options:
        if opt in dictionary[part_of_speech]:
            return 1

    return 0


def e_search(word):  # генерация всех вариантов написания слова через Е/Ё
    n = 0
    index = []
    flag = False

    for i in range(len(word)):
        if word[i] == 'Е':
            n += 1
            index.append(i)

        elif word[i] == 'Ё':
            flag = True
            break

    if n == 0 or flag:
        return [word]

    size = pow(2, n)
    bites = [[]] * size
    temp = [0] * n

    counter = 1
    bites[0] = list(temp)

    while counter < size:
        for i in range(n - 1, -1, -1):
            if temp[i] == 0:

                temp[i] = 1
                for j in range(i + 1, n):
                    temp[j] = 0

                bites[counter] = list(temp)
                counter += 1
                break

    res = [list(word)] * size
    for i in range(size):
        place = 0
        for v in bites[i]:
            if v == 1:
                res[i][index[place]] = 'Ё'
            else:
                res[i][index[place]] = 'Е'
            place += 1
        res[i] = "".join(c for c in res[i])

    return res


def get_features(s):  # получение информации о выполнении признаков
    s = s.strip().split("\t")
    right, wrong = check_answers(s)

    has_context = 0
    if s[3] == '':
        has_context = 1

    sentence = s[2].split()
    word_features = get_word(sentence)
    word, is_first, is_last, is_capitalized = word_features[0:4]

    hyphen = has_hyphen(word)
    is_last_in_clause = last_in_clause(sentence)

    is_Geox = this_part_of_speech(word, 'Geox')
    is_Abbr = this_part_of_speech(word, 'Abbr')
    is_Name = this_part_of_speech(word, 'Name')
    is_Fixd = this_part_of_speech(word, 'Fixd')

    in_quot = quotations(sentence)

    prev_is_number = number(sentence)

    prev = prev_word(sentence)
    prev_pos = "\t".join(str(v) for v in what_part_of_speech(prev).values())

    nv_one, nv_three, nv_five, nv_ten = nearest_verb(sentence)

    return s[0], s[1], s[2], right, wrong, has_context, \
           is_first, is_last, is_capitalized, \
           hyphen, is_last_in_clause, is_Geox, is_Abbr, is_Name, is_Fixd, in_quot, \
           prev_is_number, prev_pos, nv_one, nv_three, nv_five, nv_ten, "\n"


with open('pools/pools.txt', 'r') as fin, open('table.txt', 'w', encoding='utf8') as result:
    for s in fin:
        s = s.split("\t")

        if s[1].strip() == 'NOUN&sing&nomn@NOUN&sing&accs' and s[2].strip() == "9":
            index = s[0]
            file_name = 'pools/pool_' + index + '.tab'

            with open(file_name, 'r', encoding='utf8') as f:
                for string in f:
                    result.write("\t".join(str(v) for v in get_features(string)))
