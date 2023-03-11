from palabras_ES import words
import random

def print_console(listshowword:list,letterused:str) -> tuple:
    """
    Funcion encargada de devolver los espacios de las letras no encontradas de la palabra a buscar, las letras encontradas en su repectiva posición y las letras utilizadas a lo largo de la partida.
    
    Parameters
    ----------
    listshowword : list, optional
        Contiene la palabra secreta pero no completa, a medida que la computadora arriesga letras, se va rellenando.
    letterused : str
        Almacena las letras que el usuario va ingresando para adivinar la palabra.

    Returns
    -------
    tuple
        La tupla devuelve los espacios de las letras no encontradas, las letras encontradas en su repectiva posición y las letras ya utilizadas.

    """
    
    showword=str(listshowword).replace("[","").replace("]","").replace("'","").replace(",","")
    return  ("\n" + showword + "\t("+ letterused +")",showword)

def list_showword(word:str,listshowword:list=[]) -> list:
    """
    Funcion dedicada a ocultar los caracteres de la palabra oculta, utilizando guiones.
    
    Parameters
    ----------
    word : str
        Almacena la palabra oculta.
    listshowword : list, optional
        Contiene la palabra secreta pero no completa, a medida que la computadora arriesga letras, se va rellenando.

    Returns
    -------
    list
        listshowword.

    """
    listshowword.clear()
    
    for i in range(len(word)):
        listshowword.append("_")
    return listshowword

def human_hangman(secretword:str="", triesremaning:int=5,showword:str="",letterused:str="") -> str:
    """
    Funcion dedicada a correr el modo de juego Human hangman, en el cual el usuario busca adivinar la palabra elegida por la computadora.
    
    Parameters
    ----------
    secretword : str, optional
        Almacena la palabra oculta.
    triesremaning : int, optional
        Almacena el numero de intentos que tiene el usuario para adivinar la palabra, los cuales se van descontando con cada letra errada. Hay 5 intentos por default.
    showword : str, optional
        Almacena la palabra a descubrir, mostrando con guiones de aquellas letras que todavia no se descubrieron.
    letterused : str, optional
        Almacena las letras que el usuario va utilizando a lo largo de la partida.

    Raises
    ------
    ValueError
        Se utiliza para evitar errores a la hora de ingresar caracteres por medio de los inputs.

    Returns
    -------
    str
        Muestra el resultado final correspondiente a la partida desarrollada.

    """
    secretword=random.choice(words)
    listshowword=list_showword(secretword)
    
    while triesremaning>0:
        #El juego se va a desarrollar hasta que se gasten los 5 intentos
        print(print_console(listshowword, letterused)[0])
        showword=print_console(listshowword, letterused)[1]
        if not("_") in showword:
            #Si no hay guiones en la palabra escondida, el juego finaliza, se ha encontrado la palabra.
            return "\nCongratulations!, you find the secret word " + secretword
        print("\n",triesremaning,"tries remaning.")
        while True:
            #Evitamos que se ingresen datos no deseados.
            try:
               humaninput=(input("Put a caracter or a word: ")).lower()
               if not humaninput.isalpha() or len(humaninput)!=len(secretword) and len(humaninput)!=1:
                   raise ValueError
               break
            except ValueError:
                print("\nOops!  There was a problem. Try again...")
        if len(humaninput)>1:
            if humaninput==secretword:
                #Si el usuario arriesga una palabra completa.
                return "\nCongratulations!, you find the secret word " + secretword
            else:
                break
        if humaninput not in letterused:
            #Almacenamos las letras ingresadas que no se hayan jugado.
            letterused+=humaninput
        elif not(humaninput in letterused and humaninput in secretword):
            #Sumamos un intento si el usuario ingresa una letra que ya no esta en la palabra secreta y la arriesga por 2da vez.
            triesremaning+=1
        if humaninput in secretword:
            #Si la letra ingresada esta en la palabra secreta, la remplazaremos.
            for position in range(len(secretword)):
                if secretword[position] == humaninput:
                    listshowword[position]=humaninput      
        else:
            #Si la letra arriesgada no esta en la palabra secreta, restamos un intento
            triesremaning-=1

    return "\nYou lose, the secret word was " + secretword

def computer_hangman(words_list:list=[],compute_letter:str="",triesremaning:int=5,findword:str="",letterused:str="",position:int=0,showword:str="",listshowword:list=[],end:str="") -> str:
    """
    Esta funcion conciste en el modo de juego automatico, donde la computadora buscara encontrar una palabra secreta ingresada por el usuario. 
    
    Parameters
    ----------
    words_list : list, optional
        Lista de palabras.
    compute_letter : str, optional
        Almacena las letras que la computadora prueba para tratar de adivinar la palabra.
    triesremaning : int, optional
        Almacena el numero de intentos de la computadora a la hora de ariesgar una letra. Hay 5 intentos.
        intentos por default.
    findword : str, optional
        Almacena la palabra a encontrar por la computadora.
    letterused : str, optional
        Almacena las letras arriesgadas por la compuadora.
    position : int, optional
        Se utiliza para seleccionar la letra con mayor porcentaje de presencia en la lista.
    showword : str, optional
        Almacena la palabra a encontrar, colocando guiones en los lugares donde las letras no han sido descubiertas.
    listshowword : list, optional
        Contiene la palabra secreta pero no completa, a medida que la computadora arriesga letras, se va rellenando.
    end : str, optional
        El string puede ser una "y"(yes) o una "n" (no). 

    Raises
    ------
    ValueError
        Se utiliza para evitar errores a la hora de ingresar caracteres por medio de los inputs.
    Returns
    -------
    str
        Muestra el resultado final correspondiente a la partida desarrollada.

    """
    #El filtrado sera apor el tamaño,y luego por la probabilidad de que la letra sea la correspondiente
    listshowword.clear()
    words_list.clear()
    
    def sizeword(findword:str) -> list:
        """
        Función dedicada a crear una nueva lista que posea todas aquellas palabras del mismo tamaño que la palabra a encontrar por la computadora.
        
        Parameters
        ----------
        findword : str
            Almecena la palabra introducida por el usuario, la cual debe ser adivinada por la maquina.

        Returns
        -------
        list
            La lista contiene las palabras con la misma contidad de letras que la palabra a encontrarpor la computadora.

        """
        size_findword=len(findword)
        #Tamaño de la palabra a buscar
        for value in words:
            #Creamos una lista a partir del tamaño de la palabra ingresada.
            if size_findword == len(value):
                words_list.append(value)
            else:
                 continue
        return words_list   
      
    def probabilities(lista:list=[],probabilities_list:list=[],ocurrence:int=0,letters:str=0) -> list:
        """
        Funcion dedicada a caulculara el porsentaje de ocurrencia deletras dentro de las palabras de una lista.
        
        Parameters
        ----------
        lista : list, optional
            Contiene la lista de palabras.
        probabilities_list : list, optional
            Almacena el porsentaje de presencia de las letras de los elementos de la lista.
        ocurrence : int, optional
            Almacena el conteo de la ocurrencia de las letras.
        letters : str, optional
            Registra el conteo de todas las letras presentes en la lista.

        Returns
        -------
        list
            probabilities_list.

        """
        probabilities_list.clear()
        for i in range(97,123):
             for word in lista:
                 #Contamos la ocurrencia de cada letra en la lista completa para armar un promedio
                 if chr(i) in word:
                     ocurrence += word.count(chr(i))
                 #Aprovechamos el for para contar la cantidad de letras actual en toda la lista
                 if i == 97:
                 #Usamos la primer letra para contar la cantidad de letras
                     letters+=len(word) 
             ocurrence = ocurrence/letters
             #Calculamos promedio
             probabilities_list.extend([(ocurrence,chr(i))])
             #Extendemos la lista con una tupla del promedio y cada letra.
             ocurrence=0
        probabilities_list.sort(reverse=True)
        #Ordenamos la lista de letras y proimedios, de mayor a menor porcentaje.
        return probabilities_list  
     
    def yes_or_no() -> str:
        """
        Función dedicada a impedir que el usuario ingrese una indicacion a la computadora diferente a y (si) o n (no).
        
        Raises
        ------
        ValueError
            Se utiliza para evitar errores a la hora de ingresar caracteres por medio de los inputs.
            
        Returns
        -------
        str
            La salida puede ser una "y"(yes) o una "n" (no).

        """
        while True:
            try:
               end=input("[y/n]: ").lower()
               if end!="n" and end!="y":
                   raise ValueError
               break
            except ValueError:
                print("\nOops!  This instance only takes letters beetween y (yes) or n (no).  Try again...")
        return end
    
    def lies_detector(letterused:str,findword:str,showword:str) -> (str,bool):
        """
        Funcion dedicada a detectar cuando el usuario le da indicaciones correctas a la computadora cuando esta busca adivinar la palabra.
        
        Parameters
        ----------
        findword : str, optional
            Alacena la palabra a encontrar por la computadora.
        letterused : str, optional
            Almacena las letras arriesgadas por la compuadora.
        showword : str, optional
            Almacena la palabra a encontrar, mostrando los repectivos espacios en blanco en los lugares donde las letras no han sido descubiertas.

        Returns
        -------
        str
            Nos arroja una advertencia, de que se han ingresado mal las letras, nos permite evitar la mentira hacia la maquina.
        bool
            Nos permite distinguir cuando se mintio y cuando no.

        """
        for i in letterused:
            if i in findword and i not in showword:
                return ("\n-------WARNING-------\nRespond appropriately to the machine so that it responds accordingly, do not deceive it", True)     
            else:
                continue
        return ("",False)
    
    def findword():
        """
        Funcion dedicada a limitar al usuario para que solo pueda ingresar una palabra presente en la lista de palabras del juego.
        
        Raises
        ------
        ValueError
            Se utiliza para evitar que el usuario ingrese una palabra que no este en la lista de palabras.

        Returns
        -------
        str
            La palabra a encontrar por la computadora.

        """
         
        while True:
            try:
               findword=(input("Put a word and the computer will try to find :")).lower()
               if findword not in words:
                   raise ValueError
               break
            except ValueError:
                print("\nOops!  The word that you select, doesn't exist in the list of posible words.  Try again...")
        return findword
    
    def select_compute_letter(letterused:str,position:int=0) -> str:
        """
        Funcion dedicada a mejorar la eleccion final de la computadora.
        
        Parameters
        ----------
        letterused : str, optional
            Almacena las letras arriesgadas por la compuadora.
        position : int, optional
            Se utiliza para seleccionar la letra con mayor porcentaje de presencia en la lista.

        Returns
        -------
        str
            la letra seleccionada por la computadora, la cual tiene mas chances de estar en la palabra que busca.

        """
        compute_letter=(probabilities(words_list))[0][1]
        #La letra a ingrear por la maquina es aquella que mas ocurrencia tiene.
        while compute_letter in letterused:
        #Evitamos que arriesgue una misma letra.
            position+=1
            compute_letter=(probabilities(words_list))[position][1]
        position=0 
        return compute_letter
    
    def replace_listshowword(listshowword:list,findword:str,compute_letter:str,question:str) -> list:
        """
        Funcion dedicada a reemplazar los guiones por las letras letras acertadas por la computadora en su posición correspondiente.
        
        Parameters
        ----------
        listshowword : list, optional
            Contiene la palabra secreta pero no completa, a medida que la computadora arriesga letras, se va rellenando.
        findword : str
            Palabra oculta.
        compute_letter : str, optional
            Almacena las letras que la computadora prueba para tratar de adivinar la palabra.
        question : str
            Contiene la respuesta ingresada por el usuario.

        Returns
        -------
        list
            lista actualizada que se mostrara en pantalla luego de ser transformada a str.

        """
        for i in range(len(listshowword)):
            #Reemplazamos en la palabra oculta, las letras arriesgadas acertadas.
            if findword[i]==compute_letter and question=="y":
                listshowword[i]=compute_letter
            else:
                continue
        return listshowword
   
    def select_random_final_word(words_list:list,letterused:str,findword:str) -> str:
        """
        En esta funcion evitamos que la palabra random que escojera la maquina no tenga ninguna letra de las que ya habiamos descartado.
        
        Parameters
        ----------
        words_list : list
            Lista con las palabras posibles.
        letterused : str
            lestras que se han usado durante el desarrollo del juego.
        findword : str
            Palabra oculta.

        Returns
        -------
        str.
            La palabra arriesgada por la maquina.

        """
        final_desicion = random.choice(words_list)
        
        while True:
            for i in final_desicion:
                if i in letterused and i not in findword:
                    final_desicion = random.choice(words_list)
                    break
            if i==final_desicion[len(final_desicion)-1]:
                break
        return final_desicion

    findword=findword() 
    words_list = sizeword(findword)
    listshowword=list_showword(findword)
    
    while triesremaning>0:
        #El juego se va a desarrollar hasta que se gasten los 5 intentos
        newlist=[]
        showword=print_console(listshowword, letterused)[1]
        
        if len(words_list)==1:
            #Si la lista de palabras tiene un solo elemento, esta palabra es la secreta.
            print("\nIs the word" ,words_list[0],"?")
            end=yes_or_no()
            
            if lies_detector(letterused,findword,showword)[1]:
                #Evitamos que el usuario tenga la libertad de responder cualquier cosa, las repuestas no admiten engaño.
                return lies_detector(letterused,findword,showword)[0]
            
        if end=="n":
            return "\nAssume your defeat, the word you chose was" + words_list[0]
        elif end=="y":
            return "\nThe computer guessed right, the word you chose was "+ words_list[0]     
            
        print(print_console(listshowword, letterused)[0])
        
        print("\n",triesremaning,"tries remaning.\n")
        
        compute_letter=select_compute_letter(letterused)
        
        if triesremaning>1 or compute_letter in findword:
            print("Is the letter",compute_letter,"present in the word?")
            question = yes_or_no()
            
        listshowword=replace_listshowword(listshowword, findword, compute_letter,question)
            
        letterused+=compute_letter
        
        if compute_letter not in findword and question=="y":
            print("\n---Answer correctly,",compute_letter,"is not in the secret word---")
        
        if compute_letter in findword and question == "n":
            print("\n---Answer correctly,",compute_letter,"is in the secret word---")
        #Ambas avisan de la presencia de un angaño
        
        if compute_letter in findword and question=="y":
            #Si la letra arriesgada es correcta, procederemos a descartar aquellas palabras que no la contengan y en el espacio correspondiente.
            for word in words_list:
                for letter in range(len(findword)):
                    if word[letter]==compute_letter==findword[letter]:
                        continue
                    elif word[letter]!=compute_letter and compute_letter!=findword[letter]:
                        continue
                    else:
                        break
                if letter==len(findword)-1 and  findword.count(compute_letter) == word.count(compute_letter):
                    newlist.append(word)
            words_list=newlist.copy()  
            
        else:
            if triesremaning == 1 and len(words_list) > 1:
                #Si queda un intento, la maquina arriesgara una palabra de las que quedan en la lista de palabras posibles.
                final_desicion=select_random_final_word(words_list,letterused,findword)
                print("\nIs the word" ,final_desicion,"?")
                end=yes_or_no()
                if end=="y" and final_desicion==findword:
                    if lies_detector(letterused,findword,showword)[1]:
                        return lies_detector(letterused,findword,showword)[0]
                    return "\nThe computer guessed right, the word you chose was " + final_desicion
                elif end=="y" and final_desicion!=findword:
                    return "\n-------WARNING-------\nRespond appropriately to the machine so that it responds accordingly, do not deceive it"
                    
            triesremaning-=1
          
    if lies_detector(letterused,findword,showword)[1]:
                #Evitamos que el usuario tenga la libertad de responder de manera incorrecta, las repuestas no admiten engaño.
        return lies_detector(letterused,findword,showword)[0]
     
    return "\nYou won, the computer did not guess the selected word correctly " + findword 


def play(Play:bool):
    """
    Funcion dedicada a presentar los diferentes modos de juego del Hangman.
    
    Parameters
    ----------
    Play : bool
        Es la funcion que almacena todos los modos de juego del programa.

    Raises
    ------
    ValueError
        Se utiliza para evitar errores a la hora de ingresar caracteres por medio de los inputs.

    Returns
    -------
    None.

    """
    while Play:
        print("\nHow do you want to play?\n1. Human hangman \n2. Computer hangman \n3. Go back")
        while True:
            try:
               choose_mode=int(input("Select at most one option > "))
               if choose_mode !=1 and choose_mode !=2 and choose_mode !=3 :
                   raise ValueError
               break
            except ValueError:
                print("Oops!  This instance doesn´t take letters or numbers outside 1,2 or 3. Try again...")
        if choose_mode==1:
            print("\n----------------------------\nHUMAN HANGMAN")
            print(human_hangman())
        elif choose_mode==2:
            print("\n----------------------------\nCOMPUTER HANGMAN")
            print(computer_hangman())
        else:
            Play=False
          
def wordlist(words:tuple) -> str:
    """
    Funcion dedicada a mostrar en pantalla la lista de palabras utilizada en el programa.
    
    Parameters
    ----------
    words : tuple
        Almacena las palabras que se pueden utilizar para este programa.

    Returns
    -------
    str
        Printea la lista de palabras en la consola al ser solicitada por el usuario.
    """
    palabras=(str(words)).replace("(","").replace(")","").replace("'","")
    return "\n\n----LIST OF WORDS----\n\n" + palabras

def main():
    """
    Esta funcion se ejecutara siempre, en ella se encuentran los menus principales.

    Raises
    ------
    ValueError
        Se utiliza para evitar errores a la hora de ingresar caracteres por medio de los inputs.
    """
    jugar=True
    while jugar:
        print("\n\nLet's play hangman! \nWhat do you want to do?\n1. Play \n2. See words list \n3. Quit")
        while True:
            try:
               principal_menu=int(input("Select at most one option > "))
               if principal_menu !=1 and principal_menu !=2 and principal_menu !=3 :
                   raise ValueError
               break
            except ValueError:
                print("Oops!  This instance doesn´t take letters or numbers outside 1,2 or 3.  Try again...")
        if principal_menu==1:
            print("\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            play(True)
        elif principal_menu==2:
            print(wordlist(words))
        else: 
            jugar=False
    
if __name__=='__main__':
    main()

