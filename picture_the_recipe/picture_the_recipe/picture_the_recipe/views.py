from django.shortcuts import render
from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image
from io import BytesIO
from keras.models import model_from_json
from urllib.request import urlopen
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render

import sys, os, operator


def home(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')

def registration(request):
    return render(request, 'registration.html')

def errorimg(request):
    return render(request, 'error_incorrectimage.html')

def fileerror(request):
    return render(request, 'error_filenotuploaded.html')

def upload(request):
    return render(request,'fileupload.html')

def predictImage(request):
    print('hello')
    fileObj=request.FILES['myFile']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filepath=fs.url(filePathName)
    json_file = open("./models/food_model.json", "r")
    model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(model_json)
    # load weights into new model
    loaded_model.load_weights("./models/food_model.h5")
    print(filepath)
    img = image.load_img('.'+filepath, target_size=(64, 64))
    test=image.img_to_array(img)
    test=np.expand_dims(test, axis=0)
    result=loaded_model.predict(test)
    print(result)
    if (result[0][0]==1):
        outcome='Biryani'
    elif (result[0][1]==1):
        outcome='Burger'
    elif( result[0][2]==1):
        outcome='Chicken Wings'
    elif (result[0][3]==1):
        outcome='Pizza'
    else:
        outcome='Unable Determine'
    request.session['outcome']=outcome
    return render(request,'loader.html')


def searchresults(request):
    outcome=request.session['outcome']
    print(outcome)
    if outcome=='Burger':
        post={'header':'Burger','description':'A hamburger (also burger for short) is a sandwich consisting of one or more cooked patties of ground meat, usually beef, placed inside a sliced bread roll or bun','ingri':['1 pound ground lean (7% fat) beef','1 large egg','½ cup minced onion','¼ cup fine dried bread crumbs','1 tablespoon Worcestershire','1 or 2 cloves garlic, peeled and minced','About 1/2 teaspoon salt','About 1/4 teaspoon pepper','4 hamburger buns (4 in. wide), split','About 1/4 cup mayonnaise','About 1/4 cup ketchup','4 iceberg lettuce leaves, rinsed and crisped','1 firm-ripe tomato, cored and thinly sliced','4 thin slices red onion'],'nutri':['480 calories','calories from fat 43%','protein 31g','fat 23g','saturated fat 5.6g','carbohydrates 37g','fiber 2.4g','sodium 978mg','cholesterol 127mg'],'steps':['In a bowl, mix ground beef, egg, onion, bread crumbs, Worcestershire, garlic, 1/2 teaspoon salt, and 1/4 teaspoon pepper until well blended','Divide mixture into four equal portions and shape each into a patty about 4 inches wide','Lay burgers on an oiled barbecue grill over a solid bed of hot coals or high heat on a gas grill (you can hold your hand at grill level only 2 to 3 seconds),close lid on gas grill','Cook burgers, turning once, until browned on both sides and no longer pink inside (cut to test), 7 to 8 minutes total','Remove from grill.Lay buns, cut side down, on grill and cook until lightly toasted, 30 seconds to 1 minute.Spread mayonnaise and ketchup on bun bottoms','Add lettuce, tomato, burger, onion, and salt and pepper to taste. Set bun tops in place'],'imager':'https://media-cldnry.s-nbcnews.com/image/upload/newscms/2019_21/2870431/190524-classic-american-cheeseburger-ew-207p-2870431.jpg'}
    elif outcome=='Biryani':
        post={'header':'Biryani','description':'Long-grained rice (like basmati) flavored with fragrant spices such as saffron and layered with lamb, chicken, fish, or vegetables and a thick gravy','ingri':['1 tablespoon ghee (or vegetable oil)','1 1/2 pounds boneless, skinless chicken breasts, cut into 1" cubes','1 medium yellow onion, chopped','1 jalapeno pepper, seeded and minced','3 Tablespoons prepared ginger paste','2 teaspoons garam masala','1 teaspoon cumin','1 teaspoon turmeric','1 1/2 teaspoons salt','1 tablespoon minced garlic','2 large tomatoes, chopped','1/2 cup golden raisins','1 cup uncooked basmati rice','2 1/4 cups low-sodium chicken broth','1/4 cup chopped fresh cilantro leaves','1/4 cup sliced unsalted almonds','1 lime, cut into wedges'],'nutri':['567 Calories','Total Fat 18g','Saturated Fat 5g','Trans Fat 0g','Unsaturated Fat 12g','Cholesterol 153mg','Sodium 973mg','Carbohydrates 42g','Fiber 5g','Sugar 16g','Protein 61g'],'steps':['Heat the oil over medium-high heat in a large nonstick skillet or frying pan. Once the oil is shimmering, add the chicken pieces and let them cook, undisturbed, for 3-5 minutes until golden brown.','Turn the chicken pieces and add the onion, jalapeno, ginger, salt, garam masala, cumin, turmeric, and salt. Saute for 3 minutes, or until the onions have softened.','Add the garlic, tomatoes, and raisins to the pan. Stir well, then add the rice and broth. Allow the liquid to come to a boil, then cover the pan and turn the heat down to medium-low. Let the rice steam for 15 minutes. Turn off the heat and fluff the rice with a fork. Re-cover the pan, and allow the rice to continue to steam for another 10 minutes.','Garnish with cilantro leaves and almond slices. Serve the Biryani straight out of the pan, accompanied by lime wedges for squeezing.'],'imager':'https://myfoodstory.com/wp-content/uploads/2018/09/The-Best-Chicken-Biryani-Recipe-3.jpg'}
    elif outcome=='Pizza':
        post={'header':'Pizza','description':'Pizza, dish of Italian origin consisting of a flattened disk of bread dough topped with some combination of olive oil, oregano, tomato, olives, mozzarella or other cheese','ingri':['½ (12 ounce) can CONTADINA® Tomato Paste','1 teaspoon dried oregano, crushed','1 teaspoon dried basil, crushed','½ teaspoon garlic powder','½ teaspoon onion powder','½ teaspoon sugar','½ teaspoon salt','¼ teaspoon black pepper','3 ¼ cups all-purpose flour, or more as needed','2 (.25 ounce) envelopes Yeast','1 tablespoon sugar','1 ½ teaspoons salt','1 ⅓ cups very warm water (120 degrees F to 130 degrees F)','⅓ cup oil','1 (6 ounce) package HORMEL® Pepperoni','1 cup shredded mozzarella cheese, or more to taste'],'nutri':['590 calories','protein 19.5g','carbohydrates 60.4g','fat 29.1g','cholesterol 47.5mg','sodium 1408.3mg'],'steps':['For sauce: Combine all sauce ingredients with 1/2 cup water in a medium bowl; set aside for flavors to develop while making crust. Freeze remaining paste.','For crusts: Combine 2 cups of flour with the dry yeast, sugar and salt. Add the water and oil and mix until well blended (about 1 minute). Gradually add enough remaining flour slowly, until a soft, sticky dough ball is formed.','Knead for about 4 minutes, on a floured surface, until dough is smooth and elastic. Add more flour, if needed. (If using RapidRise® Yeast, let dough rest, covered, for 10 minutes.)','Divide dough in half. Pat each half (with floured hands) into a 12-inch greased pizza pan OR roll dough to fit pans.','For pizzas: Preheat oven to 425 degrees F. Top crusts with sauce, pepperoni and cheese.','Bake for 18 to 20 minutes until crusts are browned and cheese is bubbly. For best results, rotate pizza pans between top and bottom oven racks halfway through baking.'],'imager':'https://www.simplyrecipes.com/thmb/52FAbqwMY-ZDhx2ogNm8vpFx07M=/450x0/filters:no_upscale():max_bytes(150000):strip_icc()/__opt__aboutcom__coeus__resources__content_migration__simply_recipes__uploads__2019__09__easy-pepperoni-pizza-lead-4-82c60893fcad4ade906a8a9f59b8da9d.jpg'}
    elif outcome=='Chicken Wings':
        post={'header':'Chicken Wings','description':'chicken wings, or simply wings, deep-fried, unbreaded chicken wings or drums coated with a vinegar-and-cayenne-pepper hot sauce mixed with butter','ingri':['50 split chicken wings','¼ cup flour','salt & pepper to taste','1 tablespoon olive oil','Sauce','½ cup honey','4 tablespoons soy sauce','4 large garlic cloves crushed','1 tablespoon ginger finely diced','½ teaspoon chili flakes','⅓ cup water','1 teaspoon corn starch'],'nutri':['Calories: 290', 'Carbohydrates: 14g', 'Protein: 19g', 'Fat: 17g', 'Saturated Fat: 4g', 'Cholesterol: 77mg', 'Sodium: 410mg', 'Potassium: 180mg', 'Sugar: 11g'],'steps':['Preheat oven to 425°F. Dab wings with paper towels until completely dry','Toss wings with flour, salt and pepper. Remove any excess flour and brush with olive oil (or use an olive oil spray).','Line a pan with foil and then place parchment paper on top (you may need 2 pans) and bake 35 minutes turning at 20 minutes.','Meanwhile, combine sauce ingredients in a small pan. Bring to a boil, reduce heat and simmer about 10 minutes or until slightly thickened and sauce coats the back of a spoon.','Take wings from oven, toss with sauce and return to the oven for 10 minutes, turning after 5 minutes.','Allow to cool 10 minutes. As the sauce cools, it thickens. Stir the wings every few minutes to coat in the sauce as it thickens.'],'imager':'https://www.licious.in/blog/wp-content/uploads/2020/12/Fried-Chicken-Wing.jpg'}
    return render(request, 'searchresults.html',post)