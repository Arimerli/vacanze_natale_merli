import random
import time

punt1 = 0
punt2 = 0
punti = [0,0]
game = [0,0]
while True:
    vincente = random.randint(0,1)
    if punti[vincente] == 0:
        punti[vincente] = 15
    elif punti[vincente] == 15:
        punti[vincente] = 30
    elif punti[vincente] == 30:
        punti[vincente] = 40
    else:
        if punti[1-vincente] == 40:
            if len(punti) == 2:
                punti.append(vincente)
            else:
                if punti[2]==vincente:
                    game[vincente]+=1
                    punti = [0,0]
                else:
                    punti.pop(2)
        else:
            game[vincente] += 1
            punti = [0, 0]
        if game[vincente] == 6 and game[vincente - 1] < 5:
            punti = [0, 0]
            game = [0,0]
            if vincente == 0:
                punt1 += 1
            else:
                punt2 += 1
        if game[vincente] == 7:
            punti = [0, 0]
            game = [0, 0]
            if vincente == 0:
                punt1 += 1
            else:
                punt2 += 1
    print(punti, game, punt1, punt2)
    time.sleep(0.5)

#<p>{{ partite[0]['giocatore1'] }} VS {{ partite[0]['giocatore2'] }}                 {{ partite[0]['setg1'] }}:{{ partite[0]['setg2'] }}</p>