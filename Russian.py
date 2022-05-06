from random import randint
from math import exp


def fill_vocab_list(text: list)->tuple:
    # splits a text file into chapters by character '.' and by lines with Russian and English separated by ';'
    vocab_list = []
    chapter_list = [0]
    for i in text:
        # fills the vocab list
        if i[0] == ".":
            chapter_list.append(text.index(i))
            i = i[1:]
        z = i.split(";")
        temp_list = []
        for x in z:
            temp_list.append(x)
        vocab_list.append(temp_list)
    chapter_list.append(len(text))
    return vocab_list, chapter_list


def fill_verb_ad_list(text: list)->tuple:
    nouns = []
    temp_noun_list = text.pop(0).split(";")
    for i in temp_noun_list:
        nouns.append(i.split(":"))
    word_list = []
    temporary_list = []
    # splits the russian from english
    for i in text:
        z = i.split(";")
        temp_list = []
        for x in z:
            temp_list.append(x)
        temporary_list.append(temp_list)
    # splits ending from stem
    for i in temporary_list:
        y = i[0].split(":")
        z = y[1].split(",")
        word_list.append([y[0], z, i[1:]])
    return word_list, nouns


def phonetic_to_russ_char(alpha_input: str)->str:
    # converts a phonetic character to the cyrillic alphabet
    if len(alpha_input) == 1:
        alpha_input += " "
    unicode_alpha = ("\u0410", "\u0411", "\u0412", "\u0413", "\u0414", "\u0415", "\u0416", "\u0417", "\u0418", "\u0419",
                     "\u041A", "\u041B", "\u041C", "\u041D", "\u041E", "\u041F", "\u0420", "\u0421","\u0422", "\u0423",
                     "\u0424", "\u0425", "\u0426", "\u0427", "\u0428", "\u0429", "\u042A", "\u042B", "\u042C", "\u042D",
                     "\u042E", "\u042F", "\u0401", " ", "-")
    russ_alpha = ("a ", "b ", "v ", "g ", "d ", "je", "zh", "z ", "i ", "y ", "k ", "l ", "m ", "n ", "o ", "p ", "r ",
                  "s ", "t ", "u ", "f ", "x ", "ts", "ch", "sh", "sc", "hd", "ih", "sf", "e ", "ju", "ja", "jo", "  ",
                  "- ")
    # checks whether input is a valid character
    if alpha_input not in russ_alpha:
        return "not found"
    i = 0
    while i < len(russ_alpha):
        if alpha_input == russ_alpha[i]:
            return unicode_alpha[i]
        i += 1


def phonetic_to_russ_str(phonetic_string: str)->str:
    # takes a string in the form "11223344" and returns it in cyrillic
    ret = ""
    for i in range(0, len(phonetic_string), 2):
        ret += phonetic_to_russ_char(phonetic_string[i:i+2])
    return ret


def input_to_str()->str:
    # compiles multiples inputs into one string
    ret = ""
    while True:
        temp = input("Enter a letter, ex to finish, back to delete last entry ").lower()
        if temp == "back":
            ret = ret[:-2]
            print(phonetic_to_russ_str(ret))
        elif len(temp) == 1:
            temp += " "
        if len(temp) == 2:
            if temp == "ex":
                print("Input = " + phonetic_to_russ_str(ret))
                return ret
            elif phonetic_to_russ_char(temp) == "not found":
                print("Input is not a valid character. Try again")
            else:
                ret += temp


def translate(word: str, language: str, vocabulary: list) -> str:
    # takes in a word and translates it to output language using a vocabulary
    if language == "r":
        # iterates through all english translations to check whether they are equal to input
        for j in vocabulary:
            i = 1
            while i < len(j):
                if j[i] == word:
                    return phonetic_to_russ_str(j[0])
                i += 1
    for j in vocabulary:
        # prints all english translations from a russian input
        ret = ""
        if j[0] == word:
            i = 1
            while i < len(j):
                ret += j[i] + ", "
                i += 1
            return ret[:-2]
    return "Word not found."


def num_translate(number: int, num_list: list, decimal_list: list) -> str:
    # takes each digit and translates individually
    if number >= 1000**2:
        print("too large")
        return "- "
    else:
        if number >= 1000:
            return num_translate(number//1000, num_list, decimal_list) + num_list[decimal_list[3]][0] + \
                   num_translate(number % 1000, num_list, decimal_list)
        elif 0 <= number % 100 < 20:
            if number % 100 == 0:
                ret = ""
            else:
                ret = num_list[number % 100][0]
        else:
            if number % 10 == 0:
                ret = num_list[int(decimal_list[1]) - 2 + (number // 10) % 10][0]
            else:
                ret = num_list[int(decimal_list[1]) - 2 + (number // 10) % 10][0] + num_list[number % 10][0]
        if (number // 100) != 0:
            ret = num_list[int(decimal_list[2] - 1 + (number // 100) % 100)][0] + ret
        return ret


def adjective_translation(adjective: str, noun: str)->str:
    # takes gender sign and removes it and brackets
    gender = noun[1]
    noun = noun[3:]
    # checks which gender the adjective has to be corrected to
    genders = "mfnpa"
    for i in range(0, len(genders)):
        if genders[i] == gender:
            return adjective[0] + adjective[1][i] + "  " + noun


def verb_translation(verb: str, pronoun: str)->str:
    # takes person and removes it and brackets
    person = pronoun[1]
    pronoun = pronoun[3:]
    # checks which person the verb has to be corrected to
    persons = "123456"
    for i in range(0, len(persons)):
        if persons[i] == person:
            return pronoun + "  " + verb[0] + verb[1][i]


def write(file: str)->None:
    # adds russian words to a text file
    try:
        f = open(file + ".txt", "a+")
        count = 0
        while True:
            finish = input("Would you like to finish? Y for Yes: ")
            if finish == "Y":
                break
            else:
                print("Enter Russian word")
                russian = input_to_str()
                english = ""
                while True:
                    eng = ";" + input("Enter each English translation separately, quit when all English translations"
                                      " added: ")
                    if eng == ";quit":
                        break
                    english += eng
                    f.write("\n" + russian + english)
                    count += 1
        f.close()
        print("Finished editing file " + file + " " + str(count) + " words added.")
    except IOError:
        print("File could not be found")


def help_message()->None:
    # prints representations of russian letters
    print("Symbols for Cyrillic letters:\n\u0410 = a, \u0411 = b, \u0412 = v\n\u0413 = g, \u0414 = d, "
          "u0415 = je\n\u0416 = zh, \u0417 = z, \u0418 = i\n\u0419 = y, \u041A = k, \u041B = l\n"
          "\u041C = m, \u041D = n, \u041E = o\n\u041F = p, \u0420 = r, \u0421 = s\n \u0422 = t, \u0423 = u,"
          " \u0424 = f\n\u0425 = x, \u0426 = ts, \u0427 = ch\n \u0428 = sh, \u0429 = sc, \u042A = hd\n"
          "\u042B = ih, \u042C = sf, \u042D = e\n \u042E = jo, \u042F = ja, \u0401 = jo")


def auto_translation(vocab_list: list)->None:
    # allows the user to translate individual words, or get a help message, or to exit
    while True:
        function = input("Please indicate whether you would like to 'translate', receive 'help' or 'quit' ").lower()
        if function == "quit":
            return None
        elif function == "help":
            help_message()
        elif function == "translate":
            while True:
                language_input = input("'r' to translate into Russian, 'e' to translate into English ")
                if language_input == 'r':
                    word_original = input("Enter a word")
                elif language_input == "e":
                    word_original = input_to_str()
                else:
                    print("Invalid language")
                    continue
                print(translate(word_original, language_input, vocab_list))
                break
        else:
            print("Not available")


def chapter_view(vocab_list: list, chapter_list: list)->None:
    # uses chapter list to print a whole chapter
    while True:
        chapter = input("Which chapter would you like to view? quit to quit ")
        if chapter == "quit":
            break
        if chapter == "help":
            help_message()
        if chapter.isdigit():
            chapter = int(chapter)
            if chapter <= len(chapter_list)-1:
                print("Chapter " + str(chapter) + "\n" + format("Russian", "<25s") + "English")
                for i in range(chapter_list[chapter-1], chapter_list[chapter]):
                    ret = ""
                    for j in range(1, len(vocab_list[i])):
                        ret += str(vocab_list[i][j]) + ", "
                    ret = ret[:-2]
                    print(format(phonetic_to_russ_str(vocab_list[i][0]), "<24s"), ret)
            else:
                print("Chapter not available")
        else:
            print("Invalid input")


def chapter_test(vocab_list: list, chapter_list: list)->None:
    # tests the user on a specific chapter
    while True:
        # initialise variables according to user input
        chapter = input("Which chapter would you like to complete? quit to quit ")
        if chapter == "quit":
            # quit
            break
        if chapter == "help":
            # help
            help_message()
        if chapter.isdigit():
            # checks whether chapter value is a number
            chapter = int(chapter)
            if chapter < len(chapter_list) - 1:
                # checks whether within correct amount of chapters
                score = 0
                language = input("Type \"r\" to test English to Russian, or anything else to test into English ")
                while True:
                    number = input("How many questions would you like? ")
                    if number == "quit":
                        break
                    elif number.isdigit():
                        number = int(number)
                        for i in range(0, number):
                            # for each iteration asks for the translation of a random word in a specific chapter
                            random = randint(chapter_list[chapter - 1], chapter_list[chapter] + 1)
                            print("What is the translation of:")
                            if language == "r":
                                # translation to russian
                                print(vocab_list[random][1])
                                translation = input_to_str()
                                if translation == vocab_list[random][0]:
                                    # correct
                                    score += 1
                                    print("Correct")
                                else:
                                    # incorrect
                                    print("The correct answer is " + phonetic_to_russ_str(vocab_list[random][0]))
                            else:
                                # translation to english
                                language = "e"
                                translation = input(phonetic_to_russ_str(vocab_list[random][0]) + " ")
                                for j in range(1, len(vocab_list[random])):
                                    if translation == vocab_list[random][j]:
                                        # correct
                                        score += 1
                                        print("Correct")
                                    else:
                                        # incorrect
                                        print("The correct answer is " + vocab_list[random][1])
                    else:
                        print("Please enter an integer. ")
                        continue
                    # prints and writes final scores to a file
                    print("Score: " + str(score) + "/" + str(number))
                    f = open("scores.txt", "a+")
                    f.write("\nChapter " + str(chapter) + ", to " + language + ", Score: " + str(score) + "/" +
                            str(number))
                    f.close()
            else:
                # if chapter too large
                print("Chapter not available")
        else:
            # if not a number
            print("Invalid input")


def vocab(text_file: str = "vocab.txt")->None:
    try:
        # opens the file and reads the vocabulary
        f = open(text_file)
        text = f.read().splitlines()
        f.close()
        temp_list = fill_vocab_list(text)
        vocab_list = temp_list[0]
        chapter_list = temp_list[1]
        # function directory for vocab
        while True:
            function = input("Would you like to 'translate', 'view' a chapter, or take a chapter 'test' ").lower()
            if function == "quit":
                break
            elif function == "translate":
                auto_translation(vocab_list)
            elif function == "view":
                chapter_view(vocab_list, chapter_list)
            elif function == "test":
                chapter_test(vocab_list, chapter_list)
            else:
                print("Invalid input")
    except IOError:
        print("File could not be opened. Check both files are in correct directory.")


def num_auto_translation(number_list: list, decimal_list: list)->None:
    # translates digits into russian using num_translate
    while True:
        num = input("Enter number: ")
        if num.isdigit():
            print(num + " is " + phonetic_to_russ_str(num_translate(int(num), number_list, decimal_list)))
        elif num == "quit":
            break
        else:
            print("Invalid input")


def numbers(text_file: str = "numbers.txt")->None:
    try:
        # fills number list
        f = open(text_file)
        text = f.read().splitlines()
        f.close()
        temp_list = fill_vocab_list(text)
        number_list = temp_list[0]
        decimal_list = temp_list[1]
        while True:
            function = input("Would you like to 'translate' a number or 'test' yourself? ").lower()
            if function == "quit":
                break
            elif function == "translate":
                num_auto_translation(number_list, decimal_list)
            elif function == "test":
                while True:
                    diff = input("Please indicate difficulty: 1-3 ")
                    score = 0
                    # addition
                    if diff == "quit":
                        break
                    elif diff == "1":
                        questions = input("How many questions would you like to answer? ")
                        if questions == "quit":
                            break
                        if questions.isdigit():
                            for i in range(0, int(questions)):
                                a = randint(0, 100)
                                b = randint(0, a)
                                print(str(a-b) + "+" + str(b) + "= ")
                                result = input_to_str()
                                ret = num_translate(a, number_list, decimal_list)
                                if ret == result:
                                    print("Correct")
                                    score += 1
                                else:
                                    print("Incorrect")
                                    print("Correct answer was " + phonetic_to_russ_str(ret))
                        else:
                            print("Not a number")
                            continue
                    # subtraction
                    elif diff == "2":
                        questions = input("How many questions would you like to answer? ")
                        if questions == "quit":
                            break
                        if questions.isdigit():
                            for i in range(0, int(questions)):
                                a = randint(0, 1000)
                                b = randint(0, a)
                                print(str(a) + "-" + str(b) + "= ")
                                result = input_to_str()
                                ret = num_translate(a-b, number_list, decimal_list)
                                if ret == result:
                                    print("Correct")
                                    score += 1
                                else:
                                    print("Incorrect")
                                    print("Correct answer was " + phonetic_to_russ_str(ret))
                        else:
                            print("Not a number")
                            continue
                    # integration
                    elif diff == "3":
                        questions = input("How many questions would you like to answer? ")
                        if questions == "quit":
                            break
                        if questions.isdigit():
                            print("Enter all results rounded down to the nearest integer")
                            for i in range(0, int(questions)):
                                function = randint(1, 3)
                                coefficient = randint(1, 10)
                                lower_limit = randint(0, 1)
                                upper_limit = randint(2, 3)
                                # exponential form
                                if function == 1:
                                    power = randint(1, 3)
                                    print("\u222B" + str(coefficient) + "e^" + str(power) + "x from " + str(lower_limit)
                                          + " to " + str(upper_limit))
                                    result = int(((exp(power * upper_limit)) - (exp(power * lower_limit))) /
                                                 power * coefficient)
                                # x to a power
                                else:
                                    power = randint(1, 9)
                                    print("\u222B" + str(coefficient) + "x^" + str(power) + " from " + str(lower_limit)
                                          + " to " + str(upper_limit))
                                    result = int(((upper_limit ** (power + 1)) - (lower_limit ** (power + 1))) /
                                                 (power + 1) * coefficient)
                                answer = input_to_str()
                                if num_translate(result, number_list, decimal_list) == answer:
                                        print("Correct")
                                        score += 1
                                else:
                                    print("Incorrect")
                                    print("Correct answer was " +
                                          phonetic_to_russ_str(num_translate(result, number_list, decimal_list)))
                        else:
                            print("Not a number")
                            continue
                    else:
                        print("Invalid difficulty")
                        continue
                    print("Score: " + str(score) + "/" + str(questions))
                    f = open("scores.txt", "a+")
                    f.write("\nMath level " + str(diff) + ", Score: " + str(score) + "/" + str(questions))
                    f.close()
                else:
                    print("Invalid function. Returning to main selection.")
            else:
                print("Invalid input")
    except IOError:
        print("File could not be opened")


def adjectives_view(ads: list)->None:
    # printed title
    print(format("Adjective (masc.)", "<20s") + format("Fem, Neut, Plural, Accusative", "<35s") + "English")
    for i in ads:
        endings = ""
        english = ""
        # adds all endings but the masculine to list endings
        for j in range(1, len(i[1])):
            endings = endings + phonetic_to_russ_str(i[1][j]) + ","
        # adds all english translations to list english
        for k in i[2]:
            english = english + k + ", "
        # prints adjective with male ending, endings and english - excluding the final commas
        print(format(phonetic_to_russ_str(str(i[0]) + str(i[1][0])), "<20s") + format(endings[:-1], "<35s")
              + english[:-2])


def adjectives_test(ads: list, nouns: list)->None:
    while True:
        questions = input("How many questions would you like? ")
        if questions == "quit":
            break
        score = 0
        # loop for the amount of questions specified
        if questions.isdigit():
            for i in range(0, int(questions)):
                # chooses a random adjective, noun, and english translation
                adjective = randint(0, len(ads)-1)
                noun = randint(0, len(nouns)-1)
                english = randint(0, len(ads[adjective][2])-1)
                print(str(ads[adjective][2][english]) + " " + str(nouns[noun][1]))
                answer = input_to_str()
                if answer == adjective_translation(ads[adjective], nouns[noun][0]):
                    score += 1
                    print("Correct")
                else:
                    print("Correct answer: " + phonetic_to_russ_str(adjective_translation(ads[adjective],
                                                                                          nouns[noun][0])))
            print("Score: " + str(score) + "/" + str(questions))
            f = open("scores.txt", "a+")
            f.write("\nAdjectives, Score: " + str(score) + "/" + str(questions))
            f.close()
        else:
            print("Not a number")


def adjectives(ad_file: str)->None:
    try:
        # opens adjective file: the first line contains nouns and their genders
        f = open(ad_file)
        text = f.read().splitlines()
        f.close()
        temp_list = fill_verb_ad_list(text)
        ad_list = temp_list[0]
        nouns = temp_list[1]
        # function choice
        while True:
            function = input("Would you like to 'view' adjectives, 'test' yourself or 'quit' ").lower()
            if function == "quit":
                break
            elif function == "view":
                adjectives_view(ad_list)
            elif function == "test":
                adjectives_test(ad_list, nouns)
            else:
                print("Invalid function")
    except IOError:
        print("File could not be opened")


def verbs_view(verb: list)->None:
    # printed title
    print(format("Verb stem", "<20s") + format("1st, 2nd, 3rd person: singular/plural", "<40s") + "English")
    for i in verb:
        endings = ""
        english = ""
        # adds all endings to list endings
        for j in range(0, len(i[1])):
            endings = endings + phonetic_to_russ_str(i[1][j]) + ","
        # adds all english translations to list english
        for k in i[2]:
            english = english + k + ", "
        # prints verb stem, endings and english - excluding the final commas
        print(format(phonetic_to_russ_str(str(i[0]) + "- "), "<20s") + format(endings[:-1], "<40s")
              + english[:-2])


def verbs_test(verb: list, pronouns: list)->None:
    while True:
        questions = input("How many questions would you like? ")
        if questions == "quit":
            break
        score = 0
        # loop for the amount of questions specified
        if questions.isdigit():
            for i in range(0, int(questions)):
                # chooses a random adjective, noun, and english translation
                verb_ = randint(0, len(verb)-1)
                pronoun = randint(0, len(pronouns)-1)
                english = randint(0, len(verb[verb_][2])-1)
                print(str(pronouns[pronoun][1]) + " " + str(verb[verb_][2][english]))
                answer = input_to_str()
                if answer == verb_translation(verb[verb_], pronouns[pronoun][0]):
                    score += 1
                    print("Correct")
                else:
                    print("Correct answer: " + phonetic_to_russ_str(verb_translation(verb[verb_],
                                                                                     pronouns[pronoun][0])))
            print("Score: " + str(score) + "/" + str(questions))
            f = open("scores.txt", "a+")
            f.write("\nVerbs, Score: " + str(score) + "/" + str(questions))
            f.close()
        else:
            print("Not a number")
        


def verb_aspect(verb: list, pronouns: list)->None:
    while True:
        questions = input("How many questions would you like? ")
        if questions == "quit":
            break
        score = 0
        # loop for the amount of questions specified
        if questions.isdigit():
            for i in range(0, int(questions)):
                # chooses a random adjective, noun, and english translation
                verb_ = randint(0, len(verb)-1)
                pronoun = randint(0, len(pronouns)-1)
                english = randint(0, len(verb[verb_][2])-1)
                print(str(pronouns[pronoun][1]) + " " + str(verb[verb_][2][english]))
                answer = input_to_str()
                if answer == verb_translation(verb[verb_], pronouns[pronoun][0]):
                    score += 1
                    print("Correct")
                else:
                    print("Correct answer: " + phonetic_to_russ_str(verb_translation(verb[verb_],
                                                                                     pronouns[pronoun][0])))
            print("Score: " + str(score) + "/" + str(questions))
            f = open("scores.txt", "a+")
            f.write("\nVerbs, Score: " + str(score) + "/" + str(questions))
            f.close()
        else:
            print("Not a number")


def verbs(verb_file: str)->None:
    try:
        # opens verb file: the first line contains pronouns
        f = open(verb_file)
        text = f.read().splitlines()
        f.close()
        temp_list = fill_verb_ad_list(text)
        verb_list = temp_list[0]
        pronouns = temp_list[1]
        # function choice
        while True:
            function = input("Would you like to 'view' verbs, 'test' yourself or 'quit' ").lower()
            if function == "quit":
                break
            elif function == "view":
                verbs_view(verb_list)
            elif function == "test":
                verbs_test(verb_list, pronouns)
            elif function == "aspect":
                try:
                    verb_aspect(aspect_load(aspect_file))
                except IOError:
                    print("File could not be opened")
            else:
                print("Invalid function")
    except IOError:
        print("File could not be opened")


def main_function()->None:
    # calls different function based on user input
    print("Welcome to Russian!")
    while True:
        function = (input("Options: 'quit', 'vocab', 'math', 'adjectives', 'verbs', 'write' "
                          "to file. ")).lower()
        if function == "quit":
            break
        elif function == "vocab":
            vocab()
        elif function == "math":
            numbers()
        elif function == "adjectives":
            adjectives("adjectives.txt")
        elif function == "verbs":
            verbs("verbs.txt")
        elif function == "write":
            inp = input("Please give the name of the text file including '.txt': ")
            write(inp)
        else:
            print("Invalid input.")


main_function()
