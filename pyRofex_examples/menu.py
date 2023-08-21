import sys
import subprocess
import threading
import time


class Menu:
    ''' Displays a list of choices on the terminal for  the user to run '''

    def __init__(self):

        self.choices = {
            "1": "1_reference_data.py",
            "2": "2_market_data.py",
            "3": "3_order_routing.py",
            "4": "4_websocket_market_data.py",
            "5": "5_websocket_order_report.py",
            "6": "6_MM_Strategy_practico.py",
            "7": "7_Price_Visualization.py",
            "8": self.quit}

    def display_menu(self):
        print(""" 
            Scripts Menu  

            1: 1_reference_data.py
            2: 2_market_data.py
            3: 3_order_routing.py
            4: 4_websocket_market_data.py
            5: 5_websocket_order_report.py
            6: 6_MM_Strategy_practico.py
            7: 7_Price_Visualization.py
            8: quit
             """)

    def run(self):
        ''' Display menu and respond to user choices '''

        while True:

            self.display_menu()
            choice = input("Enter an option: ")
            script = self.choices.get(choice)

            if isinstance(script, str):
                #t=threading.Thread(target=subprocess.run,args=(["C:/Users/jljuncos/PycharmProjects/Algo_Trading/venv/Scripts/python",script],))
                #t.start()
                subprocess.check_call(["python", script])
                #proc.communicate(timeout=15))
            elif hasattr(script,'__call__'):
                script()
            else:
                print("{0} is not a valid choice".format(choice))

    def quit(self):
        ''' quit or terminate the program '''
        print("Thank you for using")
        sys.exit(0)


if __name__ == "__main__":
    Menu().run()
