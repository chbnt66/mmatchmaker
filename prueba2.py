# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 22:53:30 2023

@author: Javier
"""
import pandas as pd
import numpy as np
from flask import Flask, request, render_template

app = Flask(__name__)



# Ruta al archivo Excel con los datos de los luchadores y sus rivales
archivo_excel = 'datos_luchadores.xlsx'

def calcular_mejor_rival(nombre_luchador, location):
    data = pd.read_excel('rankfeed_09082023.xlsx')
    df = data.copy()

    variables_to_remove = ["number", "date", "weight_class_name", "link_title", "regional_rank", "gender"]
    for val in variables_to_remove:
        del df[val]


    myfighter = nombre_luchador
    
    if myfighter not in df['name'].values:
        return None
    elif location not in df['home_country'].values:
        return None
    else:
    # i=1
    # while i==1:
    #     if myfighter not in df['name'].values:
    #         print(f"Le nom {myfighter} n'existe pas dans le DataFrame.")
    #         myfighter = input("Check the spelling, or choose another fighter. Write the name: ")
    #     else:
    #        #print(f"The name {myfighter} existe dans le DataFrame, patience, nous recherchons le meilleur combat...")
    #         i=0
    # i=1  
    # while i==1:
    #     if location not in df['home_country'].values:
    #         print(f"The country {location} does not host fights or is wrongly spelled.")
    #         location = input("Please, check the spelling, or choose another country: ")
    #     else:
    #         print(f"The fight is in {location}, we now are looking for the best fight...")
    #         i=0
    
        index1 = np.where(df['name'] == myfighter) # find the index of your fighter in the table
        index1 = index1[0]
    
        # EXTRACT ALL THE FIGHTER FROM THE SAME WEIGHT CLASS
        
        weight_fighter_code = df['weight_class_code'][index1] # take the weight class code of the fighter
        weight_fighter_code = weight_fighter_code.values[0]
        
        #TABLE WITH THE FIGHTERS IN THE SAME CATEGORY
        newdf = df[df['weight_class_code'] == weight_fighter_code].copy()
        
        
        fighter_organization = df['organization'][index1]
        fighter_organization = fighter_organization.values
        fighter_organization = fighter_organization[0]
        
        newdf= newdf[newdf['organization']==fighter_organization]
        newdf = newdf.sort_values(by='rank')
        newdf = newdf.reset_index(drop=True)
        index = np.where(newdf['name'] == myfighter) # find the index of your fighter in the table
        index = index[0][0]
        if len(newdf)>=20:
            if index <= 4:
                newdf = newdf.head(9)
            elif index <= 10:
                newdf = newdf.head(index+10)
            elif len(newdf)-index < 10:
                newdf = newdf.iloc[index-10 :]
            else :
                newdf = newdf.iloc[index-10:index+11]
        newdf = newdf.reset_index(drop=True)
        
        print(newdf)
        
        def last5(x):
            l5 = np.zeros(len(x))
            for i in range(len(x)):            
                y = x['last_5'][i].split('|')
                
                if y[4] == 'W':
                    l5[i] += 5            
                elif y[4] == 'D':
                    l5[i] += 2
                    
                if y[3] == 'W':
                    l5[i] += 3
                elif y[3] == 'D':
                    l5[i] += 2
                    
                if y[2] == 'W':
                    l5[i] += 2
                elif y[2] == 'D':
                    l5[i] += 1
            return l5
        last5(newdf)
        
        def pro_record(x):
            lpro = np.zeros(len(x))
            for i in range(len(x)):        
                pr = x['pro_record'][i].split('-')
                n = int(pr[0])+int(pr[1])+int(pr[2])
                lpro[i] = (int(pr[0])*10)/n
                print(pr)
            return lpro
        pro_record(newdf)
        
        def finish_rate(x):
            fin = np.zeros(len(x))
            for i in range(len(x)):        
                pr = x['win_finish_pct'][i].split('%')
                fin[i] = np.float64(pr[0])/10
            return fin
        
        print(finish_rate(newdf))
        
        
        index2 = np.where(newdf['name'] == myfighter)
        index2 = index2[0][0]
        my_fighter_country = newdf['home_country'][index2]
        print(location)
        
        def loca(x):
            loc = np.zeros(len(x))
            for i in range(len(x)):
                
                if location == my_fighter_country :
                    if newdf['home_country'][i] == location :
                        loc[i]= 7.5
                    else : loc[i] = 10
                else : 
                    if newdf['home_country'][i] == location :
                        loc[i] = 2.5
                    else : loc[i] = 5
            return loc
        
        loca(newdf)
        
        def experience(x):
            xp = np.zeros(len(x))
            number_of_fights = []
            debut = []
            myfighter_debut = x['pro_debut_date'][index2]
            for i in range(len(x)):
                pr = x['pro_record'][i].split('-')
                prd = x['pro_debut_date'][i]
                debut.append(prd)
                number_of_fights.append(int(pr[0])+int(pr[1])+int(pr[2]))
            for i in range(len(x)):
                maximum = max(number_of_fights)
                xp[i] = (number_of_fights[i]/maximum)*7
                if debut[i]<myfighter_debut :
                    xp[i]+=3
                elif debut[i]==myfighter_debut :
                    xp[i]+=2
                else  : xp[i]+=1
            return xp
        
        experience(newdf)
        
        
        def last5_single(x):            
            y = x['last_5'].split('|')
            l5 = 0    
            if y[4] == 'W':
                l5 += 5            
            elif y[4] == 'D':
                l5 += 2
                    
            if y[3] == 'W':
                l5 += 3
            elif y[3] == 'D':
                l5 += 2
                    
            if y[2] == 'W':
                l5 += 2
            elif y[2] == 'D':
                l5 += 1
            return l5
        
        
        def pro_record_single(x):       
            pr = x['pro_record'].split('-')
            n = int(pr[0])+int(pr[1])+int(pr[2])
            lpro = (int(pr[0])*10)/n
            return lpro
        
        
        def last_opp(x) :
            
            last_opponent_list = np.zeros(len(x))
            
            for i in range(len(x)) :
                last_opponent = x['last_opponent'][i]
                
                #print('last_opponent : ', last_opponent ,' and ', type(last_opponent))
                
                if last_opponent == '' :
                    print(' We have no information about the last opponent of ',x['name'][i])
                else : 
                    index_last_opponent = np.where(df['name'] == last_opponent) # find the index of  the last opponent le
        
                    if len(index_last_opponent[0]) == 0:
                        print(' The last opponent of ',x['name'][i], ' is ', last_opponent, ' but we have no information about this fighter.')
                        
                    else : 
                        
                        index_last_opponent = index_last_opponent[0][0]
                        index_our_opponent = np.where(df['name'] == x['name'][i])
                        index_our_opponent = index_our_opponent[0][0]
                    
                    
                    
                        if df['rank'][index_last_opponent] > df['rank'][index_our_opponent] and  df['rank'][index_last_opponent] > df['rank'][index1].values[0] :
                        
                            last_opponent_list[i] += 10
                            last_opponent_list[i] += last5_single(df.iloc[index_last_opponent])
                            last_opponent_list[i] += pro_record_single(df.iloc[index_last_opponent])
                            last_opponent_list[i] = last_opponent_list[i] /3
                    
                        if df['rank'][index_our_opponent] > df['rank'][index_last_opponent] > df['rank'][index1].values[0] or df['rank'][index1].values[0] > df['rank'][index_last_opponent] > df['rank'][index_our_opponent]  :
                        
                            last_opponent_list[i] += 10* 2/3
                            last_opponent_list[i] += last5_single(df.iloc[index_last_opponent])
                            last_opponent_list[i] += pro_record_single(df.iloc[index_last_opponent])
                            last_opponent_list[i] = last_opponent_list[i] /3
                            
                        else : 
                        
                            last_opponent_list[i] += 10 * 1/3
                            last_opponent_list[i] += last5_single(df.iloc[index_last_opponent])
                            last_opponent_list[i] += pro_record_single(df.iloc[index_last_opponent])
                            last_opponent_list[i] = last_opponent_list[i] /3
                        
            return(last_opponent_list)
                        
                        
                
        last_opp(newdf)   
        
        
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        
        
                
                
        def last_fight_date(x) : 
            
            y= datetime.now()
            
            last_fight_date = np.zeros(len(x))  # create an empty list
                
            
            for i in range(len(x)) :
                
                if x['last_fight_date'][i] == '' :
                    print('there is no information about the last fight date of ', x['name'][i])
                    last_fight_date[i] += 5
                else :   
                    
                    date_aux = x['last_fight_date'][i].split(' ')
                    date_aux = date_aux[0]
                    date_last_fight = datetime.strptime(date_aux, "%Y-%m-%d").date() 
                    
                    
                    delta = relativedelta(y, date_last_fight)
                    
                    if  0<= delta.months <= 4 :
                        last_fight_date[i] = 10
                        
                    elif  4< delta.months <= 8:
                        
                        last_fight_date[i] = 8 
                    
                    elif 8< delta.months <= 11  :
                        
                        last_fight_date[i] = 6
                        
                    elif 1 <= delta.years < 2 :
                        
                        last_fight_date[i] = 4
                        
                    else :
                        last_fight_date[i] = 2
                        
            return(last_fight_date)
                    
                   
                    
                    
                    
            
        last_fight_date(newdf)
            
        
        
        def grade_comparison(x) :
            index = np.where(newdf['name'] == myfighter) # find the index of your fighter in the table
            index = index[0]
            print('index my fighter',index)
            
            note_ponderation =  ( 5*last5(x) + 4*pro_record(x) + 4*finish_rate(x)+ 3*loca(x)+ 3*experience(x)+ 3*last_opp(x)+ 3 *last_fight_date(x) ) / 25
            
            target_value = note_ponderation[index]  # take the grade of our fighter
            
            
            absolute_differences = np.abs(note_ponderation - target_value)
            absolute_differences[index] = 10  # to make sure that we don't have our fighter in output
            
            index_of_closest_element = np.where(absolute_differences == np.min(absolute_differences)) # Find the index of the element with the smallest absolute difference
            index_of_closest_element = index_of_closest_element[0]
            mejor_rival = newdf['name'][index_of_closest_element].values[0]
            
            print('the best fight for your fighter is : ',newdf['name'][index_of_closest_element])
            
            #return(note_ponderation) 
            return mejor_rival
        
        grade_comparison(newdf)
        
        def grade_best(x) :
            index = np.where(newdf['name'] == myfighter) # find the index of your fighter in the table
            index = index[0]
            print('index my fighter',index)
            
            note_ponderation =  ( 5*last5(x) + 4*pro_record(x) + 4*finish_rate(x)+ 3*loca(x)+ 3*experience(x)+ 3*last_opp(x)+ 3 *last_fight_date(x) ) / 25
            
            note_ponderation[index] = 0 #to make sure that we do not output our fighter
            
            
            
            index_best = np.where(note_ponderation == np.max(note_ponderation))
            
            index_best = index_best[0][0]  # assuming that the grades can't be the same
        
        
            print('the best fight for your fighter is : ',newdf['name'][index_best])
            return(note_ponderation)
        
        grade_best(newdf)
        # Supongamos que el DataFrame tiene columnas 'Luchador' y 'Mejor Rival'
        # Encuentra el mejor rival para el luchador dado
        
    
        return grade_comparison(newdf)


@app.route('/', methods=["GET", "POST"])
def luchador():
    if request.method == "POST":
        # Obtén el nombre del luchador ingresado por el usuario
        nombre_luchador = request.form.get("luchador")
        location = request.form.get("lugar")

        # Calcula el mejor rival
        mejor_rival = calcular_mejor_rival(nombre_luchador, location)

        # Renderiza una plantilla HTML con el resultado
        if mejor_rival is not None:
            return "The best rival is "+mejor_rival
        else:
            error_message = "El nombre del luchador no se encuentra en la base de datos. Por favor, inténtelo de nuevo."
            return render_template("form.html", error_message=error_message)
        
    return render_template("form.html")

if __name__ == '__main__':
    app.run()
