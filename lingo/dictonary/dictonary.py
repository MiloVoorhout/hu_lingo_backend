def create_library():
    with open('../../assets/unfiltered_dictionaries/woorden.txt', 'r') as outfile:
        nl = "NL"
        myfile = open('../../assets/filtered_dictionaries/' + nl + '.txt', 'w+')
        for word in outfile:
            word = word.strip()
            if not word[0].isupper():
                if 5 <= len(word) <= 7 and word.isalpha():
                    myfile.write(word + "\n")

        myfile.close()

create_library()