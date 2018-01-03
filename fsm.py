from transitions.extensions import GraphMachine
import time

life_level = 100
sick_level = 0
mood_level = 0
boring_level = 0
hungry_level = 0
money = 100   
name = 'Joseph'

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )  
    """initial ok"""
    def is_going_to_initial(self, update):
        text = update.message.text                        
        return text.lower() == 'initial'

    def on_enter_initial(self, update):        
        update.message.reply_text("Initial and 'Intro'")
        global life_level, sick_level, mood_level, boring_level, hungry_level, money        
        life_level = 100
        sick_level = 0
        mood_level = 0
        boring_level = 0
        hungry_level = 0
        money = 100           

    def on_exit_initial(self, update):
        print('exit initial')

    """name ok"""
    def is_going_to_name(self, update):
        text = update.message.text                        
        return text.lower() == 'intro'

    def on_enter_name(self, update):        
        update.message.reply_text('Hi! My name is ' + name) 
        self.is_going_to_normal(update)       

    def on_exit_name(self, update):
        update.message.reply_text('Hungry Level : ' +str(hungry_level)
                                + '\nSick Level : ' +str(sick_level)
                                + '\nMood Level : ' +str(mood_level)
                                + '\nBoring Level : ' +str(boring_level)
                                + '\nMoney : '+str(money))
        print('exit name')

    """normal"""
    def is_going_to_normal(self, update):               
        print('go to normal')

    def on_enter_normal(self, update):
        print('normal') 
        global life_level, sick_level, mood_level, boring_level, hungry_level, money
        counter = 0      
        update.message.reply_text(' Life Level : ' + str(life_level))
        while(counter<5):            
            time.sleep(5)

            money = money + 30
            sick_level = sick_level + 3
            mood_level = mood_level + 4
            boring_level = boring_level + 5
            hungry_level = hungry_level + 8                                 

            if(sick_level>80 or mood_level>80):
                self.is_going_to_sick(update)
                break 

            if(hungry_level>70):               
                self.is_going_to_hungry(update)
                break

            if(mood_level>50 or boring_level>50):
                self.is_going_to_angry(update)
                break            

            if(boring_level>20):               
                self.is_going_to_boring(update)
                break                        

            if(life_level<90):
                life_level = life_level + 10
            
            counter = counter+1
        
        if(counter == 5):
            self.is_going_to_check(update)
                            

    def on_exit_normal(self, update):
        print('exit normal')
    
    
    """check ok"""
    def is_going_to_check(self, update):
        print('go to check')

    def on_enter_check(self, update):        
        update.message.reply_text('Name : ' + name
                                + '\nLife Level : ' +str(life_level)
                                + '\nHungry Level : ' +str(hungry_level)
                                + '\nSick Level : ' +str(sick_level)
                                + '\nMood Level : ' +str(mood_level)
                                + '\nBoring Level : ' +str(boring_level)
                                + '\nMoney : '+str(money))
        self.is_going_to_normal(update)

    def on_exit_check(self, update):
        print('exit check')

    """hungry"""
    def is_going_to_hungry(self, update):        
        print('go to hungry')

    def on_enter_hungry(self, update):               
        update.message.reply_text("I'm hungry.\n\noption[H1] -30 $20\noption[H2] -10 $10\nHungry Level : "+str(hungry_level)+"\nMoney : " + str(money)+'\n\nor do nothing')      
        global life_level
        life_level = life_level - 10
        if(life_level<0):
            self.is_going_to_dead(dead)
    
    def on_exit_hungry(self, update):       
        print('exit hungry')

    """hungry option1"""
    def is_going_to_hungry_option1(self, update):
        text = update.message.text        
        return text.lower() == 'h1'

    def on_enter_hungry_option1(self, update):               
        update.message.reply_text('option[H1] -30 $20') 
        global hungry_level, money
        hungry_level = hungry_level -30
        money = money-20       
        self.is_going_to_normal(update)       

    def on_exit_hungry_option1(self, update): 
        update.message.reply_text('Fed')      
        print('exit hungry option1')
        
    """hungry option2"""
    def is_going_to_hungry_option2(self, update):
        text = update.message.text        
        return text.lower() == 'h2'

    def on_enter_hungry_option2(self, update):               
        update.message.reply_text('option[H2] -10 $10')
        global hungry_level, money
        hungry_level = hungry_level -10
        money = money-10        
        self.is_going_to_normal(update)

    def on_exit_hungry_option2(self, update):
        update.message.reply_text('Fed')       
        print('exit hungry option2')  
        

    """sick"""
    def is_going_to_sick(self, update):
        print('go to sick')

    def on_enter_sick(self, update):        
        update.message.reply_text("I'm sick.\n\noption[S1] -50 $30\noption[S2] -80 $60\nSick Level : "+str(sick_level)+"\nMoney : " + str(money)+'\n\nor do nothing')        
        global life_level
        life_level = life_level - 20
        if(life_level<0):
            self.is_going_to_dead(update)
    
    def on_exit_sick(self, update):
        print('exit sick')

    """sick option1"""
    def is_going_to_sick_option1(self, update):
        text = update.message.text        
        return text.lower() == 's1'

    def on_enter_sick_option1(self, update):        
        update.message.reply_text("option[S1] -50 $30") 
        global sick_level, money
        sick_level = sick_level -50
        money = money-30
        self.is_going_to_normal(update)        

    def on_exit_sick_option1(self, update):
        update.message.reply_text('Cured')
        print('exit sick option1')

    """sick option2"""
    def is_going_to_sick_option2(self, update):
        text = update.message.text        
        return text.lower() == 's2'

    def on_enter_sick_option2(self, update):        
        update.message.reply_text("option[S2] -80 $60") 
        global sick_level, money
        sick_level = sick_level -80
        money = money-60
        self.is_going_to_normal(update)        

    def on_exit_sick_option2(self, update):
        update.message.reply_text('Cured')
        print('exit sick option2')

    """boring"""
    def is_going_to_boring(self, update):
        print('go to boring')

    def on_enter_boring(self, update):        
        update.message.reply_text("I'm boring.\n\noption[B1] -30 $20\noption[B2] -20 $15\noption[B3] -10 $10\nBoring Level : "+str(boring_level)+"\nMoney : " + str(money)+'\n\nor do nothing')       
        global life_level
        life_level = life_level - 2        

    def on_exit_boring(self, update):        
        print('exit boring')

    """boring option1"""
    def is_going_to_boring_option1(self, update):
        text = update.message.text        
        return text.lower() == 'b1'

    def on_enter_boring_option1(self, update):        
        update.message.reply_text("option[B1] -30 $20")  
        global boring_level, money
        boring_level = boring_level -30
        money = money-20      
        self.is_going_to_normal(update)

    def on_exit_boring_option1(self, update):
        update.message.reply_text("Got somthing to do")        
        print('exit boring option1')

    """boring option2"""
    def is_going_to_boring_option2(self, update):
        text = update.message.text        
        return text.lower() == 'b2'

    def on_enter_boring_option2(self, update):        
        update.message.reply_text("option[B2] -20 $15") 
        global boring_level, money
        boring_level = boring_level -20
        money = money-15     
        self.is_going_to_normal(update)

    def on_exit_boring_option2(self, update): 
        update.message.reply_text("Got somthing to do.")       
        print('exit boring option2')

    """boring option3"""
    def is_going_to_boring_option3(self, update):
        text = update.message.text        
        return text.lower() == 'b3'

    def on_enter_boring_option3(self, update):        
        update.message.reply_text("option[B3] -10 $10")
        global boring_level, money
        boring_level = boring_level -10
        money = money-10        
        self.is_going_to_normal(update)

    def on_exit_boring_option3(self, update):
        update.message.reply_text("Got somthing to do.")        
        print('exit boring option3')

    """angry"""
    def is_going_to_angry(self, update):
        print('go to angry')

    def on_enter_angry(self, update):         
        update.message.reply_text("I'm angry.\n\noption[A1] -30 $40\noption[A2] -20 $20\noption[A3] -10 $10\nMood Level : "+str(mood_level)+"\nMoney : " + str(money)+'\n\nor do nothing')        
        global life_level
        life_level = life_level - 2        

    def on_exit_angry(self, update):
        print('exit angry')

    """angry option1"""
    def is_going_to_angry_option1(self, update):
        text = update.message.text        
        return text.lower() == 'a1'

    def on_enter_angry_option1(self, update):         
        update.message.reply_text("option[A1] -30 $40")
        global mood_level, money
        mood_level = mood_level -30
        money = money-40        
        self.is_going_to_normal(update)

    def on_exit_angry_option1(self, update):
        update.message.reply_text("I'm good.")
        print('exit angry option1')

    """angry option2"""
    def is_going_to_angry_option2(self, update):
        text = update.message.text        
        return text.lower() == 'a2'

    def on_enter_angry_option2(self, update):         
        update.message.reply_text("option[A2] -20 $20") 
        global mood_level, money
        mood_level = mood_level -20
        money = money-20       
        self.is_going_to_normal(update)

    def on_exit_angry_option2(self, update):
        update.message.reply_text("I'm good.")
        print('exit angry option2')

    """angry option3"""
    def is_going_to_angry_option3(self, update):
        text = update.message.text        
        return text.lower() == 'a3'

    def on_enter_angry_option3(self, update):         
        update.message.reply_text("option[A3] -10 $10")
        global angry_level, money
        mood_level = mood_level -10
        money = money-10        
        self.is_going_to_normal(update)

    def on_exit_angry_option3(self, update):
        update.message.reply_text("I'm good.")
        print('exit angry option3')

    """dead"""
    def is_going_to_dead(self, update):
        print("dead")

    def on_enter_dead(self, update):        
        update.message.reply_text("I'm dead. Wait for 1 minutes and initialize 'initial'.")
        time.sleep(60)

    def on_exit_dead(self, update):
        update.message.reply_text('You can start again.')
        print('Initial')

    def do_nothing(self, update):
        text = update.message.text        
        return text.lower() == 'do nothing'

    def kill_this(self, update):
        text = update.message.text        
        return text.lower() == 'kill'
