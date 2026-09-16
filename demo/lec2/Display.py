"""
-----------------------------------------------------------
Introduction to artificial intelligence - Course's Examples
-----------------------------------------------------------
@ Victor Mangeleer - S181670

---------------
Documentation :
---------------
Ensemble de fonctions utilisées pour afficher des informations sur le terminal

"""

def display(message):
    """
    Documentation
    _____________
    
    Affiche sur le terminal un message

    Keywords
    ________

    - 'message' : le message à afficher

    """

    print(message + "\n")

def display_PACMANLOGO():
    print(" ")
    print(" _ __   __ _  ___ _ __ ___   __ _ _ __  ")
    print("| '_ \ / _` |/ __| '_ ` _ \ / _` | '_ \ ")
    print("| |_) | (_| | (__| | | | | | (_| | | | |")
    print("| .__/ \__,_|\___|_| |_| |_|\__,_|_| |_|")
    print("| |                                     ")
    print("|_|                                     ")
    print(" ")

def display_b(message):

    """
    Documentation
    _____________
    
    Affiche sur le terminal un message avec des bordures

    Keywords
    ________

    - 'message' : le message à afficher

    """
    
    # Longueur du message pour la bordure
    t_length = len(message)

    # Bordure du message
    bordure = ""

    for i in range(t_length):

        bordure = bordure + "-"

    # Affichage terminal
    print("")
    print(bordure)
    print(message)
    print(bordure)
