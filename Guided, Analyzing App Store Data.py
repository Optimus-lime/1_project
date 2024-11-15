#!/usr/bin/env python
# coding: utf-8

# # Analysis of mobile apps
# 
# In this project I will be taking on the role of a data analyzer, I will be collecting data from various apps in google and apple app store. My goal will be to try and figure out what app category would attract the most amount of users.

# In[1]:


#this functions allows me to slice a dataset and print the rows need for inspection
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[2]:


#going through the process of opening, reading and saving the read info from the AppleStore.csv
opened_apple = open('AppleStore.csv')
from csv import reader
read_apple = reader(opened_apple)
apple_data = list(read_apple)

#same proccess i did above but for the googleplaystore.csv
opened_google = open('googleplaystore.csv')
read_google = reader(opened_google)
google_data = list(read_google)


# In[3]:


#using the explore_date function to print a couple of the rows from the datasets
explore_data(apple_data, 0, 1, False)
explore_data(google_data,0,2,False)


# In[4]:


#using the dataset forums i was able to find a discrepancie in the dataset to remove
explore_data(google_data,10473,10474,False)
del google_data[10473]
explore_data(google_data,10473,10474,False)


# In[5]:


# the google dataset has duplicate entries  
#i will try to find and extract the duplicates
duplicates = []
unique = []

for row in google_data:
    name = row[0]
    if name in unique:
        duplicates.append(name)
    else:
        unique.append(name)
        
print("#  of dups:", len(duplicates))
print('\n')
print('Examples of duplicate apps:', duplicates[:10])


# In[6]:


print('Expected length:', len(google_data) - 1181)


# In[7]:


#instead of removing the duplicate entries at random
#i will be removing only the outdated inputs
#only the input with the largest amount of reviews wil be left in the dataset
#here i will be retrieving the updated review count alongside the app name, in a dictionary
reviews_max = {}
for row in google_data[1:]:
    name = row[0]
    n_reviews = float(row[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    if name not in reviews_max:
        reviews_max[name] = n_reviews
print(len(reviews_max))


# In[8]:


#this list will be used to add alll the non-duplicate app info from the google dataset
google_clean = []
#this list will be used to keep track of the apps that have already been added to the anroid_clean list
already_added = []

#going through the google dataset to pull the updated rows with the latest review count
for row in google_data[1:]:
    name = row[0]
    n_reviews = float(row[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        google_clean.append(row)
        already_added.append(name)
print(len(google_clean))


# In[9]:


#in this step i will be creating a function that can go through a string and identify whether
#the app name has more than 3 non-english characters
def en(string):
    non_en = 0
    for character in string:
        if ord(character) > 127:
            non_en +=1
    if non_en > 3:
        return False
    else:
        return True
print(en('Instagram'))
print(en('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(en('Docs To Go™ Free Office Suite'))
print(en('Instachat 😜'))


# In[10]:


#both of these will be used to store the info of the english apps
google_english = []
apple_english = []

#going through our updated google dataset and running the function we created above to extract
#the english apps
for app in google_clean:
    name = app[0]
    if en(name):
        google_english.append(app)

#doing the same proccess but for the apple dataset
for app in apple_data:
    name = app[1]
    if en(name):
        apple_english.append(app)
        
print(len(google_english))
print(len(apple_english))


# In[11]:


#both of these lists will be used to store the info of the free apps
google_free = []
apple_free = []

#going through the dataset of the english google apps to extract the free ones
for app in google_english:
    types = app[6]
    if types == 'Free':
        google_free.append(app)

#doing the same process but for the apple dataset
for app in apple_english[1:]:
    price = app[4]
    if price == '0.0':
        apple_free.append(app)

print(len(google_free))
print(len(apple_free))


# In[12]:


#we want our app to be on both platforms so we will be looking at info from both app stores

#this function will go through a dataset and return a dictionary with the name of the specific column
#that was chosen and the frequency that it was repeated in percentage form
def freq_table(dataset, index):
    freq = {}
    length = 0
    for rows in dataset:
        length += 1
        key = rows[index]
        if key in freq:
            freq[key] += 1
        else:
            freq[key] = 1
            
    percent_table = {}
    for key in  freq:
        percentages = (freq[key] / length) * 100
        percent_table[key] = percentages
    return percent_table

#this function turns the dictionary created from the freq_table function into a tuple
#it then sorts the list in descending order
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[13]:


#frequency table for prime_genre column in apple dataset
display_table(apple_free, -5)


# In[14]:


#frequency table for Genres column in google dataset
display_table(google_free, 1)


# In[15]:


#frequency table in Category column in google dataset
display_table(google_free, -4)


# In[16]:


#in this line of code i am creating a dictionary for the genres in the apple data 
#and saving it to a vairable
genres_apple = freq_table(apple_free, -5)

#these loops are being used to see how many users on average rate an app in a spefific genre
#the first loop is being used to keep track of the total amount of ratings per genre
#and the amount of apps in a specific genre
for genre in genres_apple:
    total = 0
    len_genre = 0
    #this loop is used to pull the amount of ratings a specific genre is receiving
    for apps in apple_free:
        genre_app = apps[-5]
        #this if condition adds the amount of ratings pulled from a specific app to the total ratings 
        #per genre
        if genre_app == genre:
            ratings = float(apps[5])
            total += ratings
            len_genre += 1
    #this line of code divides the total amount of ratings a genre received by the amount of apps
    #in that genre
    avg_ratings = total / len_genre
    print(genre, ':', avg_ratings)


# In[17]:


#in this line of code I am creating a dictionary for the genres in the google dataset 
#and saving it to a variable
category_google = freq_table(google_free, 1)

#these loops are used to see how many people have installed an app in a specific genre
#the first loop is being used to keep track of the total installs per genre
#and the number of apps in each genre
for category in category_google:
    total = 0 
    len_category = 0
    #this loop is used to pull the amount of intalls a specific app received
    for apps in google_free:
        category_app = apps[1]
        #this if condition adds the amount of installs an app recieved to the total amount being stored
        #in the main loop
        if category_app == category:
            installs = apps[5]
            installs = installs.replace('+', '')
            installs = installs.replace(',', '')
            total += float(installs)
            len_category += 1
    #this line of code divides the total amount of installs a genre received by the amount of apps
    #in that genre
    avg_installs = total / len_category
    print(category, ': ',  avg_installs )


# #Conclusion
# In conclusion applications in the Social and Gaming categories contain the most amount of users. Making those very competitive categories not only with giants taking majority of marketshare but filled with a ton of smaller applications trying to get their share of the pie. Out of the entire categories listed in both datasets, I would recommend creating an app in the productivity/utilies category. This category this contains a large user base and isn't as flooded as the social or gaming categories.
