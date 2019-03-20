import speech_recognition as sr
import os
import re
import nltk
from tqdm import tqdm
from decimal import Decimal
tqdm(nltk.download('stopwords'))
cwd = os.getcwd()
folders = os.listdir(f"{cwd}/Audio_dir/")
lyrics = ''
print()
print("Loading....Pleas wait")
print()
for folder in tqdm(folders):
    if folder in os.listdir(f"{cwd}/audio_text_data"):
        continue
    files = os.listdir(f"{cwd}/Audio_dir/{folder}")
    for file in files:
        AUDIO_FILE = (f"{cwd}/Audio_dir/{folder}/{file}")  
  
        r = sr.Recognizer() 
  
        with sr.AudioFile(AUDIO_FILE) as source: 
            audio = r.record(source)
        filepath = os.path.join(f"{cwd}/audio_text_data/", folder)
        
        try:
            line = (r.recognize_google(audio, language = 'English'))
            lyrics += line
            fil = open(filepath, 'w')
            fil.write(lyrics)
            fil.close()
  
        except sr.UnknownValueError:  
            continue
        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            continue
print("Your testing data is ready Let's go.......")


train_data = f'{cwd}/training_data/'
test_data = f'{cwd}/audio_text_data'

def words_in_a_folder(path):
    """Total number of words in a folder"""
    files_contents = ''
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        opened_file = open(file_path)
        content = opened_file.read()
        files_contents += content
    files_contents = re.sub(r'[^\w\s]','',files_contents) #remove punctuation
    contents_list = files_contents.split()
    contents_list.sort()
    contents_list = [x.lower() for x in contents_list] #to lower case all words
    #contents_list = lammatize(contents_list)
    contents_list = stop_word(contents_list)
    return contents_list

def possible_words(train_data):
    """to count all possible words in training data"""
    list_words = []
    for dir in os.listdir(train_data):
        path = (f"{train_data}{dir}")
        list_words.extend(words_in_a_folder(path)) # combain lists
        list_words = list(dict.fromkeys(list_words)) # rm duplicates from List:
        list_words = stop_word(list_words)
    count = len(list_words)
    return count

def count_files(list_dir = os.listdir(train_data)):
    """count files in a directory"""
    count = 0
    for dir in list_dir:
        count += len(os.listdir(f"{train_data}{dir}"))
    return count

def stop_word(input_words):
    from nltk.corpus import stopwords
    en_stops = set(stopwords.words('english'))
    all_words = input_words
    words = list()
    for word in all_words: 
        if word not in en_stops:
            words.append(word)    
    return words

# def lammatize(word_list):
#     from nltk.stem import WordNetLemmatizer
#     lemmatizer = WordNetLemmatizer()
#     lemmatized_output = [lemmatizer.lemmatize(w) for w in word_list]
#     return lemmatized_output
def probability_dict(file_contents_list, train_data):
    """ find the probability of testing data up on trained data"""
    x = {}
    for dir in os.listdir(train_data):
        words =  words_in_a_folder(f'{train_data}{dir}')
        same_words_counts=[]
        for element in file_contents_list:
            count = 0
            for word in words:
                if element == word:
                    count += 1
            same_words_counts.append(count)
        p_of_words = []     #p_of_words means probability of words
        possible_word = possible_words(train_data)
        word_len = len(words)
        product = 1
        for count in same_words_counts:
            p_a_word = Decimal((count + 1)/(word_len + possible_word))
            product = Decimal(p_a_word * product)
        total_files = count_files()
        Word_containing_file = len(os.listdir(f'{train_data}{dir}'))
        prob_category = Decimal(Word_containing_file / total_files)
        probability = Decimal(product * prob_category)
        x.update({dir:probability})
    return x

def Percentage_calculator(x):
    key_list = list()
    value_list = list()
    for i in x.keys():
        key_list.append(i)
    for j in x.values():
        value_list.append(j)
        
    sum_list = sum(value_list)
    Percentage_list = list()
    for i in value_list:
        try:
            PERCENTAGE = (i/sum_list) * 100
            Percentage_list.append(PERCENTAGE)
        except ZeroDivisionError:
            percentage = 0
    Percentage_dict = dict()
    for key, Percentage in zip(key_list, Percentage_list):
        print(f"{key} =  {Percentage} %.")
        print()
        Percentage_dict.update({key:Percentage})
    return Percentage_dict
    
    
def probability(test_data, train_data):
    prob_list = list()
    for filename in os.listdir(test_data):
        print(filename)
        print()
        file_path = os.path.join(test_data, filename)
        opened_file= open(file_path)
        contents = opened_file.read()
        clean_contents = re.sub(r'[^\w\s]','',contents) #remove punctuation !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
        contents_list = clean_contents.split()
        contents_list.sort()
        contents_list = [x.lower() for x in contents_list] #to lower case all words
        #contents_list = lammatize(contents_list)
        contents_list = list( dict.fromkeys(contents_list)) #remove repeted words
        contents_list = stop_word(contents_list)
        x = probability_dict(contents_list, train_data)
        prob_list.append(Percentage_calculator(x))
        print("=== " * 34)
    return prob_list

def name_file(file_names = os.listdir('audio_text_data')):
    file_name_list = []
    for filename in file_names:
        file_name_list.append(filename)
    return file_name_list
dictr =  probability(test_data, train_data)
def highest(dictr):
    global lenth
    lenth = len(dictr)
    keylist = list()
    for i in name_file():
        for j in dictr:
            value_list = list()
            for value in j.values():
                value_list.append(value)
            maxi = max(value_list)
            keylist.append(list(j.keys())[list(j.values()).index(maxi)])
        return keylist

def final_stat():
    file_names = name_file()
    sucess = 0
    feild = 0
    highest1 = highest(dictr)
    for file_name, high in zip(file_names, highest1):
        file_name_list = file_name.split()
        highest_list = high.split()
        file_name_list= [x.lower() for x in file_name_list]
        highest_list = [x.lower() for x in highest_list]
        if highest_list[0] == file_name_list[0]:
            sucess += 1
        else:
            feild += 1
    print(f"Your model predict {sucess} sucess and {feild} feil")
    print()
    sucess_perc = (sucess/lenth)* 100
    print(f"Your system is {sucess_perc} % accurate")
    stars = (int(sucess_perc/10)*'⭐ ')
    print()
    print(f"Your rating is {stars}")
    print()
    print("💖💖 ⮘⮘Thanks for use me⮚⮚ 💖💖")
    print()
    print("=== " * 34)
        
final_stat()



