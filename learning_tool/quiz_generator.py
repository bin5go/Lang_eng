"""
quiz_generator.py — Vocabulary quiz generator for Great Writing 2
Usage:
    python quiz_generator.py             # generates quiz_01.md (words 1-15 by page asc)
    python quiz_generator.py --quiz 3    # generates quiz_03.md (words 31-45)
    python quiz_generator.py --list      # list all quiz groups
"""

import json
import argparse
from pathlib import Path

DATA_FILE = Path(__file__).parent / "words_gw2.json"

# ---------------------------------------------------------------------------
# Section B — Fill-in-the-blank sentences (word removed, student fills blank)
# ---------------------------------------------------------------------------

FILL_IN_SENTENCES = {
    "a great deal (of)": "She spent ___ time preparing for the presentation.",
    "abroad": "Many students dream of studying ___.",
    "accomplish": "It takes hard work to ___ your goals.",
    "accurately": "Please read the instructions ___ before starting the test.",
    "addictive": "Social media can be very ___ for teenagers.",
    "advantage": "Being bilingual gives you a big ___ in many careers.",
    "advertising": "The company spent millions on ___ its new product.",
    "affect": "Lack of sleep can ___ your concentration at school.",
    "amazed": "The audience was ___ by the magician's tricks.",
    "ancient": "Historians study ___ civilizations to understand the past.",
    "apply": "You should ___ for the scholarship before the deadline.",
    "approximately": "The journey takes ___ three hours by train.",
    "assign": "The teacher will ___ different topics to each group.",
    "assistance": "She asked for ___ when she couldn't open the jar.",
    "at an angle": "The tower in Pisa leans ___ because of soft ground.",
    "at least": "You should drink ___ eight glasses of water a day.",
    "attraction": "The Eiffel Tower is a major tourist ___ in Paris.",
    "available": "The tickets are not ___ online; you must buy them in person.",
    "ban": "The city decided to ___ plastic bags from all supermarkets.",
    "basic": "Cooking rice is a ___ skill everyone should learn.",
    "benefit": "Regular exercise is a great ___ for mental health.",
    "bilingual": "Growing up in two cultures made her naturally ___.",
    "billion": "The world population has exceeded eight ___.",
    "boil": "You need to ___ the water before adding the pasta.",
    "calculate": "Use a calculator to ___ the total cost.",
    "casually": "He was dressed ___ in jeans and a T-shirt.",
    "claim": "The company ___ their product cures headaches.",
    "come up to": "The water in the lake ___ his waist.",
    "common sense": "You don't need a rulebook — just use ___.",
    "communication": "Good ___ is essential in any team.",
    "complain": "The customer called to ___ about the late delivery.",
    "concentrate": "It's hard to ___ when there is too much noise.",
    "confuse": "The complicated instructions ___ most students.",
    "connection": "There is a clear ___ between diet and health.",
    "construction": "The ___ of the new bridge will take two years.",
    "contest": "She entered a writing ___ and won first prize.",
    "continent": "Africa is the second-largest ___ in the world.",
    "contrast": "In ___ to summer, winter nights are very long.",
    "contribution": "Everyone should make a ___ to keeping the classroom clean.",
    "convenient": "Living near a bus stop is very ___ for daily travel.",
    "convince": "She tried to ___ her parents to let her stay out late.",
    "culture": "Learning a language also means learning about its ___.",
    "current": "The ___ situation requires everyone to stay calm.",
    "customer": "The shop assistant helped every ___ with a smile.",
    "damage": "The storm caused serious ___ to the roof.",
    "deadly": "The scientist discovered a ___ virus in the jungle.",
    "debt": "He worked two jobs to pay off his ___.",
    "decade": "Smartphones have changed society in less than a ___.",
    "depend (on)": "The outcome will ___ how well you prepare.",
    "destination": "Paris is a popular holiday ___ for many tourists.",
    "destroy": "The fire threatened to ___ the entire forest.",
    "differ": "Opinions on this topic ___ widely among experts.",
    "disagree": "It is normal for friends to sometimes ___.",
    "discovery": "The ___ of penicillin saved millions of lives.",
    "diverse": "The city has a ___ population from many countries.",
    "divide": "The teacher will ___ the class into groups of four.",
    "divided": "Opinion was ___ on whether to change the school uniform.",
    "document": "Always ___ your sources when writing an essay.",
    "due to": "___ bad weather, the match was postponed.",
    "economy": "Tourism plays an important role in the country's ___.",
    "educational": "Visiting museums is both fun and ___.",
    "effective": "This new method is more ___ than the old one.",
    "embarrassing": "Forgetting someone's name is always ___.",
    "empty": "The classroom was ___ when I arrived early.",
    "entire": "She read the ___ book in one day.",
    "exceed": "Your essay must not ___ 500 words.",
    "experiment": "The scientist ran an ___ to test her hypothesis.",
    "expression": "\"Break a leg\" is a common English ___ for good luck.",
    "extremely": "The exam was ___ difficult this year.",
    "final": "This is your ___ chance to improve your grade.",
    "flood": "The heavy rain caused a ___ in the lower part of town.",
    "focus": "Try to ___ on one task at a time.",
    "former": "The ___ president gave a speech at the ceremony.",
    "freedom": "___ of speech is an important human right.",
    "frequently": "She ___ goes to the library after school.",
    "frighten": "Loud thunder can ___ young children.",
    "function": "The main ___ of the heart is to pump blood.",
    "generally": "Students ___ find science interesting when it is hands-on.",
    "get over": "It took her weeks to ___ the flu.",
    "guest": "We prepared a special meal for our ___.",
    "hide": "The cat likes to ___ under the bed.",
    "highly": "The book is ___ recommended by all the teachers.",
    "imagine": "Can you ___ life without electricity?",
    "immigrant": "Her grandparents were ___ who arrived with very little money.",
    "improve": "Practice every day to ___ your pronunciation.",
    "in advance": "Book your tickets ___ to get a better price.",
    "in shape": "She goes jogging every morning to stay ___.",
    "increase": "The number of electric cars continues to ___.",
    "ingredient": "Sugar is the main ___ in most desserts.",
    "injure": "He fell off his bike and ___ his knee.",
    "interact": "Social skills help you ___ confidently with others.",
    "invention": "The ___ of the printing press changed history.",
    "keep track (of)": "Use a notebook to ___ your new vocabulary.",
    "laundry": "She does her ___ every Sunday morning.",
    "likely": "It is ___ to rain tomorrow, so bring an umbrella.",
    "limited": "The school has ___ resources, so students share textbooks.",
    "location": "The hotel has a perfect ___ near the beach.",
    "maintain": "It is important to ___ a healthy lifestyle.",
    "majority": "The ___ of students prefer shorter homework assignments.",
    "manage": "She somehow managed to ___ three projects at once.",
    "mayor": "The ___ gave a speech at the opening of the new park.",
    "messy": "His bedroom is always ___, with clothes on the floor.",
    "motivation": "A good teacher can increase students' ___ to learn.",
    "multiply": "If you ___ six by seven, you get forty-two.",
    "no matter": "___ how hard it is, never give up.",
    "obtain": "You must ___ permission before using someone's photos.",
    "occasionally": "She ___ forgets to bring her homework.",
    "occupation": "Teaching is a very rewarding ___.",
    "old-fashioned": "Some people think handwriting letters is ___.",
    "on purpose": "He didn't break the vase ___ — it was an accident.",
    "opportunity": "Studying abroad is a great ___ to improve your language skills.",
    "option": "If the first choice doesn't work, there is always another ___ to consider.",
    "organized": "An ___ student always knows when assignments are due.",
    "ought to": "You ___ apologise if you hurt someone's feelings.",
    "outweigh": "The benefits of exercise clearly ___ the effort required.",
    "patient": "Good doctors are always calm and ___ with their patients.",
    "peaceful": "Early mornings in the countryside feel very ___.",
    "perfectly": "She understood the instructions ___ clearly.",
    "performance": "Her ___ in the school play was outstanding.",
    "polluted": "The river became ___ after the factory opened nearby.",
    "population": "The ___ of the capital city is over ten million.",
    "position": "Sitting in an uncomfortable ___ can hurt your back.",
    "powerful": "Wind is a ___ and clean source of energy.",
    "prevent": "Washing your hands regularly can ___ the spread of germs.",
    "private": "She kept a ___ diary that no one else could read.",
    "produce": "Farms in this region ___ most of the country's rice.",
    "profit": "The company made a large ___ last year.",
    "protective": "Parents are naturally ___ of their young children.",
    "provide": "The school will ___ all the materials you need.",
    "quality": "Always choose ___ over quantity.",
    "range": "The store offers a wide ___ of sports equipment.",
    "reach": "Can you ___ the top shelf, or should I get a ladder?",
    "recognize": "I didn't ___ him at first because of his new haircut.",
    "recommend": "I would ___ this restaurant to anyone who loves Italian food.",
    "reduce": "Turn off lights to ___ energy consumption.",
    "regardless of": "___ the weather, the match will go ahead.",
    "region": "Rice is the main food in this ___ of Asia.",
    "regional": "The team won the ___ championship for the third year in a row.",
    "relationship": "A good ___ with your teacher helps you learn more.",
    "remarkable": "The young pianist gave a truly ___ performance.",
    "remind": "Please ___ me to submit the form before Friday.",
    "replace": "When a light bulb breaks, you need to ___ it.",
    "require": "This task will ___ a lot of concentration.",
    "research": "Scientists do ___ to find cures for diseases.",
    "resident": "Every ___ of the building must register their name.",
    "respected": "She is a highly ___ scientist in her field.",
    "rural": "Many young people move from ___ areas to the city.",
    "score": "He studied hard to get a high ___ on the test.",
    "select": "Please ___ the correct answer from the options below.",
    "shade": "We sat in the ___ of a tree to escape the heat.",
    "shocked": "Everyone was ___ when the favourite team lost.",
    "similar": "The two paintings look very ___ at first glance.",
    "site": "The construction ___ is not open to the public.",
    "spill": "Be careful not to ___ your drink on the keyboard.",
    "spot": "This is the perfect ___ for a picnic.",
    "strategy": "She developed a clear ___ for improving her grades.",
    "style": "Her writing ___ is easy to read and enjoyable.",
    "submit": "Remember to ___ your assignment by midnight.",
    "suitable": "This film is not ___ for young children.",
    "surround": "Mountains ___ the valley on all sides.",
    "take a deep breath": "When you feel nervous, ___ and count to ten.",
    "take place": "The ceremony will ___ in the school hall at 9 a.m.",
    "task": "The most difficult ___ is usually the one you do first.",
    "technology": "New ___ has made communication much faster.",
    "therefore": "She studied hard; ___, she passed the exam easily.",
    "thick": "The walls of the old castle are very ___.",
    "traditional": "Wearing a kimono is a ___ part of Japanese culture.",
    "translation": "The ___ of the poem lost some of its original feeling.",
    "tremendously": "The new library has benefited the community ___.",
    "trillion": "The national debt reached over one ___ dollars.",
    "unexpected": "The ___ snowstorm cancelled all flights.",
    "unless": "___ you study regularly, you will find the exam very hard.",
    "used to": "She ___ walk to school, but now she takes the bus.",
    "valid": "Make sure your passport is ___ before you travel.",
    "valuable": "Time is the most ___ resource we have.",
    "versus": "Tomorrow's match is our school ___ the regional champions.",
    "volunteer": "She decided to ___ at the local animal shelter on weekends.",
    "waste time": "Don't ___ on social media when you should be studying.",
    "wonder": "I ___ why some people find mathematics so difficult.",
}

# ---------------------------------------------------------------------------
# Section B — Synonym / meaning-clue hints (replaces CEFR level hint)
# ---------------------------------------------------------------------------

FILL_IN_HINTS = {
    "a great deal (of)": "a large amount",
    "abroad": "in a foreign country",
    "accomplish": "to achieve or complete",
    "accurately": "correctly, without errors",
    "addictive": "hard to stop doing",
    "advantage": "a benefit or helpful factor",
    "advertising": "promoting a product publicly",
    "affect": "to have an influence on",
    "amazed": "very surprised and impressed",
    "ancient": "very old, from long ago",
    "apply": "to make a formal request",
    "approximately": "roughly, not exactly",
    "assign": "to give a task to someone",
    "assistance": "help or support",
    "at an angle": "not straight, tilted",
    "at least": "a minimum of",
    "attraction": "something that draws visitors",
    "available": "able to be obtained or used",
    "ban": "to officially forbid",
    "basic": "simple and fundamental",
    "benefit": "a positive result or advantage",
    "bilingual": "able to speak two languages",
    "billion": "one thousand million",
    "boil": "to heat water until bubbles form",
    "calculate": "to work out a number or amount",
    "casually": "in a relaxed, informal way",
    "claim": "to state something as true",
    "come up to": "to reach as far as",
    "common sense": "practical, everyday judgement",
    "communication": "sharing information with others",
    "complain": "to express dissatisfaction",
    "concentrate": "to focus your attention",
    "confuse": "to make someone uncertain or puzzled",
    "connection": "a link or relationship between things",
    "construction": "the process of building something",
    "contest": "a competition",
    "continent": "a large land mass (e.g. Asia, Africa)",
    "contrast": "a clear difference between two things",
    "contribution": "something given to help a shared goal",
    "convenient": "easy to use or access",
    "convince": "to persuade someone",
    "culture": "the traditions and values of a group",
    "current": "happening now, present",
    "customer": "a person who buys goods or services",
    "damage": "harm or injury caused to something",
    "deadly": "likely to cause death",
    "debt": "money owed to someone",
    "decade": "a period of ten years",
    "depend (on)": "to rely on something or someone",
    "destination": "the place you are travelling to",
    "destroy": "to ruin completely",
    "differ": "to be unlike or not the same",
    "disagree": "to have a different opinion",
    "discovery": "finding something new or unknown",
    "diverse": "varied, showing many differences",
    "divide": "to split into parts",
    "divided": "split into opposing groups",
    "document": "to record in writing",
    "due to": "because of",
    "economy": "the financial system of a country",
    "educational": "teaching or informative",
    "effective": "producing the desired result",
    "embarrassing": "causing feelings of shame or awkwardness",
    "empty": "containing nothing",
    "entire": "whole, complete",
    "exceed": "to go beyond a limit",
    "experiment": "a scientific test or trial",
    "expression": "a phrase or saying",
    "extremely": "to a very high degree",
    "final": "last, coming at the end",
    "flood": "an overflow of water onto land",
    "focus": "to concentrate on one thing",
    "former": "previous, from an earlier time",
    "freedom": "the right to act without restriction",
    "frequently": "often, many times",
    "frighten": "to make someone feel afraid",
    "function": "the purpose or role of something",
    "generally": "in most cases, usually",
    "get over": "to recover from",
    "guest": "a visitor who is invited",
    "hide": "to put something out of sight",
    "highly": "to a great extent, very much",
    "imagine": "to picture something in your mind",
    "immigrant": "a person who moves to a new country",
    "improve": "to become or make better",
    "in advance": "before the time something happens",
    "in shape": "physically fit and healthy",
    "increase": "to grow or rise in amount",
    "ingredient": "a component used in a recipe",
    "injure": "to cause physical harm",
    "interact": "to communicate or work with others",
    "invention": "a new device or process created by someone",
    "keep track (of)": "to monitor or record",
    "laundry": "clothes that need washing",
    "likely": "probable, expected to happen",
    "limited": "restricted in amount or extent",
    "location": "the place where something is",
    "maintain": "to keep in good condition",
    "majority": "more than half, the greater part",
    "manage": "to succeed in doing something difficult",
    "mayor": "the elected leader of a city or town",
    "messy": "untidy and disorganised",
    "motivation": "the reason for doing something",
    "multiply": "to increase by a given number",
    "no matter": "regardless of",
    "obtain": "to get or acquire",
    "occasionally": "sometimes, not often",
    "occupation": "a job or profession",
    "old-fashioned": "no longer modern or popular",
    "on purpose": "deliberately, intentionally",
    "opportunity": "a chance to do something",
    "option": "a choice available to someone",
    "organized": "planned and arranged in an orderly way",
    "ought to": "should, have a moral duty to",
    "outweigh": "to be more important than",
    "patient": "calm when waiting or dealing with difficulties",
    "peaceful": "calm and free from disturbance",
    "perfectly": "completely, in every way",
    "performance": "the act of doing something in front of others",
    "polluted": "contaminated with harmful substances",
    "population": "all the people living in a place",
    "position": "the way something is placed or arranged",
    "powerful": "having great strength or influence",
    "prevent": "to stop something from happening",
    "private": "personal and not for others to see",
    "produce": "to make or create something",
    "profit": "money earned after costs are paid",
    "protective": "keeping someone or something safe from harm",
    "provide": "to supply or give something needed",
    "quality": "how good something is",
    "range": "a variety of different things",
    "reach": "to stretch out to touch or get something",
    "recognize": "to identify someone or something seen before",
    "recommend": "to suggest as a good choice",
    "reduce": "to make smaller or less",
    "regardless of": "without being affected by",
    "region": "an area of a country or the world",
    "regional": "relating to a specific area",
    "relationship": "a connection between people or things",
    "remarkable": "unusual and worth noticing",
    "remind": "to help someone remember something",
    "replace": "to put something new in the place of another",
    "require": "to need something",
    "research": "careful study to find new information",
    "resident": "a person who lives in a place",
    "respected": "admired and held in high regard",
    "rural": "relating to the countryside, not the city",
    "score": "a result in a test or game",
    "select": "to choose from a group",
    "shade": "an area sheltered from direct sunlight",
    "shocked": "very surprised and upset",
    "similar": "almost the same, alike",
    "site": "a place where something is located",
    "spill": "to accidentally let liquid fall out",
    "spot": "a particular place or location",
    "strategy": "a plan for achieving a goal",
    "style": "the way something is done or expressed",
    "submit": "to hand in work or a form",
    "suitable": "right or appropriate for a purpose",
    "surround": "to be on all sides of something",
    "take a deep breath": "to breathe in slowly and deeply to calm down",
    "take place": "to happen or occur",
    "task": "a piece of work to be done",
    "technology": "machines and systems developed by science",
    "therefore": "as a result, for that reason",
    "thick": "measuring a large distance from one side to the other",
    "traditional": "following customs passed down through generations",
    "translation": "converting text from one language to another",
    "tremendously": "to a very great degree",
    "trillion": "one million million",
    "unexpected": "surprising, not anticipated",
    "unless": "except on the condition that",
    "used to": "did something regularly in the past",
    "valid": "legally or officially acceptable",
    "valuable": "worth a lot, very useful",
    "versus": "against, in competition with",
    "volunteer": "to offer to do something without being paid",
    "waste time": "to spend time on unproductive things",
    "wonder": "to be curious or want to know",
}

# ---------------------------------------------------------------------------
# Section A — Multiple choice definitions (C1 words)
# ---------------------------------------------------------------------------

C1_DEFINITIONS = {
    "addictive": {
        "answer": "causing a strong desire or need to keep doing or having something",
        "options": [
            "A. describing something that is very expensive",
            "B. causing a strong desire or need to keep doing or having something",
            "C. relating to physical exercise and sport",
            "D. something that is boring and repetitive",
        ],
    },
    "assign": {
        "answer": "to give a particular job or task to someone",
        "options": [
            "A. to borrow something from a library",
            "B. to refuse to complete a piece of work",
            "C. to give a particular job or task to someone",
            "D. to make a mathematical calculation",
        ],
    },
    "bilingual": {
        "answer": "able to speak two languages fluently",
        "options": [
            "A. having lived in two different countries",
            "B. relating to a person who teaches languages",
            "C. able to speak two languages fluently",
            "D. describing a school that offers two subjects",
        ],
    },
    "diverse": {
        "answer": "showing a great deal of variety; very different from each other",
        "options": [
            "A. very similar to others",
            "B. showing a great deal of variety; very different from each other",
            "C. difficult to understand or explain",
            "D. relating to only one culture or background",
        ],
    },
    "exceed": {
        "answer": "to go beyond a set limit or be greater than something",
        "options": [
            "A. to fall below the expected standard",
            "B. to repeat an action several times",
            "C. to go beyond a set limit or be greater than something",
            "D. to compare two different results",
        ],
    },
    "motivation": {
        "answer": "a reason or desire that makes someone want to do something",
        "options": [
            "A. a feeling of fear about doing something new",
            "B. a reason or desire that makes someone want to do something",
            "C. an instruction given by a teacher",
            "D. a type of reward given after completing a task",
        ],
    },
    "outweigh": {
        "answer": "to be greater in importance, value, or benefit than something else",
        "options": [
            "A. to weigh more than the recommended amount",
            "B. to be smaller or less important than something",
            "C. to be greater in importance, value, or benefit than something else",
            "D. to count or measure physical objects",
        ],
    },
    "regardless of": {
        "answer": "without being affected by or considering something",
        "options": [
            "A. only when certain conditions are met",
            "B. as a result of a specific event",
            "C. without being affected by or considering something",
            "D. in addition to something else",
        ],
    },
    "tremendously": {
        "answer": "to a very great extent; enormously",
        "options": [
            "A. in a slow or careless manner",
            "B. to a very great extent; enormously",
            "C. with some doubt or uncertainty",
            "D. in a way that is barely noticeable",
        ],
    },
}

# ---------------------------------------------------------------------------
# Section A — Multiple choice definitions (non-C1 words)
# ---------------------------------------------------------------------------

SYNONYM_MCQ = {
    "population": {
        "answer": "the total number of people living in a place",
        "options": [
            "A. the total number of people living in a place",
            "B. the physical size of a country",
            "C. the rate at which a city grows",
            "D. the number of government buildings in a region",
        ],
    },
    "differ": {
        "answer": "to be unlike or not the same as something else",
        "options": [
            "A. to agree with another person's opinion",
            "B. to be unlike or not the same as something else",
            "C. to change into something completely new",
            "D. to avoid a difficult situation",
        ],
    },
    "in advance": {
        "answer": "before something happens or before a deadline",
        "options": [
            "A. immediately after the event",
            "B. before something happens or before a deadline",
            "C. at the same time as something else",
            "D. without telling anyone first",
        ],
    },
    "majority": {
        "answer": "more than half of a group",
        "options": [
            "A. exactly half of a total",
            "B. a very small part of something",
            "C. more than half of a group",
            "D. an equal share between two sides",
        ],
    },
    "performance": {
        "answer": "the act of entertaining an audience by acting, singing, or playing",
        "options": [
            "A. a written report about an event",
            "B. the act of entertaining an audience by acting, singing, or playing",
            "C. a type of classroom test",
            "D. the process of building something new",
        ],
    },
    "polluted": {
        "answer": "made dirty or harmful by chemicals or waste",
        "options": [
            "A. clean and safe for use",
            "B. very cold and difficult to survive in",
            "C. made dirty or harmful by chemicals or waste",
            "D. crowded with too many people",
        ],
    },
    "position": {
        "answer": "the place or arrangement of something or someone",
        "options": [
            "A. the speed at which something moves",
            "B. the place or arrangement of something or someone",
            "C. the colour or appearance of an object",
            "D. the price asked for a service",
        ],
    },
    "powerful": {
        "answer": "having great strength, force, or influence",
        "options": [
            "A. very small and easy to overlook",
            "B. slow-moving and difficult to control",
            "C. relating to something used in cooking",
            "D. having great strength, force, or influence",
        ],
    },
    "convince": {
        "answer": "to persuade someone to believe or do something",
        "options": [
            "A. to force someone to act against their will",
            "B. to persuade someone to believe or do something",
            "C. to give someone a reward for good work",
            "D. to explain a complex topic clearly",
        ],
    },
    "debt": {
        "answer": "money that is owed to another person or organisation",
        "options": [
            "A. money saved for future use",
            "B. a type of government tax",
            "C. money that is owed to another person or organisation",
            "D. the cost of running a business",
        ],
    },
    "messy": {
        "answer": "untidy and disorganised",
        "options": [
            "A. very clean and well-arranged",
            "B. untidy and disorganised",
            "C. carefully decorated",
            "D. too small to be useful",
        ],
    },
    "require": {
        "answer": "to need something in order to succeed or function",
        "options": [
            "A. to avoid something that is unnecessary",
            "B. to suggest an optional activity",
            "C. to need something in order to succeed or function",
            "D. to finish a task before the deadline",
        ],
    },
    "divided": {
        "answer": "separated into opposing groups with different opinions",
        "options": [
            "A. united and in full agreement",
            "B. confused about what to choose",
            "C. separated into opposing groups with different opinions",
            "D. very large and difficult to manage",
        ],
    },
    "current": {
        "answer": "happening or existing now",
        "options": [
            "A. relating to something from the distant past",
            "B. happening or existing now",
            "C. planned for a future date",
            "D. no longer used or relevant",
        ],
    },
    "customer": {
        "answer": "a person who buys goods or services from a shop or business",
        "options": [
            "A. the owner of a shop or business",
            "B. a person who works at a shop",
            "C. a person who buys goods or services from a shop or business",
            "D. someone who delivers products",
        ],
    },
    "damage": {
        "answer": "harm or injury caused to something",
        "options": [
            "A. a plan to improve or repair something",
            "B. harm or injury caused to something",
            "C. the cost of buying a product",
            "D. a reward given after hard work",
        ],
    },
    "final": {
        "answer": "last in a series; coming at the end",
        "options": [
            "A. happening at the very beginning",
            "B. repeated many times over",
            "C. last in a series; coming at the end",
            "D. uncertain and likely to change",
        ],
    },
    "similar": {
        "answer": "almost the same as something else",
        "options": [
            "A. completely opposite in every way",
            "B. almost the same as something else",
            "C. more expensive than other options",
            "D. unique and very rare",
        ],
    },
    "location": {
        "answer": "the particular place where something is",
        "options": [
            "A. the time when an event happens",
            "B. the reason why something exists",
            "C. the particular place where something is",
            "D. the person responsible for something",
        ],
    },
    "customer": {
        "answer": "a person who buys goods or services from a shop or business",
        "options": [
            "A. the owner of a shop or business",
            "B. a person who works at a shop",
            "C. a person who buys goods or services from a shop or business",
            "D. someone who delivers products",
        ],
    },
    "improve": {
        "answer": "to become better or to make something better",
        "options": [
            "A. to stay the same over time",
            "B. to become worse gradually",
            "C. to become better or to make something better",
            "D. to replace something entirely",
        ],
    },
    "reduce": {
        "answer": "to make something smaller or less in amount",
        "options": [
            "A. to make something larger or more",
            "B. to make something smaller or less in amount",
            "C. to measure the size of something",
            "D. to keep something at the same level",
        ],
    },
    "recognize": {
        "answer": "to know and remember someone or something seen before",
        "options": [
            "A. to see something for the very first time",
            "B. to know and remember someone or something seen before",
            "C. to describe someone's appearance",
            "D. to forget who someone is",
        ],
    },
    "recommend": {
        "answer": "to suggest that something is good or suitable",
        "options": [
            "A. to warn someone about a danger",
            "B. to disagree with someone's choice",
            "C. to suggest that something is good or suitable",
            "D. to order someone to do something",
        ],
    },
    "educational": {
        "answer": "relating to learning and providing useful information",
        "options": [
            "A. relating to learning and providing useful information",
            "B. designed only for very young children",
            "C. expensive and difficult to access",
            "D. focused on physical fitness",
        ],
    },
    "effective": {
        "answer": "producing the result that was intended",
        "options": [
            "A. very complicated and hard to use",
            "B. producing the result that was intended",
            "C. taking a very long time to finish",
            "D. suitable only for experts",
        ],
    },
    "focus": {
        "answer": "to give all your attention to something",
        "options": [
            "A. to ignore something that is unimportant",
            "B. to give all your attention to something",
            "C. to share a task with a partner",
            "D. to finish work quickly",
        ],
    },
    "maintain": {
        "answer": "to keep something in its current good condition",
        "options": [
            "A. to let something slowly get worse",
            "B. to completely change how something works",
            "C. to keep something in its current good condition",
            "D. to repair something that is badly broken",
        ],
    },
    "interact": {
        "answer": "to communicate and work together with other people",
        "options": [
            "A. to compete against someone in a contest",
            "B. to avoid speaking to other people",
            "C. to communicate and work together with other people",
            "D. to study alone without any help",
        ],
    },
    "select": {
        "answer": "to carefully choose something from a group",
        "options": [
            "A. to buy everything available",
            "B. to carefully choose something from a group",
            "C. to reject all the available options",
            "D. to mix several things together",
        ],
    },
    "obtain": {
        "answer": "to get or acquire something, especially by effort",
        "options": [
            "A. to lose something you previously owned",
            "B. to give something away to others",
            "C. to get or acquire something, especially by effort",
            "D. to return something to its original place",
        ],
    },
    "suitable": {
        "answer": "right or appropriate for a particular purpose or situation",
        "options": [
            "A. very difficult and demanding",
            "B. right or appropriate for a particular purpose or situation",
            "C. completely unnecessary",
            "D. only useful for trained professionals",
        ],
    },
    "strategy": {
        "answer": "a careful plan for achieving a goal",
        "options": [
            "A. a sudden decision made without thinking",
            "B. a list of problems to solve",
            "C. a careful plan for achieving a goal",
            "D. a set of rules for playing a game",
        ],
    },
    "valid": {
        "answer": "officially acceptable and recognised",
        "options": [
            "A. outdated and no longer in use",
            "B. officially acceptable and recognised",
            "C. difficult to prove or verify",
            "D. only used in informal situations",
        ],
    },
    "waste time": {
        "answer": "to spend time on things that are not productive or useful",
        "options": [
            "A. to use time very efficiently",
            "B. to spend time on things that are not productive or useful",
            "C. to plan ahead for future tasks",
            "D. to take a short break from work",
        ],
    },
    "deadly": {
        "answer": "likely to cause death",
        "options": [
            "A. easily treated with common medicine",
            "B. likely to cause death",
            "C. very common and widespread",
            "D. harmless to most living things",
        ],
    },
    "get over": {
        "answer": "to recover from an illness or a difficult experience",
        "options": [
            "A. to avoid facing a problem",
            "B. to make something worse",
            "C. to recover from an illness or a difficult experience",
            "D. to give up when something is too difficult",
        ],
    },
    "casually": {
        "answer": "in a relaxed and informal way",
        "options": [
            "A. in a very formal and serious way",
            "B. in a relaxed and informal way",
            "C. with a great deal of effort",
            "D. very quickly and carelessly",
        ],
    },
    "document": {
        "answer": "to record information in writing for future reference",
        "options": [
            "A. to destroy records that are no longer needed",
            "B. to share information only by speaking",
            "C. to record information in writing for future reference",
            "D. to copy someone else's work",
        ],
    },
    "contrast": {
        "answer": "a clear difference between two things when compared",
        "options": [
            "A. a similarity between two things",
            "B. a clear difference between two things when compared",
            "C. a combination of two ideas",
            "D. a step-by-step instruction",
        ],
    },
    "contribution": {
        "answer": "something given or done to help achieve a shared goal",
        "options": [
            "A. a problem that prevents progress",
            "B. something given or done to help achieve a shared goal",
            "C. a negative comment about someone's work",
            "D. a request for more resources",
        ],
    },
    "frequently": {
        "answer": "happening often and regularly",
        "options": [
            "A. happening only once in a while",
            "B. happening often and regularly",
            "C. never happening at all",
            "D. happening at an unexpected time",
        ],
    },
    "function": {
        "answer": "the purpose or role that something is designed to perform",
        "options": [
            "A. the appearance or colour of an object",
            "B. the price or value of something",
            "C. the purpose or role that something is designed to perform",
            "D. the age or history of a device",
        ],
    },
    "generally": {
        "answer": "in most cases; usually, but not always",
        "options": [
            "A. never, under any circumstances",
            "B. only on very special occasions",
            "C. in most cases; usually, but not always",
            "D. exactly, without exception",
        ],
    },
    "increase": {
        "answer": "to become or make something greater in size or amount",
        "options": [
            "A. to stay the same over a long time",
            "B. to become or make something greater in size or amount",
            "C. to make something smaller and less important",
            "D. to keep something constant",
        ],
    },
    "provide": {
        "answer": "to supply or make available what is needed",
        "options": [
            "A. to take something away from someone",
            "B. to supply or make available what is needed",
            "C. to prevent access to resources",
            "D. to charge money for a service",
        ],
    },
    "region": {
        "answer": "a specific area of a country or the world",
        "options": [
            "A. an exact point on a map",
            "B. a specific area of a country or the world",
            "C. the border between two countries",
            "D. a single city or town",
        ],
    },
    "relationship": {
        "answer": "the way in which two or more people or things are connected",
        "options": [
            "A. a disagreement between two people",
            "B. a set of rules that must be followed",
            "C. the way in which two or more people or things are connected",
            "D. a formal document signed by both sides",
        ],
    },
    "research": {
        "answer": "careful study and investigation to discover new information",
        "options": [
            "A. writing a report from memory",
            "B. careful study and investigation to discover new information",
            "C. copying information from a textbook",
            "D. solving a maths problem",
        ],
    },
    "available": {
        "answer": "able to be used, obtained, or reached",
        "options": [
            "A. broken and impossible to use",
            "B. reserved only for special people",
            "C. able to be used, obtained, or reached",
            "D. very expensive and out of reach",
        ],
    },
    "accurately": {
        "answer": "done in a way that is correct and without errors",
        "options": [
            "A. done very quickly and carelessly",
            "B. done in a way that is correct and without errors",
            "C. done only by professionals",
            "D. done in a creative and unusual way",
        ],
    },
    "assistance": {
        "answer": "help or support given to someone",
        "options": [
            "A. a penalty or punishment",
            "B. help or support given to someone",
            "C. an order to do something",
            "D. a payment for a service",
        ],
    },
    "claim": {
        "answer": "to state that something is true, sometimes without proof",
        "options": [
            "A. to admit that you were wrong",
            "B. to agree with what someone else says",
            "C. to state that something is true, sometimes without proof",
            "D. to ask someone a direct question",
        ],
    },
    "concentrate": {
        "answer": "to direct all your attention and effort to one thing",
        "options": [
            "A. to think about many things at the same time",
            "B. to stop working and take a rest",
            "C. to direct all your attention and effort to one thing",
            "D. to make something much simpler",
        ],
    },
    "connection": {
        "answer": "a link or relationship between two things",
        "options": [
            "A. a barrier that prevents communication",
            "B. a link or relationship between two things",
            "C. a difference that separates two ideas",
            "D. a mistake made during a test",
        ],
    },
    "a great deal (of)": {
        "answer": "a large amount of something",
        "options": [
            "A. a large amount of something",
            "B. a small or insignificant portion",
            "C. a set of instructions for doing something",
            "D. a specific number or measurement",
        ],
    },
    "patient": {
        "answer": "able to wait calmly without becoming annoyed",
        "options": [
            "A. quick to react and easily upset",
            "B. able to wait calmly without becoming annoyed",
            "C. always in a hurry to finish tasks",
            "D. very strict and demanding",
        ],
    },
    "peaceful": {
        "answer": "calm, quiet, and free from disturbance",
        "options": [
            "A. full of noise and excitement",
            "B. very busy and crowded",
            "C. calm, quiet, and free from disturbance",
            "D. dangerous and unpredictable",
        ],
    },
    "imagine": {
        "answer": "to form a picture or idea in your mind",
        "options": [
            "A. to describe something using words",
            "B. to remember something from the past",
            "C. to form a picture or idea in your mind",
            "D. to explain something to another person",
        ],
    },
    "in shape": {
        "answer": "physically fit and healthy",
        "options": [
            "A. having a specific form or outline",
            "B. physically fit and healthy",
            "C. organised and tidy",
            "D. ready to start a new task",
        ],
    },
    "respected": {
        "answer": "admired by others because of skill or good behaviour",
        "options": [
            "A. admired by others because of skill or good behaviour",
            "B. known for causing problems",
            "C. very well paid and successful",
            "D. liked by everyone for being funny",
        ],
    },
    "construction": {
        "answer": "the process of building something such as a house or road",
        "options": [
            "A. the process of destroying something",
            "B. the process of building something such as a house or road",
            "C. the act of repairing a broken object",
            "D. the design of a machine",
        ],
    },
    "economy": {
        "answer": "the system of trade and industry by which a country's wealth is made",
        "options": [
            "A. the history of a country's government",
            "B. the system of trade and industry by which a country's wealth is made",
            "C. the number of people who live in a country",
            "D. the cost of living in a city",
        ],
    },
    "destination": {
        "answer": "the place you are travelling to",
        "options": [
            "A. the vehicle used to travel somewhere",
            "B. the length of a journey",
            "C. the place where a journey begins",
            "D. the place you are travelling to",
        ],
    },
    "frighten": {
        "answer": "to make someone feel suddenly afraid",
        "options": [
            "A. to make someone feel suddenly afraid",
            "B. to make someone feel happy and excited",
            "C. to confuse someone with complicated information",
            "D. to encourage someone to be brave",
        ],
    },
    "shocked": {
        "answer": "feeling very surprised and upset by something unexpected",
        "options": [
            "A. feeling calm and prepared",
            "B. feeling slightly disappointed",
            "C. feeling very surprised and upset by something unexpected",
            "D. feeling proud of an achievement",
        ],
    },
    "style": {
        "answer": "a particular way of doing or presenting something",
        "options": [
            "A. the amount of time spent on a task",
            "B. the difficulty of a piece of work",
            "C. a particular way of doing or presenting something",
            "D. the cost of a product or service",
        ],
    },
    "surround": {
        "answer": "to be all around something or someone on every side",
        "options": [
            "A. to be directly opposite something",
            "B. to be all around something or someone on every side",
            "C. to be far away from something",
            "D. to be underneath something",
        ],
    },
    "ancient": {
        "answer": "belonging to a period long ago in history",
        "options": [
            "A. belonging to a period long ago in history",
            "B. brand new and recently made",
            "C. relating to the future",
            "D. very popular at the present time",
        ],
    },
    "due to": {
        "answer": "because of; caused by",
        "options": [
            "A. in spite of something",
            "B. before a particular time",
            "C. in addition to something else",
            "D. because of; caused by",
        ],
    },
    "extremely": {
        "answer": "to a very great degree; very",
        "options": [
            "A. slightly, to a small degree",
            "B. to a very great degree; very",
            "C. in an ordinary, unremarkable way",
            "D. less than expected",
        ],
    },
    "on purpose": {
        "answer": "done deliberately, not by accident",
        "options": [
            "A. happening suddenly and unexpectedly",
            "B. done by mistake without thinking",
            "C. done deliberately, not by accident",
            "D. agreed upon by a group",
        ],
    },
    "perfectly": {
        "answer": "in a way that is completely correct and without any faults",
        "options": [
            "A. in a way that is mostly correct but with some errors",
            "B. in a way that is completely correct and without any faults",
            "C. in a way that is unusual and surprising",
            "D. only partly or to a limited degree",
        ],
    },
    "spill": {
        "answer": "to accidentally cause a liquid to flow out of its container",
        "options": [
            "A. to carefully pour liquid into a glass",
            "B. to accidentally cause a liquid to flow out of its container",
            "C. to store liquid in a safe place",
            "D. to heat liquid until it boils",
        ],
    },
    "spot": {
        "answer": "a particular place or location",
        "options": [
            "A. a particular place or location",
            "B. a large area of land",
            "C. the distance between two cities",
            "D. a route taken from one place to another",
        ],
    },
    "old-fashioned": {
        "answer": "no longer modern; from an earlier time",
        "options": [
            "A. very new and up to date",
            "B. no longer modern; from an earlier time",
            "C. popular with young people right now",
            "D. designed for professional use only",
        ],
    },
    "hide": {
        "answer": "to put something in a place where it cannot be found or seen",
        "options": [
            "A. to display something openly for all to see",
            "B. to put something in a place where it cannot be found or seen",
            "C. to move something to a new location",
            "D. to throw something away",
        ],
    },
    "remarkable": {
        "answer": "unusual or surprising in a way that deserves attention",
        "options": [
            "A. very ordinary and easy to overlook",
            "B. slightly better than average",
            "C. unusual or surprising in a way that deserves attention",
            "D. difficult and not worth trying",
        ],
    },
    "regional": {
        "answer": "relating to a particular region or area",
        "options": [
            "A. relating to the whole world",
            "B. relating to a particular region or area",
            "C. relating only to a single city",
            "D. relating to national government",
        ],
    },
    "thick": {
        "answer": "measuring a large distance between one surface and the other",
        "options": [
            "A. measuring a very small distance between surfaces",
            "B. very long from end to end",
            "C. measuring a large distance between one surface and the other",
            "D. light and easy to carry",
        ],
    },
    "flood": {
        "answer": "a large amount of water that covers an area that is usually dry",
        "options": [
            "A. a very strong wind that destroys buildings",
            "B. a large amount of water that covers an area that is usually dry",
            "C. a period of very dry weather with no rain",
            "D. a crack that appears in the earth",
        ],
    },
    "keep track (of)": {
        "answer": "to monitor and stay informed about something",
        "options": [
            "A. to ignore something that is unimportant",
            "B. to monitor and stay informed about something",
            "C. to record something only once",
            "D. to lose information about something",
        ],
    },
    "prevent": {
        "answer": "to stop something from happening",
        "options": [
            "A. to allow something to continue",
            "B. to stop something from happening",
            "C. to make something happen faster",
            "D. to start a process over again",
        ],
    },
    "at an angle": {
        "answer": "in a tilted or slanted position, not straight",
        "options": [
            "A. in a perfectly straight, upright position",
            "B. placed flat on a surface",
            "C. in a tilted or slanted position, not straight",
            "D. moving in a circular direction",
        ],
    },
    "embarrassing": {
        "answer": "causing a feeling of shame or awkwardness",
        "options": [
            "A. causing a feeling of great pride",
            "B. causing a feeling of shame or awkwardness",
            "C. causing a feeling of excitement",
            "D. causing a feeling of confusion",
        ],
    },
    "organized": {
        "answer": "arranged in a neat, logical, and efficient way",
        "options": [
            "A. arranged in a neat, logical, and efficient way",
            "B. scattered randomly without order",
            "C. made up of many unrelated parts",
            "D. very difficult to understand",
        ],
    },
    "ought to": {
        "answer": "used to say what is the right or sensible thing to do",
        "options": [
            "A. used to describe something that is impossible",
            "B. used to say what is the right or sensible thing to do",
            "C. used to describe something that happened in the past",
            "D. used to make a polite request",
        ],
    },
    "injure": {
        "answer": "to harm or hurt a person's body",
        "options": [
            "A. to treat and heal a wound",
            "B. to harm or hurt a person's body",
            "C. to exercise in order to stay fit",
            "D. to describe physical pain without a cause",
        ],
    },
    "profit": {
        "answer": "money gained after all costs have been paid",
        "options": [
            "A. money spent on running a business",
            "B. the total amount of sales made",
            "C. a loan taken to start a business",
            "D. money gained after all costs have been paid",
        ],
    },
    "shade": {
        "answer": "an area sheltered from the sun and therefore cooler and darker",
        "options": [
            "A. an area exposed to bright sunlight",
            "B. an area sheltered from the sun and therefore cooler and darker",
            "C. a bright colour used in painting",
            "D. a type of window covering",
        ],
    },
    "occasionally": {
        "answer": "sometimes but not very often",
        "options": [
            "A. never, under any circumstances",
            "B. always, without exception",
            "C. sometimes but not very often",
            "D. regularly and predictably",
        ],
    },
    "versus": {
        "answer": "against; used to compare two sides in a contest or argument",
        "options": [
            "A. in addition to; together with",
            "B. similar to; like",
            "C. against; used to compare two sides in a contest or argument",
            "D. after; following",
        ],
    },
    "range": {
        "answer": "a variety of different things of the same general type",
        "options": [
            "A. a single item from a collection",
            "B. a variety of different things of the same general type",
            "C. the exact number of items available",
            "D. the most expensive item in a collection",
        ],
    },
    "trillion": {
        "answer": "the number one million million (1,000,000,000,000)",
        "options": [
            "A. the number one thousand",
            "B. the number one million",
            "C. the number one billion",
            "D. the number one million million (1,000,000,000,000)",
        ],
    },
    "occupation": {
        "answer": "a job or profession that someone does regularly for money",
        "options": [
            "A. a hobby done for pleasure in free time",
            "B. a job or profession that someone does regularly for money",
            "C. a skill learned at school",
            "D. a qualification earned at university",
        ],
    },
    "opportunity": {
        "answer": "a chance to do something useful, valuable, or enjoyable",
        "options": [
            "A. an obstacle that stops progress",
            "B. a requirement that must be met",
            "C. a chance to do something useful, valuable, or enjoyable",
            "D. a risk that may lead to failure",
        ],
    },
    "accomplish": {
        "answer": "to succeed in doing or completing something",
        "options": [
            "A. to begin something without finishing it",
            "B. to succeed in doing or completing something",
            "C. to avoid a difficult task",
            "D. to repeat the same mistake",
        ],
    },
}

# ---------------------------------------------------------------------------
# Section C — Error analysis sentences
# ---------------------------------------------------------------------------

ERROR_ANALYSIS = {
    "differ": {
        "sentence": "Opinions on this topic **agree** widely among experts.",
        "answer": "differ",
    },
    "in advance": {
        "sentence": "Book your tickets **afterwards** to get a better price.",
        "answer": "in advance",
    },
    "majority": {
        "sentence": "The **minority** of students prefer shorter homework assignments.",
        "answer": "majority",
    },
    "performance": {
        "sentence": "Her **rehearsal** in the school play was outstanding.",
        "answer": "performance",
    },
    "polluted": {
        "sentence": "The river became **purified** after the factory opened nearby.",
        "answer": "polluted",
    },
    "position": {
        "sentence": "Sitting in an uncomfortable **direction** can hurt your back.",
        "answer": "position",
    },
    "powerful": {
        "sentence": "Wind is a **fragile** and clean source of energy.",
        "answer": "powerful",
    },
    "convince": {
        "sentence": "She tried to **prevent** her parents to let her stay out late.",
        "answer": "convince",
    },
    "debt": {
        "sentence": "He worked two jobs to pay off his **savings**.",
        "answer": "debt",
    },
    "messy": {
        "sentence": "His bedroom is always **organised**, with clothes on the floor.",
        "answer": "messy",
    },
    "require": {
        "sentence": "This task will **avoid** a lot of concentration.",
        "answer": "require",
    },
    "divided": {
        "sentence": "Opinion was **united** on whether to change the school uniform.",
        "answer": "divided",
    },
    "current": {
        "sentence": "The **ancient** situation requires everyone to stay calm.",
        "answer": "current",
    },
    "customer": {
        "sentence": "The shop assistant helped every **employee** with a smile.",
        "answer": "customer",
    },
    "damage": {
        "sentence": "The storm caused serious **improvement** to the roof.",
        "answer": "damage",
    },
    "final": {
        "sentence": "This is your **first** chance to improve your grade.",
        "answer": "final",
    },
    "similar": {
        "sentence": "The two paintings look very **opposite** at first glance.",
        "answer": "similar",
    },
    "location": {
        "sentence": "The hotel has a perfect **schedule** near the beach.",
        "answer": "location",
    },
    "improve": {
        "sentence": "Practice every day to **ignore** your pronunciation.",
        "answer": "improve",
    },
    "reduce": {
        "sentence": "Turn off lights to **increase** energy consumption.",
        "answer": "reduce",
    },
    "recognize": {
        "sentence": "I didn't **forget** him at first because of his new haircut.",
        "answer": "recognize",
    },
    "recommend": {
        "sentence": "I would **warn** this restaurant to anyone who loves Italian food.",
        "answer": "recommend",
    },
    "educational": {
        "sentence": "Visiting museums is both fun and **exhausting**.",
        "answer": "educational",
    },
    "effective": {
        "sentence": "This new method is more **complicated** than the old one.",
        "answer": "effective",
    },
    "focus": {
        "sentence": "Try to **avoid** on one task at a time.",
        "answer": "focus",
    },
    "maintain": {
        "sentence": "It is important to **ignore** a healthy lifestyle.",
        "answer": "maintain",
    },
    "interact": {
        "sentence": "Social skills help you **compete** confidently with others.",
        "answer": "interact",
    },
    "select": {
        "sentence": "Please **reject** the correct answer from the options below.",
        "answer": "select",
    },
    "obtain": {
        "sentence": "You must **refuse** permission before using someone's photos.",
        "answer": "obtain",
    },
    "suitable": {
        "sentence": "This film is not **popular** for young children.",
        "answer": "suitable",
    },
    "strategy": {
        "sentence": "She developed a clear **problem** for improving her grades.",
        "answer": "strategy",
    },
    "valid": {
        "sentence": "Make sure your passport is **expired** before you travel.",
        "answer": "valid",
    },
    "waste time": {
        "sentence": "Don't **invest** time on social media when you should be studying.",
        "answer": "waste time",
    },
    "deadly": {
        "sentence": "The scientist discovered a **harmless** virus in the jungle.",
        "answer": "deadly",
    },
    "get over": {
        "sentence": "It took her weeks to **cause** the flu.",
        "answer": "get over",
    },
    "casually": {
        "sentence": "He was dressed **formally** in jeans and a T-shirt.",
        "answer": "casually",
    },
    "document": {
        "sentence": "Always **ignore** your sources when writing an essay.",
        "answer": "document",
    },
    "contrast": {
        "sentence": "In **addition** to summer, winter nights are very long.",
        "answer": "contrast",
    },
    "contribution": {
        "sentence": "Everyone should make a **complaint** to keeping the classroom clean.",
        "answer": "contribution",
    },
    "frequently": {
        "sentence": "She **rarely** goes to the library after school.",
        "answer": "frequently",
    },
    "function": {
        "sentence": "The main **decoration** of the heart is to pump blood.",
        "answer": "function",
    },
    "generally": {
        "sentence": "Students **never** find science interesting when it is hands-on.",
        "answer": "generally",
    },
    "increase": {
        "sentence": "The number of electric cars continues to **decrease**.",
        "answer": "increase",
    },
    "provide": {
        "sentence": "The school will **remove** all the materials you need.",
        "answer": "provide",
    },
    "region": {
        "sentence": "Rice is the main food in this **building** of Asia.",
        "answer": "region",
    },
    "relationship": {
        "sentence": "A good **argument** with your teacher helps you learn more.",
        "answer": "relationship",
    },
    "research": {
        "sentence": "Scientists do **guessing** to find cures for diseases.",
        "answer": "research",
    },
    "available": {
        "sentence": "The tickets are not **mandatory** online; you must buy them in person.",
        "answer": "available",
    },
    "accurately": {
        "sentence": "Please read the instructions **carelessly** before starting the test.",
        "answer": "accurately",
    },
    "assistance": {
        "sentence": "She asked for **resistance** when she couldn't open the jar.",
        "answer": "assistance",
    },
    "claim": {
        "sentence": "The company **denied** their product cures headaches.",
        "answer": "claim",
    },
    "concentrate": {
        "sentence": "It's hard to **relax** when there is too much noise.",
        "answer": "concentrate",
    },
    "connection": {
        "sentence": "There is a clear **barrier** between diet and health.",
        "answer": "connection",
    },
    "therefore": {
        "sentence": "She studied hard; **despite**, she passed the exam easily.",
        "answer": "therefore",
    },
    "addictive": {
        "sentence": "Social media can be very **harmless** for teenagers.",
        "answer": "addictive",
    },
    "ban": {
        "sentence": "The city decided to **allow** plastic bags from all supermarkets.",
        "answer": "ban",
    },
    "attraction": {
        "sentence": "The Eiffel Tower is a major tourist **problem** in Paris.",
        "answer": "attraction",
    },
    "amazed": {
        "sentence": "The audience was **bored** by the magician's tricks.",
        "answer": "amazed",
    },
    "complain": {
        "sentence": "The customer called to **praise** the company about the late delivery.",
        "answer": "complain",
    },
    "used to": {
        "sentence": "She **wants to** walk to school, but now she takes the bus.",
        "answer": "used to",
    },
    "protective": {
        "sentence": "Parents are naturally **careless** about their young children.",
        "answer": "protective",
    },
    "assign": {
        "sentence": "The teacher will **remove** different topics to each group.",
        "answer": "assign",
    },
    "common sense": {
        "sentence": "You don't need a rulebook — just use **confusion**.",
        "answer": "common sense",
    },
    "guest": {
        "sentence": "We prepared a special meal for our **enemy**.",
        "answer": "guest",
    },
    "entire": {
        "sentence": "She read the **partial** book in one day.",
        "answer": "entire",
    },
    "destroy": {
        "sentence": "The fire threatened to **protect** the entire forest.",
        "answer": "destroy",
    },
    "confuse": {
        "sentence": "The complicated instructions **clarified** most students.",
        "answer": "confuse",
    },
    "empty": {
        "sentence": "The classroom was **crowded** when I arrived early.",
        "answer": "empty",
    },
    "multiply": {
        "sentence": "If you **divide** six by seven, you get forty-two.",
        "answer": "multiply",
    },
    "produce": {
        "sentence": "Farms in this region **import** most of the country's rice.",
        "answer": "produce",
    },
    "approximately": {
        "sentence": "The journey takes **exactly** three hours by train.",
        "answer": "approximately",
    },
    "diverse": {
        "sentence": "The city has a **uniform** population from many countries.",
        "answer": "diverse",
    },
    "divide": {
        "sentence": "The teacher will **combine** the class into groups of four.",
        "answer": "divide",
    },
    "ingredient": {
        "sentence": "Sugar is the main **product** in most desserts.",
        "answer": "ingredient",
    },
    "come up to": {
        "sentence": "The water in the lake **fell below** his waist.",
        "answer": "come up to",
    },
    "remind": {
        "sentence": "Please **forget** me to submit the form before Friday.",
        "answer": "remind",
    },
    "mayor": {
        "sentence": "The **student** gave a speech at the opening of the new park.",
        "answer": "mayor",
    },
    "outweigh": {
        "sentence": "The benefits of exercise clearly **underestimate** the effort required.",
        "answer": "outweigh",
    },
    "rural": {
        "sentence": "Many young people move from **urban** areas to the city.",
        "answer": "rural",
    },
}

# ---------------------------------------------------------------------------
# Section D — Real-world application prompts (academic words prioritised)
# ---------------------------------------------------------------------------

REAL_WORLD_PROMPTS = {
    "require": (
        "Your school is introducing a new rule. Write 1–2 sentences explaining what the rule "
        "will **require** students to do and why it is important."
    ),
    "divided": (
        "Your class cannot agree on a topic for the school project. Write 1–2 sentences "
        "describing how the class is **divided** and what you think should happen next."
    ),
    "traditional": (
        "Think of a custom or celebration in your culture. Write 1–2 sentences describing it "
        "and use the word **traditional**."
    ),
    "majority": (
        "Your class is voting on a class trip. Write 1–2 sentences explaining what happens when "
        "the **majority** of students agree on a destination."
    ),
    "performance": (
        "You saw a school play or sports event recently. Write 1–2 sentences describing the "
        "**performance** and your reaction to it."
    ),
    "function": (
        "Choose a device you use every day (e.g. a phone or a pen). Write 1–2 sentences "
        "explaining its main **function** and why it is useful."
    ),
    "focus": (
        "You have a big exam next week. Write 1–2 sentences advising a friend on how to "
        "**focus** when studying at home."
    ),
    "frequently": (
        "Think of a healthy habit. Write 1–2 sentences explaining why doing it **frequently** "
        "leads to better results."
    ),
    "generally": (
        "Write 1–2 sentences about what students **generally** do to prepare for an important "
        "test, and whether you think this is effective."
    ),
    "contrast": (
        "Compare city life and countryside life. Write 1–2 sentences explaining the biggest "
        "**contrast** between the two."
    ),
    "contribution": (
        "Think of something small everyone in your class could do to keep the school clean. "
        "Write 1–2 sentences about how each person's **contribution** makes a difference."
    ),
    "increase": (
        "Your school wants more students to join a club or activity. Write 1–2 sentences "
        "suggesting one way to **increase** interest among students."
    ),
    "interact": (
        "You have a new student in your class who seems nervous. Write 1–2 sentences explaining "
        "how you would **interact** with them to make them feel welcome."
    ),
    "provide": (
        "Your school is organising a community day. Write 1–2 sentences explaining what your "
        "class could **provide** for the event and why."
    ),
    "region": (
        "Think of a food or custom that is special to a particular **region** of your country or "
        "the world. Write 1–2 sentences describing it."
    ),
    "relationship": (
        "Think of an important **relationship** in your life — with a friend, teacher, or family "
        "member. Write 1–2 sentences explaining why it matters to you."
    ),
    "research": (
        "You want to write an essay on a topic you know little about. Write 1–2 sentences "
        "explaining how you would do **research** to gather the information you need."
    ),
    "select": (
        "Your teacher asks you to **select** a book for independent reading. Write 1–2 sentences "
        "explaining which book you would choose and why."
    ),
    "suitable": (
        "Your younger sibling asks you to recommend a film. Write 1–2 sentences explaining "
        "whether the film you like is **suitable** for them and why."
    ),
    "strategy": (
        "You have been getting low scores on vocabulary quizzes. Write 1–2 sentences describing "
        "the **strategy** you will use to improve."
    ),
    "valid": (
        "A classmate argues that watching TV shows in English is not a **valid** way to learn the "
        "language. Write 1–2 sentences agreeing or disagreeing."
    ),
    "maintain": (
        "Write 1–2 sentences advising a friend on how to **maintain** good grades throughout the "
        "school year, not just before exams."
    ),
    "obtain": (
        "You need to use a photo from the internet in your school project. Write 1–2 sentences "
        "explaining what steps you should take to **obtain** permission."
    ),
    "available": (
        "Your school library has limited copies of a book you need. Write 1–2 sentences "
        "explaining what you would do if the book is not **available** when you need it."
    ),
    "accurately": (
        "Your teacher asks you to describe a graph. Write 1–2 sentences explaining why it is "
        "important to report the data **accurately**."
    ),
    "assistance": (
        "You are struggling with a difficult homework assignment. Write 1–2 sentences explaining "
        "who you would ask for **assistance** and why."
    ),
    "effective": (
        "Think of a study method you use. Write 1–2 sentences explaining why it is (or is not) "
        "**effective** for you."
    ),
    "connection": (
        "Write 1–2 sentences explaining the **connection** between reading regularly and "
        "improving your vocabulary."
    ),
    "affect": (
        "You have not been sleeping enough this week. Write 1–2 sentences explaining how "
        "a lack of sleep can **affect** your performance at school."
    ),
    "location": (
        "Your school is planning to build a new library. Write 1–2 sentences explaining "
        "the best **location** for it and why."
    ),
    "reduce": (
        "Your school wants to create less waste. Write 1–2 sentences suggesting one way "
        "students can **reduce** the amount of rubbish they produce each day."
    ),
    "site": (
        "Your class is creating a school website. Write 1–2 sentences explaining what "
        "information the **site** should include to be useful to students."
    ),
    "likely": (
        "Your friend says they will never improve at English because they made mistakes in "
        "class. Write 1–2 sentences using the word **likely** to encourage them."
    ),
    "no matter": (
        "Write 1–2 sentences advising a classmate who wants to give up studying. "
        "Use the phrase **no matter** to show that effort is always worthwhile."
    ),
    "valuable": (
        "Think about something you have learned this year that is **valuable** to you. "
        "Write 1–2 sentences explaining what it is and why it matters."
    ),
    "communication": (
        "Your school is starting a peer-tutoring programme. Write 1–2 sentences explaining "
        "why good **communication** between students is essential for the programme to work."
    ),
}



# ---------------------------------------------------------------------------
# CLI  (v2 — uses modular pipeline)
# ---------------------------------------------------------------------------
# The data dicts above (FILL_IN_SENTENCES, FILL_IN_HINTS, C1_DEFINITIONS,
# SYNONYM_MCQ, ERROR_ANALYSIS, REAL_WORLD_PROMPTS) are imported by
# generator_template.py.  All generation and I/O logic lives in the
# other v2 modules.  This file is now the CLI entry point only.
# ---------------------------------------------------------------------------

import argparse
from pathlib import Path

import word_store
import quiz_builder
import generator_template
import generator_claude
import writer_markdown
import writer_docx


def main():
    parser = argparse.ArgumentParser(
        description="GW Vocabulary Quiz Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python quiz_generator.py --quiz 3
  python quiz_generator.py --quiz 3 --book gw3
  python quiz_generator.py --quiz 3 --no-ai
  python quiz_generator.py --quiz 3 --docx
  python quiz_generator.py --list --book gw3
  python quiz_generator.py --quiz 1 --wordlist path/to/custom.json
""",
    )
    parser.add_argument("--quiz", type=int, default=1, metavar="N",
                        help="Quiz number to generate (default: 1)")
    parser.add_argument("--list", action="store_true",
                        help="List all quiz groups without generating")
    parser.add_argument("--book", choices=["gw2", "gw3"], default="gw2",
                        help="Word list to use: gw2 (default) or gw3")
    parser.add_argument("--wordlist", metavar="PATH",
                        help="Path to a custom word list JSON (overrides --book)")
    parser.add_argument("--no-ai", action="store_true",
                        help="Skip Claude API; use static templates only")
    parser.add_argument("--docx", action="store_true",
                        help="Also export a DOCX file (requires python-docx)")
    args = parser.parse_args()

    words = word_store.load(book=args.book, wordlist_path=args.wordlist)
    total = word_store.total_quizzes(words)
    output_dir = Path(__file__).parent

    if args.list:
        book_label = args.wordlist or args.book
        print(f"Book: {book_label} | Total words: {len(words)} -> {total} quizzes of 15 words each\n")
        for q in range(1, total + 1):
            batch = word_store.get_quiz_words(words, q)
            page_range = f"pp. {batch[0]['page']}–{batch[-1]['page']}"
            word_list = ", ".join(w["word"] for w in batch)
            print(f"Quiz {q:02d} ({page_range}): {word_list}")
        return

    if args.quiz < 1 or args.quiz > total:
        print(f"Error: Quiz number must be between 1 and {total}.")
        return

    quiz_words = word_store.get_quiz_words(words, args.quiz)
    generator = generator_template if args.no_ai else generator_claude
    quiz = quiz_builder.build(args.quiz, quiz_words, args.book, generator)

    md_path = writer_markdown.write(quiz, output_dir)
    print(f"Markdown saved to: {md_path}")

    if args.docx:
        try:
            docx_path = writer_docx.write(quiz, output_dir)
            print(f"DOCX saved to: {docx_path}")
        except ImportError as e:
            print(f"Warning: {e}")


if __name__ == "__main__":
    main()
