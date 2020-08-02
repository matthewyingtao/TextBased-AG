import random
from os import system
import math
from colorama import Fore, Style

tier_1 = {"Goblin": [5, 3, 1], "Slime": [10, 1, 0], "Zombie": [8, 1, 1]}

attacks = {
    "Slash": [3, 0.9, 0.1, 0],
    "Fireball": [4, 0.7, 0.25, 1],
    "Shock": [2, 1, 0.5, 1]
}

equips = {"Sword": [0, 0, 1, 0]}

implicits = {'Abrupt': [-1, 3, 1, 2], 'Adorable': [0, -1, 3, 2], 'Adventurous': [2, 3, 1, -1],
             'Aggressive': [1, 0, -1, 2], 'Agitated': [0, -1, 3, 2], 'Alert': [1, -1, 0, 2], 'Aloof': [-1, 1, 0, 3],
             'Amiable': [3, 0, 1, 2], 'Amused': [-1, 0, 3, 2], 'Annoyed': [0, 3, 1, 2], 'Antsy': [0, -1, 1, 2],
             'Anxious': [-1, 2, 3, 1], 'Appalling': [0, -1, 1, 3], 'Appetizing': [-1, 1, 2, 0],
             'Apprehensive': [1, 0, 2, 3], 'Arrogant': [3, 2, 1, -1], 'Ashamed': [-1, 3, 1, 2],
             'Astonishing': [1, 3, 2, 0], 'Attractive': [-1, 2, 0, 1], 'Average': [1, 3, -1, 2], 'Batty': [1, 0, -1, 3],
             'Beefy': [3, 0, -1, 2], 'Bewildered': [-1, 0, 2, 1], 'Biting': [0, -1, 1, 3], 'Bitter': [0, 2, -1, 3],
             'Bland': [1, -1, 0, 2], 'Blushing': [1, 3, 0, -1], 'Bored': [0, 1, 3, -1], 'Brave': [1, -1, 3, 2],
             'Bright': [2, 1, 0, 3], 'Broad': [0, 2, 1, -1], 'Bulky': [3, -1, 0, 2], 'Burly': [1, 0, 3, -1],
             'Charming': [1, 0, 2, 3], 'Cheeky': [2, 3, 0, 1], 'Cheerful': [1, 0, 2, 3], 'Chubby': [0, -1, 2, 3],
             'Clean': [0, 2, 1, -1], 'Clear': [3, -1, 1, 2], 'Cloudy': [1, 2, 3, -1], 'Clueless': [2, -1, 1, 0],
             'Clumsy': [-1, 2, 1, 3], 'Colorful': [0, 3, 2, 1], 'Colossal': [-1, 2, 0, 1], 'Combative': [0, 3, 1, 2],
             'Comfortable': [2, 0, 1, -1], 'Condemned': [1, 0, 3, -1], 'Condescending': [1, 3, 0, -1],
             'Confused': [2, 3, -1, 0], 'Contemplative': [2, 0, 1, 3], 'Convincing': [0, -1, 2, 1],
             'Convoluted': [1, -1, 2, 3], 'Cooperative': [3, 0, 2, -1], 'Corny': [0, 1, 3, 2], 'Costly': [2, 3, -1, 1],
             'Courageous': [2, -1, 0, 3], 'Crabby': [-1, 0, 3, 2], 'Creepy': [0, 2, 3, -1], 'Crooked': [2, 0, 3, -1],
             'Cruel': [3, 2, 1, 0], 'Cumbersome': [1, 0, 2, 3], 'Curved': [-1, 3, 1, 0], 'Cynical': [1, 2, 3, -1],
             'Dangerous': [2, -1, 3, 0], 'Dashing': [-1, 1, 2, 3], 'Decayed': [1, 3, 0, -1], 'Deceitful': [3, 1, 0, -1],
             'Deep': [2, 0, 3, 1], 'Defeated': [0, 2, 3, 1], 'Defiant': [3, 0, 1, -1], 'Delicious': [0, -1, 2, 3],
             'Delightful': [0, 1, 3, -1], 'Depraved': [3, 0, 1, 2], 'Depressed': [0, 3, 2, -1],
             'Despicable': [0, -1, 3, 2], 'Determined': [1, -1, 3, 2], 'Dilapidated': [-1, 2, 3, 0],
             'Diminutive': [1, 2, -1, 3], 'Disgusted': [0, -1, 3, 1], 'Distinct': [2, 1, 0, 3],
             'Distraught': [3, -1, 2, 0], 'Distressed': [2, -1, 1, 0], 'Disturbed': [2, 3, 1, 0],
             'Dizzy': [1, 3, -1, 2], 'Drab': [-1, 1, 0, 3], 'Drained': [-1, 3, 1, 2], 'Dull': [-1, 1, 2, 0],
             'Eager': [1, 3, 2, -1], 'Ecstatic': [2, 0, 3, 1], 'Elated': [0, 1, -1, 2], 'Elegant': [1, -1, 0, 3],
             'Emaciated': [0, 2, 3, 1], 'Embarrassed': [1, -1, 3, 2], 'Enchanting': [-1, 1, 3, 0],
             'Encouraging': [2, 3, 0, -1], 'Energetic': [0, 3, 1, -1], 'Enormous': [1, -1, 3, 0],
             'Enthusiastic': [2, 3, 1, 0], 'Envious': [3, 1, 0, 2], 'Exasperated': [1, 2, 0, -1],
             'Excited': [1, 3, 2, -1], 'Exhilarated': [0, 3, 1, 2], 'Extensive': [1, 3, 0, 2],
             'Exuberant': [1, 0, -1, 2], 'Fancy': [3, 1, -1, 2], 'Fantastic': [2, -1, 1, 0], 'Fierce': [1, 2, 3, -1],
             'Filthy': [0, 3, 1, 2], 'Flat': [2, 3, 0, -1], 'Floppy': [3, -1, 2, 1], 'Fluttering': [-1, 0, 3, 2],
             'Foolish': [2, 1, -1, 3], 'Frantic': [0, 2, -1, 1], 'Fresh': [2, 0, 3, -1], 'Friendly': [0, 1, 3, 2],
             'Frightened': [0, -1, 1, 3], 'Frothy': [0, 2, 3, -1], 'Frustrating': [1, 3, 2, 0], 'Funny': [1, 0, 3, -1],
             'Fuzzy': [1, 0, 3, 2], 'Gaudy': [1, 0, 3, 2], 'Gentle': [-1, 1, 2, 3], 'Ghastly': [2, 0, -1, 1],
             'Giddy': [-1, 3, 1, 2], 'Gigantic': [-1, 1, 2, 0], 'Glamorous': [-1, 1, 0, 3], 'Gleaming': [-1, 0, 1, 2],
             'Glorious': [0, -1, 3, 2], 'Gorgeous': [3, -1, 1, 2], 'Graceful': [-1, 0, 3, 2], 'Greasy': [1, 3, 2, -1],
             'Grieving': [-1, 1, 3, 2], 'Gritty': [2, 0, 1, -1], 'Grotesque': [-1, 1, 2, 3], 'Grubby': [1, -1, 2, 3],
             'Grumpy': [2, 1, -1, 3], 'Handsome': [2, -1, 1, 0], 'Happy': [1, -1, 0, 2], 'Harebrained': [2, 0, -1, 1],
             'Healthy': [2, 0, -1, 3], 'Helpful': [1, 0, 3, -1], 'Helpless': [2, 0, 1, 3], 'High': [1, 3, 0, -1],
             'Hollow': [3, 0, 1, -1], 'Homely': [3, 0, 2, 1], 'Horrific': [-1, 3, 0, 2], 'Huge': [2, 3, -1, 1],
             'Hungry': [1, 3, 0, -1], 'Hurt': [2, 3, -1, 0], 'Icy': [1, 0, 2, 3], 'Ideal': [1, 3, -1, 2],
             'Immense': [2, 0, 1, 3], 'Impressionable': [3, -1, 1, 0], 'Intrigued': [-1, 1, 2, 3],
             'Irate': [3, 0, 2, 1], 'Irritable': [1, 2, 3, 0], 'Itchy': [2, 0, 1, -1], 'Jealous': [2, 1, 3, -1],
             'Jittery': [1, 2, 0, -1], 'Jolly': [0, 1, 2, 3], 'Joyous': [3, -1, 2, 1], 'Juicy': [3, 2, -1, 1],
             'Jumpy': [2, -1, 1, 3], 'Kind': [-1, 2, 1, 0], 'Lackadaisical': [1, 0, 3, 2], 'Large': [1, -1, 2, 3],
             'Lazy': [1, -1, 3, 2], 'Lethal': [1, 2, 3, 0], 'Little': [-1, 2, 0, 3], 'Lively': [0, 2, -1, 3],
             'Livid': [1, -1, 2, 3], 'Lonely': [2, -1, 3, 1], 'Loose': [1, -1, 3, 0], 'Lovely': [0, 3, 1, -1],
             'Lucky': [1, 0, -1, 3], 'Ludicrous': [0, 3, -1, 1], 'Macho': [2, -1, 0, 3], 'Magnificent': [1, 3, -1, 2],
             'Mammoth': [1, 2, 0, 3], 'Maniacal': [1, 2, 3, -1], 'Massive': [2, 0, -1, 1], 'Melancholy': [1, 3, 0, 2],
             'Melted': [3, 0, -1, 2], 'Miniature': [2, 1, -1, 3], 'Minute': [1, 0, 3, 2], 'Mistaken': [3, -1, 2, 1],
             'Misty': [0, 2, 3, 1], 'Moody': [-1, 0, 2, 1], 'Mortified': [-1, 1, 2, 0], 'Motionless': [3, 2, 1, 0],
             'Muddy': [-1, 3, 0, 1], 'Mysterious': [0, 3, 1, -1], 'Narrow': [0, -1, 3, 2], 'Nasty': [1, -1, 3, 2],
             'Naughty': [-1, 2, 3, 0], 'Nervous': [2, -1, 0, 3], 'Nonchalant': [-1, 0, 3, 2],
             'Nonsensical': [0, -1, 2, 3], 'Nutritious': [-1, 1, 3, 0], 'Nutty': [2, -1, 3, 0],
             'Obedient': [-1, 1, 0, 3], 'Oblivious': [0, -1, 2, 3], 'Obnoxious': [0, -1, 2, 1], 'Odd': [-1, 1, 3, 0],
             'Old-fashioned': [0, 1, 2, 3], 'Outrageous': [3, 1, 0, -1], 'Panicky': [2, -1, 3, 1],
             'Perfect': [2, 3, -1, 1], 'Perplexed': [2, 1, -1, 3], 'Petite': [1, 0, 2, 3], 'Petty': [1, -1, 2, 3],
             'Plain': [-1, 3, 0, 1], 'Pleasant': [2, 1, -1, 0], 'Poised': [3, 1, -1, 0], 'Pompous': [2, 1, 0, -1],
             'Precious': [1, 2, 0, -1], 'Prickly': [2, -1, 3, 1], 'Proud': [1, 2, 0, -1], 'Pungent': [2, 0, 3, 1],
             'Puny': [3, 2, -1, 1], 'Quaint': [0, -1, 3, 1], 'Quizzical': [1, 2, 0, 3], 'Ratty': [2, 1, 3, -1],
             'Reassured': [3, 2, 0, 1], 'Relieved': [1, 0, 2, 3], 'Repulsive': [1, -1, 0, 3],
             'Responsive': [0, 2, 3, 1], 'Ripe': [2, 0, 1, 3], 'Robust': [2, 1, 0, -1], 'Rotten': [1, 0, 2, -1],
             'Rotund': [1, 2, 3, 0], 'Rough': [0, 3, -1, 2], 'Round': [2, 3, -1, 0], 'Salty': [0, 2, -1, 1],
             'Sarcastic': [1, 2, -1, 3], 'Scant': [-1, 0, 3, 2], 'Scary': [0, 3, 2, -1], 'Scattered': [-1, 1, 3, 0],
             'Scrawny': [1, 3, 0, 2], 'Selfish': [1, 3, -1, 0], 'Shaggy': [1, -1, 3, 0], 'Shaky': [2, -1, 3, 1],
             'Shallow': [0, 2, -1, 1], 'Sharp': [3, 0, 2, 1], 'Shiny': [-1, 3, 1, 2], 'Short': [-1, 3, 0, 2],
             'Silky': [-1, 3, 2, 0], 'Silly': [3, -1, 2, 1], 'Skinny': [1, 0, 3, -1], 'Slimy': [-1, 2, 0, 3],
             'Slippery': [3, -1, 0, 2], 'Small': [0, 1, 2, -1], 'Smarmy': [-1, 0, 2, 3], 'Smiling': [2, 1, 0, 3],
             'Smoggy': [1, -1, 0, 3], 'Smooth': [0, 2, 3, 1], 'Smug': [3, 1, -1, 0], 'Soggy': [3, 2, 1, 0],
             'Solid': [2, 1, 0, -1], 'Sore': [1, 0, 3, -1], 'Sour': [-1, 2, 1, 0], 'Sparkling': [1, 3, -1, 2],
             'Spicy': [1, 3, 2, 0], 'Splendid': [1, 3, 0, 2], 'Spotless': [-1, 1, 2, 3], 'Square': [1, 2, -1, 3],
             'Stale': [0, -1, 3, 2], 'Steady': [3, 1, -1, 0], 'Steep': [-1, 2, 3, 0], 'Sticky': [0, 2, -1, 1],
             'Stormy': [-1, 0, 2, 1], 'Stout': [3, 0, 2, -1], 'Straight': [-1, 2, 0, 3], 'Strange': [1, 0, -1, 3],
             'Strong': [0, 2, 1, -1], 'Stunning': [1, 0, 2, -1], 'Substantial': [3, 0, -1, 1],
             'Successful': [-1, 3, 2, 0], 'Succulent': [0, -1, 3, 1], 'Superficial': [2, 1, -1, 0],
             'Superior': [0, -1, 3, 1], 'Swanky': [0, -1, 3, 2], 'Sweet': [-1, 1, 0, 3], 'Tart': [2, 3, 0, 1],
             'Tasty': [-1, 0, 3, 2], 'Teeny': [0, 2, -1, 3], 'Tender': [3, 0, -1, 2], 'Tense': [3, -1, 2, 0],
             'Terrible': [2, 1, 0, -1], 'Testy': [-1, 1, 2, 3], 'Thankful': [3, 2, -1, 1], 'Thick': [2, 3, 1, 0],
             'Thoughtful': [3, -1, 1, 0], 'Thoughtless': [3, -1, 1, 2], 'Tight': [1, 3, -1, 0], 'Timely': [0, 1, 2, -1],
             'Tricky': [2, -1, 3, 1], 'Trite': [0, 2, 1, 3], 'Troubled': [2, -1, 1, 0], 'Uneven': [1, 2, 3, 0],
             'Unsightly': [3, 1, 0, 2], 'Upset': [1, 0, 3, 2], 'Uptight': [0, -1, 2, 1], 'Vast': [-1, 3, 0, 1],
             'Vexed': [3, -1, 2, 1], 'Victorious': [2, -1, 3, 1], 'Virtuous': [3, 1, 2, -1], 'Vivacious': [0, -1, 3, 1],
             'Vivid': [-1, 3, 1, 2], 'Wacky': [3, 0, 2, -1], 'Weary': [1, -1, 3, 0], 'Whimsical': [-1, 2, 0, 1],
             'Whopping': [0, -1, 2, 1], 'Wicked': [-1, 0, 1, 2], 'Witty': [2, 3, 0, -1], 'Wobbly': [1, -1, 0, 3],
             'Wonderful': [2, 0, 3, -1], 'Worried': [-1, 0, 1, 2], 'Yummy': [2, 3, -1, 1], 'Zany': [-1, 3, 1, 0],
             'Zealous': [2, 0, 1, -1], 'Zippyadorable': [0, -1, 2, 1], 'Acrobatic': [0, -1, 2, 3],
             'Adaptable': [3, 2, -1, 0], 'Agile': [-1, 3, 2, 1], 'Arboreal': [2, 3, 0, 1], 'Ardent': [-1, 0, 2, 3],
             'Artful': [-1, 1, 0, 3], 'Astute': [0, 1, 2, 3], 'Attentive': [3, 0, 1, 2], 'Authentic': [1, -1, 3, 0],
             'Avid': [1, 0, 3, 2], 'Beardless': [-1, 0, 3, 1], 'Benevolent': [1, 2, 0, -1], 'Bionic': [2, 3, -1, 1],
             'Blissful': [3, -1, 0, 2], 'Bodacious': [-1, 0, 2, 1], 'Brilliant': [3, 2, 1, 0], 'Bubbly': [-1, 2, 3, 1],
             'Careful': [3, 2, 1, 0], 'Cautious': [0, 3, -1, 1], 'Circumspect': [2, 0, 3, -1],
             'Cognizant': [3, 1, -1, 2], 'Collectible': [0, 3, 1, -1], 'Communicative': [-1, 3, 0, 2],
             'Compact': [0, -1, 2, 1], 'Compassionate': [1, -1, 2, 3], 'Constant': [0, 3, 2, -1],
             'Convivial': [0, 1, -1, 3], 'Cordial': [0, -1, 3, 1], 'Cosmic': [-1, 2, 0, 3], 'Creative': [-1, 1, 2, 3],
             'Cryptic': [2, 1, 0, 3], 'Crystalline': [1, 3, 2, 0], 'Cunning': [-1, 0, 2, 3], 'Curious': [1, 3, 2, 0],
             'Dancing': [3, 2, 1, 0], 'Daring': [2, -1, 0, 3], 'Dauntless': [0, 1, 3, 2], 'Dazzling': [1, 3, -1, 0],
             'Dexterous': [1, 0, -1, 2], 'Discerning': [0, 2, -1, 1], 'Distinctive': [0, 1, 3, 2],
             'Dreaming': [1, 3, -1, 2], 'Dynamic': [-1, 3, 0, 1], 'Earnest': [1, 3, -1, 0], 'Easygoing': [-1, 0, 1, 3],
             'Eccentric': [2, 0, 1, -1], 'Effervescent': [3, 2, 1, -1], 'Elaborate': [2, -1, 0, 1],
             'Eloquent': [3, -1, 1, 2], 'Elusive': [-1, 0, 1, 2], 'Energized': [0, 2, 1, -1], 'Erudite': [0, 3, -1, 1],
             'Essential': [0, 2, 1, 3], 'Ethereal': [3, 1, 2, 0], 'Extraordinary': [-1, 1, 2, 3],
             'Exotic': [3, -1, 1, 2], 'Fearless': [1, 0, 2, 3], 'Feisty': [2, 3, 1, 0], 'Fiery': [-1, 0, 2, 3],
             'Flourishing': [3, -1, 1, 0], 'Flying': [-1, 1, 0, 3], 'Focused': [3, -1, 2, 0],
             'Fortunate': [2, -1, 3, 0], 'Frolicking': [1, 2, -1, 3], 'Gargantuan': [2, 0, -1, 1],
             'Gesticulating': [0, 1, 3, -1], 'Gleeful': [-1, 3, 1, 2], 'Grateful': [3, 2, 1, 0],
             'Gregarious': [3, 2, 1, -1], 'Harmonious': [3, 0, 1, -1], 'Hatless': [2, 3, 1, -1],
             'Heroic': [3, 0, 2, -1], 'Hydraulic': [0, 3, 1, -1], 'Idealistic': [0, 3, 2, -1],
             'Illustrious': [0, -1, 1, 2], 'Imaginative': [0, 1, -1, 2], 'Impartial': [0, 3, 2, -1],
             'Imperturbable': [2, 1, 3, 0], 'Improbable': [3, 2, -1, 1], 'Incredible': [1, 0, -1, 3],
             'Inimitable': [3, 1, 0, 2], 'Influential': [2, 1, 0, 3], 'Inquisitive': [2, -1, 0, 1],
             'Insightful': [-1, 0, 2, 1], 'Inspired': [0, 2, 3, -1], 'Intrepid': [0, 2, -1, 1],
             'Intricate': [-1, 1, 3, 2], 'Intuitive': [3, 0, 2, 1], 'Invaluable': [3, -1, 0, 1],
             'Inventive': [-1, 0, 1, 2], 'Jaunty': [-1, 3, 0, 2], 'Joyful': [3, -1, 1, 0], 'Jubilant': [1, 2, -1, 0],
             'Jumping': [0, 1, -1, 3], 'Keen': [2, 1, 0, -1], 'Laughing': [0, -1, 3, 1], 'Legendary': [0, 3, 1, 2],
             'Lenient': [-1, 0, 2, 1], 'Loquacious': [3, 2, -1, 1], 'Luminescent': [2, -1, 0, 1],
             'Magnetic': [3, 0, -1, 2], 'Majestic': [3, 2, -1, 1], 'Marvelous': [-1, 0, 1, 3], 'Masked': [-1, 1, 2, 0],
             'Mechanical': [-1, 3, 1, 0], 'Mercurial': [0, 3, -1, 1], 'Meritorious': [0, 2, -1, 1],
             'Merry': [3, 1, 2, -1], 'Methodical': [-1, 1, 3, 2], 'Meticulous': [1, 3, -1, 0], 'Mighty': [0, 3, -1, 1],
             'Mirthful': [3, 1, -1, 2], 'Mischievous': [2, 1, 0, 3], 'Modest': [3, 1, 0, 2], 'Momentous': [3, 0, 2, 1],
             'Multicolored': [2, 0, -1, 3], 'Murmuring': [-1, 1, 2, 0], 'Musical': [1, -1, 3, 0],
             'Mustachioed': [-1, 3, 1, 2], 'Nascent': [-1, 0, 3, 2], 'Neighborly': [0, 1, 3, -1],
             'Noble': [0, 3, 1, -1], 'Nomadic': [0, -1, 1, 3], 'Noncommittal': [2, -1, 3, 0],
             'Observant': [3, 2, 1, -1], 'Omnidirectional': [-1, 2, 0, 3], 'Omnivorous': [3, -1, 0, 1],
             'Optimal': [3, 2, 1, -1], 'Optimistic': [2, 3, 1, -1], 'Otherworldly': [3, 2, 1, 0],
             'Outgoing': [3, 0, 1, -1], 'Outspoken': [1, -1, 0, 3], 'Panoramic': [0, -1, 2, 3],
             'Peaceful': [2, -1, 0, 3], 'Perceptive': [-1, 1, 0, 3], 'Perpetual': [3, 1, 0, 2],
             'Perplexing': [1, 2, 0, 3], 'Perspicacious': [-1, 3, 1, 2], 'Philosophical': [2, -1, 1, 3],
             'Picturesque': [2, -1, 0, 3], 'Playful': [-1, 0, 3, 1], 'Practical': [-1, 3, 0, 1],
             'Precise': [2, 0, -1, 1], 'Precocious': [-1, 2, 0, 1], 'Prestigious': [2, -1, 0, 1],
             'Primeval': [2, 1, 0, -1], 'Primordial': [2, 1, 0, -1], 'Prismatic': [3, 0, 1, 2],
             'Proactive': [3, 1, -1, 2], 'Proficient': [-1, 0, 3, 2], 'Prototypical': [1, 3, -1, 2],
             'Prudent': [3, -1, 0, 2], 'Purposeful': [0, 1, 2, 3], 'Qualified': [3, 2, 0, 1], 'Quotable': [2, 1, 0, -1],
             'Radiant': [-1, 0, 2, 1], 'Reclusive': [1, 2, 3, -1], 'Recurring': [-1, 3, 2, 1],
             'Reflective': [-1, 3, 1, 2], 'Rejoicing': [2, 0, 3, -1], 'Relaxed': [-1, 3, 1, 2],
             'Remarkable': [2, 1, 0, -1], 'Renowned': [-1, 1, 0, 3], 'Resilient': [0, -1, 3, 1],
             'Resolute': [3, 0, 1, -1], 'Resourceful': [-1, 2, 1, 3], 'Rigorous': [1, 0, 2, -1],
             'Roaring': [-1, 0, 1, 3], 'Salient': [3, -1, 2, 1], 'Salubrious': [0, 2, 3, -1], 'Sanguine': [3, -1, 2, 1],
             'Sapient': [1, 2, 3, -1], 'Satisfied': [0, -1, 3, 1], 'Scholarly': [2, 0, -1, 3],
             'Scintillating': [-1, 1, 0, 2], 'Scrupulous': [2, -1, 0, 3], 'Selective': [0, 2, -1, 1],
             'Sincere': [1, 2, -1, 3], 'Singing': [3, -1, 1, 0], 'Sleek': [-1, 0, 3, 1], 'Sleepy': [1, 2, 3, -1],
             'Sophisticated': [-1, 2, 3, 0], 'Spectacular': [2, 3, 1, 0], 'Squeaky': [2, 0, -1, 1],
             'Stately': [1, 2, 3, -1], 'Strategic': [0, -1, 2, 3], 'Striped': [0, 3, -1, 1],
             'Stupendous': [3, 0, 1, -1], 'Stylish': [-1, 2, 1, 0], 'Sufficient': [0, 3, -1, 2],
             'Swimming': [3, 2, 0, 1], 'Symbolic': [1, 2, 0, 3], 'Symmetrical': [0, 1, 3, -1],
             'Taciturn': [-1, 1, 0, 3], 'Terrestrial': [1, -1, 0, 3], 'Tessellated': [2, 1, -1, 3],
             'Theoretical': [1, 2, 0, -1], 'Thriving': [-1, 3, 0, 2], 'Timeless': [0, 3, -1, 2],
             'Topographical': [2, 1, 3, -1], 'Transparent': [0, 2, 3, -1], 'Tranquil': [1, 0, 2, -1],
             'Ubiquitous': [0, 3, -1, 1], 'Uncanny': [1, 2, -1, 3], 'Unclouded': [2, -1, 1, 0],
             'Undisputed': [-1, 1, 3, 0], 'Unexpected': [-1, 2, 3, 1], 'Unfathomable': [2, 3, 0, -1],
             'Unflappable': [0, 1, 3, 2], 'Unique': [1, 3, 0, -1], 'Universal': [2, 0, -1, 1],
             'Unofficial': [2, 3, 0, -1], 'Unseen': [-1, 1, 3, 0], 'Unthinkable': [-1, 1, 2, 0],
             'Uproarious': [1, -1, 0, 2], 'Variegated': [2, -1, 0, 1], 'Versatile': [-1, 1, 3, 0],
             'Vigilant': [0, 1, 3, -1], 'Vigorous': [1, 0, 3, 2], 'Vociferous': [1, 3, 0, 2],
             'Wandering': [0, 1, 3, -1], 'Watchful': [0, 3, 1, -1], 'Windswept': [2, -1, 1, 0],
             'Wondrous': [3, 0, 2, 1], 'Zestful': [-1, 2, 3, 0]}

implicits_list = list(implicits.keys())

attacks_list = list(attacks.keys())

monster_multiplier_limit = [0.8, 1.2]


def color_print(color, *args):
    print(f"{color}")
    for string in args:
        print(string)
    print(f"{Style.RESET_ALL}")


def damage_calc(attacker, move, defender):
    print(Fore.RED)
    # get random float between 0-1 and check for miss
    miss = random.random()
    if miss < attacks.get(move)[1]:
        damage = (attacker.attack + attacks.get(move)[0]) - defender.defence
        # get random float between 0-1 and check for critical hit, doubles damage if true
        critical_hit = random.random()
        if critical_hit < attacks.get(move)[2]:
            damage *= 2
            color_print(Fore.GREEN, "Critical Hit!")
        # calculate damage
        try:
            defender.health[0] -= damage
        except:
            defender.health -= damage
        print(
            f"{attacker.name} used {move} and dealt {damage} damage to {defender.name}"
        )
    else:
        print("Miss!")
    print(Style.RESET_ALL)


def attack_check():
    print(f"{Style.RESET_ALL}")
    for index, action in enumerate(attacks.keys()):
        print(f"-{index + 1}- {action}")
    while True:
        try:
            selection = int(input()) - 1
            if selection < 0 or selection > (len(attacks) - 1):
                color_print(Fore.RED, "that's not a valid number!")
            elif player.mana[0] - attacks.get(attacks_list[selection])[3] < 0:
                color_print(Fore.RED, "not enough mana!")
            else:
                break
        except:
            color_print(Fore.RED, "that's not a valid number!")
    print("hi2")
    player.mana[0] -= attacks.get(attacks_list[selection])[3]
    print(Style.RESET_ALL)
    return selection


def battle(combat_monster):
    print(f"You are fighting a {combat_monster.name}")
    while combat_monster.health > 0 and player.health[0] > 0:
        damage_calc(player, attacks_list[attack_check()], combat_monster)
        if combat_monster.health > 0:
            damage_calc(combat_monster, attacks_list[0], player)
    if combat_monster.health < 0:
        color_print(Fore.GREEN, f"You have defeated {combat_monster.name}")
        player.xp[0] += combat_monster.xp
        player.xp_check()
    elif player.health[0] < 0:
        color_print(Fore.RED, f"{combat_monster.name} has defeated you")


def get_base_stats(item_type):
    base_stats = equips.get(item_type)
    return base_stats


class Equipment:
    def __init__(self, material, equip_type):
        self.name = material + " " + equip_type
        base_stats = get_base_stats(equip_type)
        self.health = base_stats[0]
        self.mana = base_stats[1]
        self.attack = base_stats[2]
        self.defence = base_stats[3]
        self.mod = "None"
        self.mod_effect = [0, 0, 0, 0]
        self.isEquipped = False
        player.inventory.append(self)

    def remove_mod(self):
        self.name = self.name[len(self.mod) + 1:]
        self.health -= self.mod_effect[0]
        self.mana -= self.mod_effect[1]
        self.attack -= self.mod_effect[2]
        self.defence -= self.mod_effect[3]
        self.mod = None
        self.mod_effect = [0, 0, 0, 0]

    def roll_mod(self):
        self.remove_mod()
        self.mod = implicits_list[random.randint(0, len(implicits_list) - 1)]
        self.mod_effect = implicits.get(self.mod)
        self.name = f"{self.mod} {self.name}"
        self.health += self.mod_effect[0]
        self.mana += self.mod_effect[1]
        self.attack += self.mod_effect[2]
        self.defence += self.mod_effect[3]

    def stats(self):
        self.attributes = vars(self)
        self.attributes_keys = list(self.attributes.keys())
        self.attributes_keys.pop()
        print(f"{Fore.GREEN}STATS:")
        for attribute in self.attributes_keys:
            print(
                f"{(attribute.replace('_', ' ').upper())}: {self.attributes.get(attribute)}"
            )
        del self.attributes
        del self.attributes_keys
        print(Style.RESET_ALL)


class Character:
    def __init__(self):
        self.name = input("what is your name? \n")
        system("clear")
        self.health = [10, 10]
        self.mana = [5, 5]
        self.attack = 3
        self.defence = 0
        self.xp = [0, 50]
        self.level = 1
        self.inventory = []

    def stats(self):
        self.attributes = vars(self)
        self.attributes_keys = list(self.attributes.keys())
        self.attributes_keys.pop()
        self.attributes_keys.pop()
        print(f"{Fore.GREEN}STATS:")
        for attribute in self.attributes_keys:
            print(
                f"{(attribute.replace('_', ' ').upper())}: {self.attributes.get(attribute)}"
            )
        del self.attributes
        del self.attributes_keys
        print(Style.RESET_ALL)

    def level_up(self):
        points = 3
        while points > 0:
            allocate = int("Allocate points:\n"
                           "-1- HEALTH\n"
                           "-2- MANA\n"
                           "-3- ATTACK\n"
                           "-4- DEFENCE\n")
            if allocate == 1:
                self.health += 1
            if allocate == 2:
                self.mana += 1
            if allocate == 3:
                self.attack += 1
            if allocate == 4:
                self.defence += 1

    def xp_check(self):
        if self.xp[0] > self.xp[1]:
            self.level += 1
            self.xp[0] -= self.xp[1]
            # XP to next level follows a logarithmic curve base 10 multiplier.
            self.xp[1] = round((math.log(self.level, 10) + 1) * self.xp[1], 0)
            color_print(Fore.GREEN, "You've leveled up!")

    def show_inventory(self):
        print("INVENTORY:")
        inventory_names = []
        for item in self.inventory:
            inventory_names.append(item.name)
        print(inventory_names)
        while True:
            try:
                select_item = int(
                    input("What would you like to do? \n"
                          "-1- Re-roll modifier\n"
                          "-2- Equip item\n"
                          "-3- Exit\n"))
                if select_item == 1:
                    remove_choice = int(input("Which item?\n")) - 1
                    if self.inventory[remove_choice].isEquipped:
                        color_print(Fore.RED, "Can't re-roll while equipped")
                    else:
                        self.inventory[remove_choice].roll_mod()
                        self.inventory[remove_choice].stats()
                        color_print(Fore.GREEN, "Mod re-rolled\n")
                elif select_item == 2:
                    equip_choice = int(input("Which item\n")) - 1
                    self.equip_item(self.inventory[equip_choice])
                elif select_item == 3:
                    system("clear")
                    break
                else:
                    color_print(Fore.RED, "that's not a valid number!\n")
            except:
                color_print(Fore.RED, "that's not a valid number!\n")

    def equip_item(self, item):
        if item.isEquipped:
            self.health[1] -= item.health
            self.mana[1] -= item.mana
            self.attack -= item.attack
            self.defence -= item.defence
            item.isEquipped = False
            print(f"You have unequipped {item.name}")
        else:
            self.health[0] += item.health
            self.health[1] += item.health
            self.mana[0] += item.mana
            self.mana[1] += item.mana
            self.attack += item.attack
            self.defence += item.defence
            item.isEquipped = True
            print(f"You have equipped {item.name}")


class Monster:
    def __init__(self, tier):
        self.name = random.choice(list(tier))
        self.multiplier = round(
            random.uniform(monster_multiplier_limit[0],
                           monster_multiplier_limit[1]), 1)
        self.health = round(tier.get(self.name)[0] * self.multiplier)
        self.attack = round(tier.get(self.name)[1] * (1 / self.multiplier))
        self.defence = tier.get(self.name)[2]
        self.xp = random.randint(20, 40)


player = Character()

dog = Equipment("Iron", "Sword")
dog.roll_mod()
dog.stats()

player.stats()

while player.health[0] > 0:
    try:
        choice = int(
            input("What would you like to do? \n"
                  "-1- Adventure \n"
                  "-2- Go to an inn \n"
                  "-3- View inventory\n"))
        if choice == 1:
            monster = Monster(tier_1)
            battle(monster)
            player.stats()
        elif choice == 2:
            player.health[0] = player.health[1]
            player.mana[0] = player.mana[1]
            player.stats()
        elif choice == 3:
            player.show_inventory()
        else:
            color_print(Fore.RED, "that's not a valid number!")
    except:
        color_print(Fore.RED, "that's not a valid number!")

print("Game Over")
