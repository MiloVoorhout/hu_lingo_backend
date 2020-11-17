def create_library():
    with open('../python-flask/assets/unfiltered_dictionaries/woorden.txt', 'r') as outfile:
        nl = "NL"
        myfile = open('assets/filtered_dictionaries/' + nl + '.txt', 'w')
        for word in outfile:
            word = word.strip()

            if 5 <= len(word) <= 7 and word.isalpha():
                myfile.write(word + "\n")
                print(str(len(word)) + " " + word)

        myfile.close()