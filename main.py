
import random
from gtts import gTTS
import time
from datetime import datetime
import os
import pyttsx3
from openpyxl import load_workbook
from datetime import datetime
import sqlite3
import threading
import speech_recognition as sr
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.properties import NumericProperty

performance = 0

#sqlite data base is not connecting

    



class MultiDonutChart(Widget):

    accuracy = NumericProperty(0)
    confidence = NumericProperty(0)
    communication = NumericProperty(0)
    

    def on_size(self,*args):
        self.draw_chart()

    def on_accuracy(self,*args):
        self.draw_chart()

    def on_confidence(self,*args):
        self.draw_chart()

    def on_communication(self,*args):
        self.draw_chart()

    def draw_chart(self):

        self.canvas.clear()

        cx = self.center_x
        cy = self.center_y
        base = min(self.width,self.height)/2

        with self.canvas:

            Color(0.2,0.6,1,1)
            Line(circle=(cx,cy,base,0,360*(self.accuracy/100)),
                 width=15,
                 cap="round")

            Color(0.3,0.8,0.4,1)
            Line(circle=(cx,cy,base-20,0,360*(self.confidence/100)),
                 width=15,
                 cap="round")

            Color(1,0.6,0.2,1)
            Line(circle=(cx,cy,base-40,0,360*(self.communication/100)),
                 width=15,
                 cap="round")


class InterviewApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.stop_listening_fn = None  # Holds the background function
        
        
    
        
        
        
        self.ans = {
        "python" : {
            "python" : ["programming language","high level","interpreted","object", "oriented"],
            "var" : ["variables", "building"," block" ,"programming" , "store"],
            "data_types" : ["int","float","string","list","tuple","dictionary","set"],
            "oop" : ["class","object","inheritance","encapsulation","polymorphism","abstraction"],
            "var_type" : ["snake" ,"case"],
            "dictnories" : ["key","value","mapping","lookup"],
            "function" : ["def","function","parameters","return","reusable"],
            "loop" : ["for","while","loop","iteration","repetition"],
            "exception" : ["try","except","finally","error","exception"],
            "module" : ["module","import","file","library","functions"],
            "list_comp" : ["list","comprehension","expression","for","brackets"]
            }
        }


        self.que = {
        "python":[
            "what is python.",
            "Role Variables in python.",
            "What are datatypes in python and give me it's types",
            "What do you know about OOP in python ?",
            "when we use _ (underscore) in var name in python then this underscore or this variable called as.",
            "Dictnories in python ?",
            "What is function and how we use it ?",
            "looping in python ?",
            "what about Exception handling and where it is used ?",
            "Importance and use Module in py",
            "list comprehension means ?"
        ]
        }
        
        self.program = {
            "loop" : r"C:\Users\Vaishnavi\OneDrive\Desktop\Tanmay\project_2\images\loop_que.png",#image path
            "reverse" : r"C:\Users\Vaishnavi\OneDrive\Desktop\Tanmay\project_2\images\reverse.png",
            "conconent" : r"C:\Users\Vaishnavi\OneDrive\Desktop\Tanmay\project_2\images\conconent.png",
            "print_it" : r"C:\Users\Vaishnavi\OneDrive\Desktop\Tanmay\project_2\images\print.png",
            "loop_2" : r"C:\Users\Vaishnavi\OneDrive\Desktop\Tanmay\project_2\images\loop2.png",
            "rev_loop": r"C:\Users\Vaishnavi\OneDrive\Desktop\Tanmay\project_2\images\rev_loop.png"
        }
        
        

        self.conn = sqlite3.connect("interview_results.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            average_score REAL
            )
            """)

        self.conn.commit()
    def store(self , name , avg_score):
    

        date = datetime.now().strftime("%d-%m-%Y")

        self.cursor.execute(
        "INSERT INTO results (name, date, average_score) VALUES (?, ?, ?)",
        (name, date, avg_score)
        )

        self.conn.commit()
        self.conn.close()
        
    def build(self):
        screen = Builder.load_file("frontend.kv")
        self.chart = screen.ids.chart
        return screen

    def toggle_mic(self):
        if not self.is_listening:
            # START LISTENING
            self.is_listening = True
            self.root.ids.mic_btn.icon = "microphone-off" # Change icon to 'Stop'
            self.root.ids.status_label.text = "Recording... Click again to stop."
            
            # Start background listening
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            
            # This starts a background thread that stays active
            self.stop_listening_fn = self.recognizer.listen_in_background(
                self.microphone, self.callback
            )
        else:
            # STOP LISTENING
            self.is_listening = False
            self.root.ids.mic_btn.icon = "microphone"
            self.root.ids.status_label.text = "Processing your answer..."
            
            if self.stop_listening_fn:
                self.stop_listening_fn(wait_for_stop=False) # Tell the background thread to stop

    def callback(self, recognizer, audio):
        # This function runs automatically once the audio is captured
        try:
            # Use Google to recognize speech
            result = recognizer.recognize_google(audio)
            # Use Clock to update UI from a background thread safely
            Clock.schedule_once(lambda dt: self.update_ui(result))
        except Exception:
            Clock.schedule_once(lambda dt: self.update_ui("Could not understand audio."))

    def update_ui(self, text):
        self.root.ids.answer_field.text = text
        self.root.ids.status_label.text = "Answer Saved!"



    #change
    
    def speak_en(self , words):
        pass
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(words)
        engine.runAndWait()
    # tts = gTTS(text=words , lang = "en")
    # tts.save("speak.mp3")
    


    def check_ans(self , usr_ans , ans , suggest):
        correct_count = 0
        usr_ans_list = []

        space_ind = 0
        for i in range(0 , len(usr_ans)):
            if(usr_ans[i] == " "):
                usr_ans_list.append(usr_ans[space_ind:i])
                space_ind = i
            elif(i == len(usr_ans)-1):
                usr_ans_list.append(usr_ans[space_ind+1:i+1])
                
        for j in range(0,len(ans)):
            if(ans[j] in usr_ans):
                correct_count += 1
                
            else:
                suggest.append(ans[j])
                
        return ((correct_count/len(ans))*100)
    
    
    def nav_home(self):
        self.root.transition.direction = "right"
        
    def nav_dash(self):
        self.root.transition.direction = "left"
    
    
    def store_result_xl(self,date,result):
        
        # make this file for saving result.
        
        with open("results.txt" , "r") as f1:
            num = f1.readline()
        
        wb = load_workbook("result.xlsx")
        
        sheet = wb.active
        
        sheet[f"A3"] = str(date)
        sheet[f"B3"] = str(result)
        
        with open("results.txt","w") as f2:
            f2.write(str(int(num)+1))
    
    def store_result_txt(self , date , score):
        self.date = date
        with open("result.txt" , "a") as f3:
            f3.write(f"{self.date} : {score}\n")
            
    def graph(self):
        
        self.day = []
        self.today_scores = []
        self.today_avg_score = 0
        self.bar1 = self.root.ids.bar1
        self.bar2 = self.root.ids.bar2
        self.bar3 = self.root.ids.bar3
        self.bar4 = self.root.ids.bar4
        self.bar5 = self.root.ids.bar5
        self.bar6 = self.root.ids.bar6
        self.bar7 = self.root.ids.bar7
        
        
        self.date1 = self.root.ids.date1
        self.date2 = self.root.ids.date2
        self.date3 = self.root.ids.date3
        self.date4 = self.root.ids.date4
        self.date5 = self.root.ids.date5
        self.date6 = self.root.ids.date6
        self.date7 = self.root.ids.date7
        self.all_dates = []
        days_order = {
            "Mon": 1,
            "Tue": 2,
            "Wed": 3,
            "Thu": 4,
            "Fri": 5,
            "Sat": 6,
            "Sun": 7
            }
        
        now = datetime.now()
        self.formatted_d = now.strftime("%d-%m-%y")
        
        with open("result.txt" , "r") as f5:
            lines = f5.readlines()
        
        for i in range(0,len(lines)):
            self.day.append(int(lines[i][:2]))
            
        for i in range(0,len(self.day)) :
            if(self.day[i] == self.day[len(self.day)-1]):   
                self.today_scores.append(float(lines[i][11:len(lines[i])-1]))
                
        for i in range(0 , len(self.today_scores)):
            self.today_avg_score += self.today_scores[i]
            
        
        
        self.final_value = self.today_avg_score/len(self.today_scores)     
        with open("day_avg_scores.txt","a") as score:
            score.write(f"{self.formatted_d} : {round(self.final_value , 1)}\n")
            
        with open("day_avg_scores.txt" , "r") as fd :
            dates = fd.readlines()
            
        for i in range(0 , len(dates)):
            self.all_dates.append(dates[i][:8])
            
            
        for line in dates:

            date = line[:8]
            score = float(line[11:].strip())

            day = self.date_to_day(date)

            if (days_order[day] <= days_order[self.date_to_day(self.formatted_d)]) :

                if day == "Mon":
                    self.bar1.size_hint_y = 0.9 * (score / 100)
                    self.date1.text = date[:2]

                elif day == "Tue":
                    self.bar2.size_hint_y = 0.9 * (score / 100)
                    self.date2.text = date[:2]

                elif day == "Wed":
                    self.bar3.size_hint_y = 0.9 * (score / 100)
                    self.date3.text = date[:2]

                elif day == "Thu":
                    self.bar4.size_hint_y = 0.9 * (score / 100)
                    self.date4.text = date[:2]

                elif day == "Fri":
                    self.bar5.size_hint_y = 0.9 * (score / 100)
                    self.date5.text = date[:2]

                elif day == "Sat":
                    self.bar6.size_hint_y = 0.9 * (score / 100)
                    self.date6.text = date[:2]

                elif day == "Sun":
                    self.bar7.size_hint_y = 0.9 * (score / 100)
                    self.date7.text = date[:2]

        
        
        
                
            
                
        
    def date_to_day(self , date):
        date_str = str(date) # YYYY-MM-DD format
        date_obj = datetime.strptime(date_str, "%d-%m-%y")

          # Full day name
        day_short = date_obj.strftime("%a")  # Short name 
        return day_short 
    # continue from this
    
    def end(self , instance):
        pass

    def correct_op(self , instance):
        if(self.correct == 1):
            self.option1.md_bg_color = (0.25, 0.70, 0.45, 1)
            self.p_score +=1
            self.option1.bind(on_release = self.end)
            self.next_btn.bind(on_release = self.next_que)
            
        elif(self.correct== 2):
            self.option2.md_bg_color = (0.25, 0.70, 0.45, 1)
            self.p_score +=1
            self.option2.bind(on_release = self.end)
            self.next_btn.bind(on_release = self.next_que)
            
        elif(self.correct == 3):
            self.option3.md_bg_color = (0.25, 0.70, 0.45, 1)
            self.p_score +=1
            self.option3.bind(on_release = self.end)
            self.next_btn.bind(on_release = self.next_que)
            
        elif(self.correct == 4):
            self.option4.md_bg_color = (0.25, 0.70, 0.45, 1)
            self.p_score +=1
            self.option4.bind(on_release = self.end)
            self.next_btn.bind(on_release = self.next_que)
            
    def wrong_op(self , instance):
        if(self.correct == 1):
            self.next_btn.bind(on_release = self.next_que)
            self.option1.md_bg_color = (0.25, 0.70, 0.45, 1)
            self.option2.line_color = (1, 0, 0, 1)
            self.option3.line_color = (1, 0, 0, 1)
            self.option4.line_color = (1, 0, 0, 1)
            
            

            
        elif(self.correct== 2):
            self.next_btn.bind(on_release = self.next_que)
            self.option2.md_bg_color = (0.25, 0.70, 0.45, 1)
            self.option3.line_color = (1, 0, 0, 1)
            self.option4.line_color = (1, 0, 0, 1)
            self.option1.line_color = (1, 0, 0, 1)
            
            
            
            
        elif(self.correct == 3):
            self.next_btn.bind(on_release = self.next_que)
            self.option3.md_bg_color = (0.25, 0.70, 0.45, 1)
            self.option4.line_color = (1, 0, 0, 1)
            self.option1.line_color = (1, 0, 0, 1)
            self.option2.line_color = (1, 0, 0, 1)
            
            
            
            
        elif(self.correct == 4):
            self.next_btn.bind(on_release = self.next_que)
            self.option4.md_bg_color = (0.25, 0.70, 0.45, 1)
            self.option1.line_color = (1, 0, 0, 1)
            self.option2.line_color = (1, 0, 0, 1)
            self.option3.line_color = (1, 0, 0, 1)
            
            
    
    
    def basic_avg(self,score):
        
        avg = 0
        for item in score:
            avg += item

        avg_performance = round(avg/len(score),1)
        
        print(f"\nYour overall performance is {avg_performance}%.")
        
        return avg_performance
    
    def p_avg(self , p_score):
        return (p_score/5)*100
    
    def next_que(self ,instance):
        self.program_questions()
        
    def result_display(self , instance):
        self.root.current = "ScoreScreen"
        self.basic_per = self.root.ids.basic_per
        self.program_per = self.root.ids.program_per
        self.hr_per = self.root.ids.hr_per
        self.root.transition.direction = "left"
        
        self.average_score = (self.basic_avg(self.score) + ((self.p_score/4)*100))/2
        
        self.basic_per.text = f"{self.basic_avg(self.score)}%"
        self.program_per.text = f"{(self.p_score/4)*100}%"
        self.hr_per.text = f"{self.average_score}%"
        
        #donut chart is not appearing
        Animation(accuracy=self.basic_avg(self.score),duration=2,t='out_quad').start(self.chart)
        Animation(confidence=(self.p_score/4)*100,duration=2,t='out_quad').start(self.chart)
        Animation(communication=self.average_score,duration=2,t='out_quad').start(self.chart)
        
        now = datetime.now()
        self.formatted_d = now.strftime("%d-%m-%y")
        self.store_result_txt(self.formatted_d , self.average_score)
        self.graph()
        
        
    
        
        
    def program_questions(self):
        program_list = []
        self.next_btn = self.root.ids.next
        self.option1 = self.root.ids.option1
        self.option2 = self.root.ids.option2
        self.option3 = self.root.ids.option3
        self.option4 = self.root.ids.option4
        self.question = self.root.ids.question_img
        self.statement = self.root.ids.p_subscript
        self.count_no = self.root.ids.p_count
        
        self.option1.disabled = False
        self.option2.disabled = False
        self.option3.disabled = False
        self.option4.disabled = False
    
        self.option1.md_bg_color = (0.12, 0.15, 0.25, 1)
        self.option2.md_bg_color = (0.12, 0.15, 0.25, 1)
        self.option3.md_bg_color = (0.12, 0.15, 0.25, 1)
        self.option4.md_bg_color = (0.12, 0.15, 0.25, 1)
        
        self.option1.line_color = (0.23, 0.51, 0.96, 1)
        self.option2.line_color = (0.23, 0.51, 0.96, 1)
        self.option3.line_color = (0.23, 0.51, 0.96, 1)
        self.option4.line_color = (0.23, 0.51, 0.96, 1)
        
        
        
        for keys in self.program :
            program_list.append(keys)
            
        self.p_que_no = random.randrange(0 , (len(program_list)))
            
        self.question.source =  self.program[program_list[self.p_que_no]]
        
        if(self.p_count >= 3):
            self.next_btn.bind(on_release = self.result_display)
            
            self.p_count -= 1
            
        else:
            pass
        
        if (self.p_que_no == 0):
            self.correct = 4
            self.p_count += 1
            self.count_no.text = f"{self.p_count}/4"
            self.statement.text = "Which line can throw Error ?"
            self.option1.text = "Line 2"
            self.option2.text = "Line 3"
            self.option3.text = "Line 4"
            self.option4.text = "No error"
            
            
            self.option4.bind(on_release = self.correct_op)
            self.option1.bind(on_release = self.wrong_op)
            self.option2.bind(on_release = self.wrong_op)
            self.option3.bind(on_release = self.wrong_op)
            
            
        elif (self.p_que_no == 1):
            self.correct = 3
            self.p_count += 1
            
            self.count_no.text = f"{self.p_count}/4"
            self.statement.text = "select correct output."
            self.option1.text = "[\'r\',\'a\',\'w\',\'h\',\'e\',\'s\',\'p\',\'l\',\'a\',\'k\']"
            self.option2.text = "[\'k\',\'a\',\'l\',\'p\',\'e\',\'s\',\'h\',\'w\',\'a\',\'r\']"
            self.option3.text = "[\'r\',\'a\',\'w\',\'h\',\'s\',\'e\',\'p\',\'l\',\'a\',\'k\']"
            self.option4.text = "[\'r\',\'e\',\'w\',\'h\',\'s\',\'e\',\'p\',\'l\',\'a\',\'k\']"
            
            self.option4.bind(on_release = self.wrong_op)
            self.option1.bind(on_release = self.wrong_op)
            self.option2.bind(on_release = self.wrong_op)
            self.option3.bind(on_release = self.correct_op)
            
        elif (self.p_que_no == 2):
            self.correct = 2
            self.p_count += 1
            
            self.count_no.text = f"{self.p_count}/4"
            self.statement.text = "select correct output if user enter \' kalpeshwar \'."
            self.option1.text = "3"
            self.option2.text = "7"
            self.option3.text = "5"
            self.option4.text = "6"
            
            self.option4.bind(on_release = self.wrong_op)
            self.option1.bind(on_release = self.wrong_op)
            self.option2.bind(on_release = self.correct_op)
            self.option3.bind(on_release = self.wrong_op)
            
        elif (self.p_que_no == 3):
            self.correct = 2
            self.p_count += 1
            
            self.count_no.text = f"{self.p_count}/4"
            self.statement.text = "select correct expression, which will write in print() to get output as 11"
            self.option1.text = "dict[\"list\"][0][\"prime\"][3]"
            self.option2.text = "dict[\"list\"][1][\"prime\"][3]"
            self.option3.text = "dict[\"prime\"][1][\"list\"][3]"
            self.option4.text = "dict[\"list\"][\"prime\"][3]"
            
            self.option4.bind(on_release = self.wrong_op)
            self.option1.bind(on_release = self.wrong_op)
            self.option2.bind(on_release = self.correct_op)
            self.option3.bind(on_release = self.wrong_op)
            
        elif (self.p_que_no == 4):
            self.correct = 3
            self.p_count += 1
            
            self.count_no.text = f"{self.p_count}/4"
            self.statement.text = "What is output of this code?"
            self.option1.text = "Infinite loop"
            self.option2.text = "Infinite range error"
            self.option3.text = "No output"
            self.option4.text = "Stepping Error"
            
            self.option4.bind(on_release = self.wrong_op)
            self.option1.bind(on_release = self.wrong_op)
            self.option2.bind(on_release = self.wrong_op)
            self.option3.bind(on_release = self.correct_op)    
            
        elif (self.p_que_no == 5):
            self.correct = 1
            self.p_count += 1
            self.statement.text = " 5\n5 4\n5 4 3\n5 4 3 2\n This is output of code , select correct parameters for inner loop"
            self.count_no.text = f"{self.p_count}/4"
            self.option1.text = "5 , i+1 , -1"
            self.option2.text = "i+1 , 5 , 1"
            self.option3.text = "0 , i , -1"
            self.option4.text = "i , 0 , 1 "
            
            self.option1.bind(on_release = self.correct_op)
            self.option2.bind(on_release = self.wrong_op)
            self.option3.bind(on_release = self.wrong_op)
            self.option4.bind(on_release = self.wrong_op)   
            
         
                 
    
    def switch_screen(self , instance):
        self.root.current = "programScreen"
        self.program_questions()
        
        
        #Basic Questions
    
    def python_basic_que(self):
        
        
        ans_keys = []
        for keys in self.ans["python"]:
            ans_keys.append(keys)
            
        

        
        
        self.root.ids.count.text = f"{self.que_count}/3"
        self.label = self.root.ids.question
        self.label.text = f"{self.que_count}. {self.que["python"][self.rand_select]}"

        


            # rand_select = random.randrange(0 , len(que["python"])-1)

            # print(f"{que["python"][rand_select]}")
            
            # #ask question
            # self.design.ids.question = f"{que_count}. {que["python"][rand_select]}"
            
            
        usr_ans = self.root.ids.answer_field.text


        suggest = []
        correct_ans_py = self.ans["python"][ans_keys[self.rand_select]]

        check = self.check_ans(usr_ans , correct_ans_py , suggest)
        performance = round( check, 0)

        if(performance >= 50 and performance < 70):
            self.root.ids.subscript.text = f"\nThat's nice it is good. \nI think it is {performance}% correct. You can improve it by adding points on {suggest}\n"
            # self.speak_en(f"\nThat's nice it is good. \nI think it is {performance}% correct. You can improve it by adding points like {suggest}")
            print(f"\nThat's nice it is good. \nI think it is {performance}% correct. You can improve it by adding points like {suggest}\n")
                
            self.score.append(performance)
            self.que_count += 1
                
        elif(performance >= 70 and performance < 80):
            self.root.ids.subscript.text = f"\nExcellent answer. You are so good. \nI think it is {performance}% correct. You can improve it by adding points on {suggest} to make it more perfect.\n"
            # self.speak_en(f"\nExcellent answer. You are so good. \nI think it is {performance}% correct. You can improve it by adding points like {suggest}")
            print(f"\nExcellent answer. You are so good. \nI think it is {performance}% correct. You can improve it by adding points like {suggest} to make it more perfect.\n")
                
            self.score.append(performance)
            self.que_count += 1
                
        elif(performance >= 80 and performance <= 100):
            self.root.ids.subscript.text = f"\nMind blowing answer. Are you a super computer !!!!! \nI think it is {performance}% correct answer.\nIf you want to improve it then add some info about {suggest} to make it more relevant.\n"
            # self.speak_en(f"\nMind blowing answer. Are you a super computer !!!!! \nI think it is {performance}% correct answer.")
            print(f"\nMind blowing answer. Are you a super computer !!!!! \nI think it is {performance}% correct answer.")
                
            self.score.append(performance)
            self.que_count += 1
            

        elif(performance >= 20 and performance < 50):
            self.root.ids.subscript.text = f"\nIt's ok . You are so good , but you need to improve it. \nI think it is {performance}% correct. You can improve it by adding points like {suggest}\n"
            # self.speak_en(f"\nIt's ok . You are so good , but you need to improve it. \nI think it is {performance}% correct. You can improve it by adding points like {suggest}")
            print(f"\nIt's ok . You are so good , but you need to improve it. \nI think it is {performance}% correct. You can improve it by adding points like {suggest}\n")
                
            self.score.append(performance)
            self.que_count += 1
                
        elif(performance >= 1 and performance < 20):
            self.root.ids.subscript.text = "Not bad, I think you should improve you performance. \n"
            # self.speak_en("Not bad, I think you should improve you performance. ")
            print("Not bad, I think you should improve you performance. \n")
                
            self.score.append(performance)
            self.que_count += 1
                
        else:
            self.root.ids.subscript.text = "Not bad, Give me answer, or any information about that. \n"
            # self.speak_en("Give me answer, or any information about that. ")
            print("Not bad, Give me answer, or any information about that. \n")
                
            self.score.append(performance)
            self.que_count += 1
            
        
        self.rand_select = random.randrange(0 , (len(self.que["python"])))

        print(f"{self.que["python"][self.rand_select]}")
            
            #ask question
            
        self.avg_Score = self.basic_avg(self.score)
        
        if(self.que_count < 4):   
            self.root.ids.count.text = f"{self.que_count}/3"
            self.label = self.root.ids.question
            self.label.text = f"{self.que_count}. {self.que["python"][self.rand_select]}"
            
        elif(self.que_count >= 4):
            
            btn = self.root.ids.send_btn
            btn.bind(on_release = self.switch_screen)
            self.que_count -= 1
            
        
        
        
        self.root.ids.answer_field.text = ""
      
    
    def on_start(self):
        self.root.current = "practice_screen"
        self.rand_select = random.randrange(0 , (len(self.que["python"])-1))
        self.score = []
        self.que_count = 1
        self.p_count = 0
        self.p_score = 0

        print(f"{self.que["python"][self.rand_select]}")
        
        
            
            #ask question
            
        self.root.ids.subtitle.text = "Basic Level"
        self.root.ids.count.text = f"{self.que_count}/3"
        self.label = self.root.ids.question
        self.label.text = f"{self.que_count}. {self.que["python"][self.rand_select]}"
        
    
    

if(__name__ == "__main__"):
    InterviewApp().run()