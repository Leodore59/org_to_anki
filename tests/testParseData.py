import sys
sys.path.append('../org_to_anki')

from org_to_anki.org_parser import parseData
from org_to_anki.ankiClasses.AnkiQuestion import AnkiQuestion
from org_to_anki.ankiClasses.AnkiDeck import AnkiDeck


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


def testTopicsDataParse():

    # Creat deck with two subdecks
    filename = "tests/testData/topicsLayout.org"
    actualDeck = parseData.parse(filename)
    
    expectedDeck = AnkiDeck("topicsLayout") 
    # TODO sperate out top level deck parsing test from topics layout
    expectedDeck.addParameter("fileType", "topics") 
    expectedDeck.addComment("# More advanced org file layout. Each topics has its own questions.")
    expectedDeck.addComment("#fileType = topics")

    firstSubDeck = AnkiDeck("Capital cites")
    q1 = AnkiQuestion("What is the capital of Ireland")
    q1.addAnswer("Dublin")
    firstSubDeck.addQuestion(q1)
    expectedDeck.addSubdeck(firstSubDeck)

    secondSubDeck = AnkiDeck("Languages of countries")
    q2 = AnkiQuestion("What are the main languages in Ireland")
    q2.addComment("#type=reverse")
    q2.addParameter('type', "reverse")
    q2.addAnswer("English")
    q2.addAnswer("Irish")

    secondSubDeck.addQuestion(q2)
    secondSubDeck.addComment("#type=basic")
    secondSubDeck.addParameter("type","basic")
    expectedDeck.addSubdeck(secondSubDeck)

    # Assert deck built correctly
    assert(actualDeck == expectedDeck)
    assert(actualDeck.getQuestions() == expectedDeck.getQuestions())


