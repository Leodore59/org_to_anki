import sys
sys.path.append('../org_to_anki')

from org_to_anki.org_parser import parseData
from org_to_anki.ankiClasses.AnkiQuestion import AnkiQuestion
from org_to_anki.ankiClasses.AnkiDeck import AnkiDeck


### Test basic deck is parsed and built correctly ###

def testBasicParseData():

    filename = "tests/testData/basic.org"
    actualDeck = parseData.parse(filename)

    expectedDeck = AnkiDeck("basic")
    expectedDeck.addComment("# Quick Anki notes")

    # build Question
    expectedQuestion = AnkiQuestion("Put request")
    expectedQuestion.addParameter('type', 'basicTest')
    expectedQuestion.addParameter('other','test')
    expectedQuestion.addComment("# type=basicTest, other=test")

    expectedQuestion.addAnswer("Puts file / resource at specific url")
    expectedQuestion.addAnswer(
        "If file ==> exists => replaces // !exist => creates")
    expectedQuestion.addAnswer("Request => idempotent")

    expectedDeck.addQuestion(expectedQuestion)

    assert(actualDeck == expectedDeck)

### Test basic deck parse with sublevels ###

def testBasicWithSublevelsParseData():

    filename = "tests/testData/basicWithSublevels.org"
    actualDeck = parseData.parse(filename)

    expectedDeck = AnkiDeck("basicWithSublevels")
    # build Question
    expectedQuestion = AnkiQuestion(
        "What is the difference between .jar and .war files in java")
    expectedQuestion.addAnswer(
        ".jar => contains libraries / resources / accessories files")
    expectedQuestion.addAnswer(
        ".war => contain the web application => jsp / html / javascript / other files")
    expectedQuestion.addAnswer("* Need for web apps")
    expectedDeck.addQuestion(expectedQuestion)

    assert actualDeck == expectedDeck


def testFormatFile():
    filename = "tests/testData/basic.org"
    data = parseData._formatFile(filename)

    assert(len(data) == 7)


def testSortData():

    lines = """#Comment 1
    # Indented comment 2

* line 1
# type=basic
** line 2
badlyformated line
""".split("\n")

    assert(len(lines) == 8)
    comments, content = parseData._sortData(lines)
    print(comments)
    print(content)

    assert(len(comments) == 2)
    assert(len(content) == 4)


def testConvertCommentsToParameters():

    comments = ["#fileType=basic, secondArg=10", "##file=basic", "#fileType2 = topics"]
    result = parseData.convertCommentsToParameters(comments)
    expected = {'fileType': 'basic', 'secondArg': '10', 'file': 'basic', 'fileType2': 'topics'}
    assert(result == expected)

### Test topics deck built correctly ###

def testTopicsDeckNamedCorrectly():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    assert(actualDeck.deckName == "topicsLayout")

def testTopicsSubDecksNamedCorrectly():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    assert(actualDeck.subDecks[0].deckName == "Capital cites")
    assert(actualDeck.subDecks[1].deckName == "Languages of countries")

def testMainDeckHasComment():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    comments = ['# More advanced org file layout. Each topics has its own questions.', '#fileType = topics']
    assert(actualDeck._comments == comments)

def testMainDeckHasParameters():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    params = {'fileType': 'topics'}
    assert(actualDeck._parameters == params)

def testSubDeck1HasParamters():
    
    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    params = {'type': 'basic'}
    comments = ["#type=basic"]
    assert(actualDeck.subDecks[1]._comments == comments)
    assert(actualDeck.subDecks[1]._parameters == params)

def testSubDeck1QuestionHasParamters():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)
    
    params = {'type': 'reverse'}
    comments = ["#type=reverse"]
    assert(actualDeck.subDecks[1].getQuestions()[0]._parameters == params)
    assert(actualDeck.subDecks[1].getQuestions()[0]._comments == comments)

def testSubDeck0HasBasicQuestion():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    q1 = AnkiQuestion("What is the capital of Ireland")
    q1.addAnswer("Dublin")
    q1.deckName = "Capital cites"

    assert(actualDeck.subDecks[0].getQuestions()[0].question == "What is the capital of Ireland")
    assert(actualDeck.subDecks[0].getQuestions()[0]._answers == ["Dublin"])

def testSubDeck1HasBasicQuestion():

    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)

    assert(actualDeck.subDecks[1].getQuestions()[0].question == "What are the main languages in Ireland")
    assert(actualDeck.subDecks[1].getQuestions()[0]._answers == ["English", "Irish"])


