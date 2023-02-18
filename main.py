
import re
import random
import fitz
import os
import requests
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PollHandler,  
)
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import constants
from pdfminer.high_level import extract_text
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import *
from telegram.ext import CommandHandler, CallbackQueryHandler,ConversationHandler
class Question:
    def __init__(self, q, a1,a2,a3,a4,a5, figureName= "") : #a question and its answers
        self.question = q
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.a5 = a5
        self.correctAnswer = a1 #fixed
        self.ans = [self.a1,self.a2,self.a3,self.a4, self.a5]
        self.figureName = figureName
        random.shuffle(self.ans)
        random.shuffle(self.ans)
    def getQuestion(self):
        return self.question
    def getAns(self):
        return self.ans
    def getCorrectAns(self):
        return self.correctAnswer
    def containsFigure(self):
        return "figure" in self.question.lower() 
    def lengthExceeded(self):
        return len(self.question)  >= constants.PollLimit.MAX_QUESTION_LENGTH # the max length for a poll question
    def setFigureName(self, name):
        self.figureName = name
    def getFigureName(self):
        return self.figureName

def findMatches(compile):
    pattern = re.compile(compile)
    matches = pattern.finditer(data)
    return matches 

path1 ="https://resources.stkfupm.com/vfm-admin/vfm-downloader.php?q=dXBsb2Fkcy9QSFlTL1BIWVMxMDIvT2xkJTIwRXhhbXMvRmlyc3QlMjBNYWpvci9QSFlTMTAyX18yMjFfX01ham9yMV9fU29sdmVkLnBkZg==&h=e1a099578441d1cac467327813c69874"
path2 ="https://resources.stkfupm.com/vfm-admin/vfm-downloader.php?q=dXBsb2Fkcy9QSFlTL1BIWVMxMDIvT2xkJTIwRXhhbXMvRmlyc3QlMjBNYWpvci9QSFlTMTAyX18yMTJfX01ham9yMV9fU29sdmVkX19aRVJPLV9WRVJTSU9OLnBkZg==&h=7d8af705997b52b85c4853dbd6e1a313"
path3 ="https://resources.stkfupm.com/vfm-admin/vfm-downloader.php?q=dXBsb2Fkcy9QSFlTL1BIWVMxMDIvT2xkJTIwRXhhbXMvRmlyc3QlMjBNYWpvci9QSFlTMTAyX18yMTNfX01ham9yMV9fU29sdmVkLnBkZg==&h=b0a21d5bcfdd91d14bd0042515a6dbf7"
path4 = "http://resources.stkfupm.com/vfm-admin/vfm-downloader.php?q=dXBsb2Fkcy9QSFlTL1BIWVMxMDIvT2xkJTIwRXhhbXMvRmlyc3QlMjBNYWpvci9QaHlzMTAyLTE4MS1GaXJzdC1NYWpvci1aZXJvLVZlcnNpb24tUG9zdC5wZGY=&h=5d83c961b4ea66bbdcf16bbcb4331f00"
path5 = "http://resources.stkfupm.com/vfm-admin/vfm-downloader.php?q=dXBsb2Fkcy9QSFlTL1BIWVMxMDIvT2xkJTIwRXhhbXMvRmlyc3QlMjBNYWpvci9QSFlTMTAyX18xNzNfX01ham9yMV9fU29sdmVkX19aZXJvLVZlcnNpb24ucGRm&h=ec2a0f71698702b34b5228ce7d5b2cf9"
path6 = "http://resources.stkfupm.com/vfm-admin/vfm-downloader.php?q=dXBsb2Fkcy9QSFlTL1BIWVMxMDIvT2xkJTIwRXhhbXMvRmlyc3QlMjBNYWpvci9QSFlTMTAyX18wOTJfX09sZC1FeGFtX19GaXJzdC1NYWpvcl9fTWFzdGVyLUtleS5wZGY=&h=6b5d6b272c6c02eb5d044dce1c43faf7"
paths = [path1,path2,path3,path4, path5,path6]
listObject = []
term = 1

for path in paths:
    with open("PDFF.pdf", 'wb') as file:
        r = requests.get(path , stream= False)
        file.write(r.content)
    pdf = fitz.open("PDFF.pdf")
    pages = len(pdf)
    count = 0
    data = extract_text("PDFF.pdf")
    data = data.replace("\n" , "")

    
    questionsIndices = []
    for match in findMatches("Q[0-9]|[0-3][0-9]\.\s"): # a pattern consist of the letter Q followed by a number followed by a dot and a space 
        span =match.span()
        questionsIndices.append(span[0])
        count  +=1

    firstChoice = []
    for match in findMatches("A\n?\)\s"): 
        span =match.span()
        firstChoice.append(span[0])   
        count  +=1
    endIndices = []
    lastChoice = []
    count =0 
    for match in findMatches("E\)\s"): 
        span = match.span()
        if(count <= 20): 
            follow =span[0]
            for i in range(constants.PollLimit.MAX_QUESTION_LENGTH *2):
                if(data[follow ]== "Q"):
                    num = follow
                    break
                if(data[follow:follow+2] == "Ki" or data[follow:follow+2] =="Fi"):
                        num = follow
                        break
            
                follow = follow +1
            newLineIndex =num
          
        else:
            newLineIndex = len(data) -1
        endIndices.append(newLineIndex)
        count +=1
        
#Extracting questions
    index = 0
    questions = []
    extendedQuestions = []
    for i in range(len(questionsIndices)): #getting the answers
        start = questionsIndices[i]
        end = firstChoice[i] 
        question = data[start:end]
        questions.append(question)
        

    #Extracting images
    imgList = [] 

    for i in range(pages):
        content = pdf[i]
        imgList.extend(content.get_images())
        j = 0 
        names  = []
    for i , Image in enumerate(imgList,start =1 ):
            xref =imgList[j][0]                 
            baseImg = pdf.extract_image(xref)
            imgBytes = baseImg['image'] #the actual data that we wanna extract and send
            ext = baseImg['ext']
            name = str(term) + str(i) + "."+ext
            
            names.append(name)
            with open(os.path.join("images" , name), 'wb') as imgOut:
                imgOut.write(imgBytes)
            j+=1
    term +=1
    

                
    questionObjects = []
    j=0
    nameIndx = 0
#Extracting answers
    for i in range(len(endIndices)): # answers done
        start = firstChoice[i]
        end = endIndices[i]
        answers = data[start:end]
     
        if("King" in answers):
            n= answers.index("King")
            letters = ["A","B" , "C" , "D" ,"E"]
            count = n
      
            while (answers[count] in letters == False) or answers[count+1] != ")":
                count = count +1
            answers = answers[0:n] +answers [count:]
        a = answers.index("A)")
        b = answers.index("B)")
        c = answers.index("C)")
        d= answers.index("D)")
        e= answers.index("E)")
        
  
        
        answer1 = answers[a:b].strip("A) ")
        answer2 = answers[b : c].strip("B) ")
        answer3= answers[c : d].strip("C) ")
        answer4 = answers[d : e].strip("D) ")
        answer5 = answers[ e: ].strip("E) ")
        
        question1 = questions[i]
        for c in question1:
            if c == "?":
                indx = question1.index("?")
                question1 = question1[:indx]

    
        question = Question(question1 , answer1,answer2,answer3,answer4,answer5)
        if(question.containsFigure()):
            question.setFigureName(names[nameIndx])
            nameIndx+=1
        questionObjects.append(question)
    listObject.append(questionObjects)






j = 0
def correctAnsPos(ans, correct):
    for i in range(len(ans)):
        if (ans[i] == correct):
            return i


def shorten(quest):
    j =len(quest) -1
    while(len(quest) >= constants.PollLimit.MAX_QUESTION_LENGTH):
        quest = quest [:j]
        j -=1
    return (quest , j)
async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Summarize a users poll vote"""
    answer = update.poll_answer
    answered_poll = context.bot_data[answer.poll_id]
    try:
        questions = answered_poll["questions"]
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        return
    selected_options = answer.option_ids
    answer_string = ""
    for question_id in selected_options:
        if question_id != selected_options[-1]:
            answer_string += questions[question_id] + " and "
        else:
            answer_string += questions[question_id]
    await context.bot.send_message(
        answered_poll["chat_id"],
        f"{update.effective_user.mention_html()} feels {answer_string}!",
    )
    answered_poll["answers"] += 1
    # Close poll after three participants voted
    if answered_poll["answers"] == 3:
        await context.bot.stop_poll(answered_poll["chat_id"], answered_poll["message_id"])


async def terms(update: Update, context: ContextTypes.DEFAULT_TYPE, n ) -> None:
     for i in listObject[n]:
        if i.containsFigure():
                await context.bot.send_photo(update.effective_chat.id,photo = open("images\\"+ i.getFigureName(), "rb"))
        pos =  correctAnsPos(i.getAns() , i.getCorrectAns())
        quest = i.getQuestion()
    
        exp = ""
        if(i.lengthExceeded()):
            holder= quest
            (quest , last) = shorten(quest)
            exp = holder[last:]
        ans = i.getAns()
        if(len(i.getAns()[0]) == 0  ):
            ans = ["EMpty"  , "Empt"]
            
        message = await context.bot.send_poll(
          update.effective_chat.id,
          quest,
          ans,
        is_anonymous=False,
        allows_multiple_answers=False,
        type= constants.PollType.QUIZ, 
        correct_option_id = pos, #the postion of the correct option 
        explanation = exp,
    )
       #ans = update.poll.get
        payload = {
        message.poll.id: {
            "questions": i.getAns(),
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": i.getCorrectAns(),
        }
       }
        context.bot_data.update(payload)

async def t221(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await terms(update, context,0 )
    await update.message.reply_text("-End of Term 221 Major-")
        
async def t212(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:


   await terms(update, context,1)
   await update.message.reply_text("-End of Term 212 Major-")
  
  
async def t213(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await terms(update, context,2)
    await update.message.reply_text("-End of Term 213 Major-")

async def t181(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await terms(update, context,3)
  await update.message.reply_text("-End of Term 181 Major-")

async def t173(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await terms(update, context,4)
    await update.message.reply_text("-End of Term 173 Major-")

async def t112(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await terms(update, context,5)
    await update.message.reply_text("-End of Term 112 Major-") 



async def start(update, context):
    options = []
    options.append(InlineKeyboardButton(text = "Term 221",callback_data= "1"))
    options.append(InlineKeyboardButton(text = "Term 213" ,callback_data='2'))
    options.append(InlineKeyboardButton(text = "Term 212" ,callback_data='3'))
    options.append(InlineKeyboardButton(text = "CODE" ,url = "https://github.com/iLawFD/Poll-quizes-maker"))
    markup = InlineKeyboardMarkup([options])
  
    await update.message.reply_text("Hi this is a poll bot for physics 102's majors. Please select the desired term" ,reply_markup=markup)
    await update.message.reply_text("or simply write the command e.g(/181)")
    choice = update.callback_query
    
async def buttons(update, context):
    query = update.callback_query
    await query.answer()
    if(query.data =="1"):
       await t221(update, context)
    elif(query.data =="2"):
         await t213(update, context)
    elif(query.data == "3"):
        await t212(update, context)
        


t = "5437308058:AAHugylPmnwAj5xPgsK61DiYXJ2jvNgDFsE"
app = ApplicationBuilder().token(t).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(CommandHandler("221", t221))
app.add_handler(CommandHandler("212", t212))
app.add_handler(CommandHandler("213", t213))
app.add_handler(CommandHandler("181", t181))
app.add_handler(CommandHandler("173", t173))
app.add_handler(CommandHandler("112", t112))




app.run_polling()



   
   

 




