from django.shortcuts import render
from urllib import parse
import json


def welcome(request):
    return render(request, 'wordish/startPage.html', {'message':'welcome to wordish'})
    

def start(request):
    # targetText = request.POST["newTarget"]
    targetText = "doppler"
    context = {}
    # if len(targetText) != 5 or (not targetText.isalpha()):
    #     context['message'] = "invalid input"
    #     return render(request,'wordish/startPage.html', context) 
        
    initialGame = [] 
    for i in range(0, 8):
        row = []
        for j in range(0, 7):
            id = 'cell_' + str(i) + '_' + str(j)
            color = 'white'
            row.append((id, color, ''))
        initialGame.append(row)
        
    context['cur_row'] = 0
    context['newTarget'] = targetText
    context['status'] = 'start'
    context['gameString'] = parse.quote(json.dumps(initialGame))
    context['game'] = initialGame
    return render(request, 'wordish/wordish.html', context)


def guess(request):
    context = {}
    currentGame = None
    row = None 
    
    try:
        if request.POST['newGuess'] is None or request.POST['newTarget'] is None or request.POST['cur_row'] is None or \
                request.POST['gameString'] is None:
            print()
            
        currentGame = json.loads(parse.unquote(request.POST["gameString"]))
        row = int(request.POST["cur_row"],10)
    except:
        context["message"] = "error: invalid input"
        return render(request, 'wordish/startPage.html', context)
    
    if(len(request.POST["newTarget"]) != 7 or not request.POST["newTarget"].isalpha()):
        context["message"] = "error: invalid target"
        return render(request, 'wordish/startPage.html', context)    
    
    guessText = request.POST["newGuess"]
    targetText = request.POST["newTarget"]
    
    
    
    if (row > 7):
        return 
    
    if len(guessText) != 7 or not guessText.isalpha():
        context['status'] = "invalid input"
        context['cur_row'] = row
        context['newTarget'] = targetText
        context['gameString'] = parse.quote(json.dumps(currentGame))
        context['game'] = currentGame
        return render(request,'wordish/wordish.html', context) 
    
    map = {}
    for i in range(0, 7):
        target_letter = targetText[i]
        if (map.__contains__(target_letter)):
            map.__setitem__(target_letter, map.get(target_letter) + 1)
        else:
            map.__setitem__(target_letter, 1)
        
    visit = [False, False, False, False, False, False, False]
    
    
    newRow = []
    for i in range(0, 7):
        letter = guessText[i]
        target_letter = targetText[i]
        if (target_letter == letter):
            visit[i] = True
            currentGame[row][i][1] = 'green'
            currentGame[row][i][2] = letter
        
            count = map.get(target_letter) - 1
            if (count == 0):
                map.__delitem__(target_letter)
            else:
                map.__setitem__(target_letter, count)
                       
                
    for i in range (0,7):
        if (visit[i]):
            continue
        if (map.__contains__(guessText[i])):
            currentGame[row][i][1] = 'yellow'
            currentGame[row][i][2] = guessText[i]
            count = map.get(guessText[i]) - 1
            if (count == 0):
                map.__delitem__(guessText[i])
            else:
                map.__setitem__(guessText[i], count)
            continue
        currentGame[row][i][1] = 'lightgray'
        currentGame[row][i][2] = guessText[i]
    
    
    row += 1
    if (guessText == targetText):
        context['status'] = "See you there baby mua!"
        context['cur_row'] = row
        context['newTarget'] = targetText
        context['gameString'] = parse.quote(json.dumps(currentGame))
        context['game'] = currentGame
        return render(request,'wordish/wordish.html', context) 
    
    
    if (row == 8): 
        context['status'] = "love you~ try again!"
        context['cur_row'] = row
        context['newTarget'] = targetText
        context['gameString'] = parse.quote(json.dumps(currentGame))
        context['game'] = currentGame
        return render(request,'wordish/wordish.html', context) 
            
            
    context['cur_row'] = row
    context['newTarget'] = targetText
    context['status'] = 'successful input'
    context['gameString'] = parse.quote(json.dumps(currentGame))
    context['game'] = currentGame
    return render(request, 'wordish/wordish.html', context)
