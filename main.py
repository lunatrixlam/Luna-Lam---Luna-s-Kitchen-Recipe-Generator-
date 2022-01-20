"""
Luna's Kitchen is a recipe generator program that uses the requests and BeautifulSoup4 modules from bs4 to webscrape data from the web to populate a recipe title, recipe description summary, link to recipe URL, and recipe details including serving size, ingredients list, and instructions list. Users also have the ability to save the recipe and URL to a dictionary and save recipe ingredients to a shopping list.
"""

from bs4 import BeautifulSoup

import requests

# A dictionary to store saved recipes
my_recipes = {}

# A list to store saved recipe ingredients
my_shopping_list = []

# The draw_border function creates a pretty border
def draw_border():
    print("-" * 45)
    print()

# The welcome function greets the user
def welcome():
    print(("\U0001F319 " * 3) + " Welcome to Luna's Kitchen " + (" \U0001F319" * 3))   # \U000 allows for emoji printing via unicode
    draw_border() # creates a decorative border

# The display_menu function displays the navigation options to the user
def display_menu():
    print("Menu Options:")
    print("[V]iew Saved Recipes")
    print("[G]et a Recipe")
    print("[D]isplay Shopping List")
    print("[Q]uit Kitchen")
    print()

# The goodbye function wishes the user goodbye
def say_goodbye():
    print(("\U0001F319 ") + " Thanks for visiting Luna's Kitchen! Goodbye. " + (" \U0001F319"))

# The get_recipe function  asks the user for input to generate a URL to allow the calling of requests, BeautifulSoup, and find methods to generate recipe title, summary, and link. 

def get_recipe():
    ingredient = input("Enter an ingredient or recipe: \n> ").lower()

    ingredients = ingredient.split()    # splits the string and stores the substring into a list
    url = "https://www.allrecipes.com/search/results/?search="  # base URL to call .get() method

    for ingredient in ingredients:  # concatenates each ingredient element to base URL to complete URL
        url = url + ingredient + "+"
    
    url = f"{url}recipe"

    print()
    print(f"Searching: {url} ")
    print()

    result = requests.get(url)  # sends HTTP GET request to URL to scrape, responding with HTML content of page

    doc = BeautifulSoup(result.text, "html.parser") # fetches and parses the HTML content data as text

    draw_border()

    global recipe_title

    recipe_title = doc.find("h3", class_="card__title").text    # analyzes h3 tag and class attributes to extract specified data

    print(recipe_title.strip()) # .strip() removes whitespace
    print()

    recipe_summary = doc.find("div", class_="card__summary").text  
    print("Summary: ")
    print(recipe_summary.strip())
    print()

    global recipe_link

    recipe_link = doc.find("a", class_="card__titleLink", href=True)["href"]    # ["href"] retrieves only link

    print(f"Link: {recipe_link}")
    print()

# The view_recipe function executes continuously until broken. It asks the user for input to determine if the recipe serving, ingredients, and instruction details should be printed.  

def view_recipe():

    while True: 
        view_recipe = input("Would you like to view the recipe? Enter yes or no: \n> ").lower().strip()

        if view_recipe == "n" or view_recipe == "no":
            print()
            break
        elif view_recipe == "y" or view_recipe == "yes":
            get_recipe = requests.get(recipe_link)

            recipe_doc = BeautifulSoup(get_recipe.text, "html.parser")

            print()
            draw_border()
            print(" Servings:")
            recipe_servings = recipe_doc.find("div", class_="recipe-adjust-servings__original-serving").string
            print(recipe_servings)
            print()

            global ingredients

            ingredients = recipe_doc.find("fieldset", class_="ingredients-section__fieldset").text

            # ln 84 to 92 cleans up the output by removing unnecessary whitespace from raw website output

            ingredients = ingredients.split('         ') and ingredients.split('      ') and ingredients.split(' ') and ingredients.split('   ')
            
            update_ingredients = []

            for i in ingredients:
                if i != '':
                    update_ingredients.append(i)
            
            ingredients = update_ingredients

            for i in ingredients:
                print(i)
                print()

            instructions = recipe_doc.find("fieldset", class_="instructions-section__fieldset").text

            # ln 102 to 117 cleans up the output by removing unnecessary whitespace from raw website output

            instructions = instructions.split('      ')
            
            update_instructions = []

            for i in instructions:
                if "Advertisement" in i:
                    i = i.split(" ")
                    i.remove("Advertisement")
                    i = " ".join(i)
                if "  Step" in i: 
                    i = i.split("  ")
                    i = "".join(i)
                if i != '      ':
                    update_instructions.append(i)
            
            instructions = update_instructions

            draw_border()

            for i in instructions:
                print(i)
                print()
            
            draw_border()
            break
        else:
            print("Sorry, that wasn't an option. Try again.")
            print()

# The my_saved_recipes function displays the saved recipes from the user's current session in Luna's Kitchen

def my_saved_recipes():

    if my_recipes == {}:
        print("No recipes currently saved.")
    else:
        print("\U0001F4D6 My Recipes:")
        
        count = 1
        for key in my_recipes:
            print(f"{count}: {key}, {my_recipes[key]}")
            count += 1    
    print()

# The save_ingredients function adds the ingredients from the most recently viewed recipe to my_shopping_list and also checks to see if the same recipe's ingredients were previously already added

def save_ingredients():

    while True:

        save_ingredient = input("Would you like to save the recipe ingredients to your shopping list? Enter yes or no: \n> ").lower().strip()
        print()

        if save_ingredient == "n" or save_ingredient == "no":
            break
        elif save_ingredient == "y" or save_ingredient == "yes":

            in_list = False

            for item in my_shopping_list:
                if item == recipe_title:
                    in_list = True
            
            if in_list == True:
                print("Recipe ingredients previously added to shopping list!")
                print()

            if in_list == False:
                my_shopping_list.append(recipe_title)
                for ingredient in ingredients:
                    my_shopping_list.append(ingredient)
                print(f"\U0001F389 Success! {recipe_title.strip()} recipe ingredients saved to shopping list.")
                print()
            break
        else:
            print("Sorry, that wasn't an option. Try again.")
            print()


# The save_recipe function saves the most recently viewed recipe into my_recipes dictionary with the "recipe_title: recipe_link" as the "key: value" pair

def save_recipe():

    while True:
        
        save_recipe = input("Would you like to save this recipe for later? Enter yes or no: \n> ").lower().strip()
        print()

        if save_recipe == "n" or save_recipe == "no":
            break
        elif save_recipe == "y" or save_recipe == "yes":
            my_recipes[recipe_title.strip()] = recipe_link.strip()

            print(f"\U0001F389 Success: {recipe_title.strip()} saved to your recipes.")
            print()        

            save_ingredients()
            break
        else:
            print("Sorry, that wasn't an option. Try again.")
            print()

# The display_shopping_list function displays the current list items in my_shopping_list to the user 

def display_shopping_list():
    if my_shopping_list == []:
        print("No items in shopping list.")
    else:
        print("\U0001F4DD My Shopping List:")
        for item in my_shopping_list:
            print(f"{item}")
    print()

# The start_kitchen function starts up the program and walks the user through the navigation options throughout the program.

def main():

    welcome()

    while True:
        display_menu()

        select_menu = input("Enter menu option: \n> ").lower().strip()
        print()

        if select_menu == "q" or select_menu == "quit":
            say_goodbye()
            break
        elif select_menu == "v" or select_menu == "view":
            my_saved_recipes()
        elif select_menu == "g" or select_menu == "get":
            get_recipe()
            view_recipe()
            save_recipe()
        elif select_menu == "d" or select_menu == "display":
            display_shopping_list()
        else:
            print("Sorry, that wasn't an option. Try again.")
            print()

# checks to see if name of file matches to main; if so then call the main() function. This allows other programs to import the other functions from this file for their program to use.
if __name__ == "__main__":
    main()