import random

quotes = [
    "Life is what happens when youre busy making other plans." ,
    "In the middle of difficulty lies opportunity." ,
    "What we think, we become." ,
    "Happiness is a warm puppy." ,
    "For every minute you are angry you lose sixty seconds of happiness." ,
    "The happiness of your life depends on the quality of your thoughts." ,
    "We do not remember days; we remember moments." ,
    "Success is not the key to happiness. Happiness is the key to success." 
    "Dont watch the clock; do what it does. Keep going." 
    "Success is not in what you have, but who you are." 
    "Push yourself, because no one else is going to do it for you." 
    "Success doesnt just find you. You have to go out and get it." 
    "Wake up with determination. Go to bed with satisfaction." 
    "Dream it. Believe it. Build it." 
    "Its going to be hard, but hard does not mean impossible." 
    "What defines us is how well we rise after falling." 
    "You dont have to be rich to travel well." 
    "Life is short and the world is wide." 
    "The greatest adventure is what lies ahead." 
    "Lets find some beautiful place to get lost."
]
     
random.sample(quotes, 15)
with open("quotes.txt", "r") as file:
    quotes = file.readlines()