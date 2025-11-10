import tkinter as tk
from tkinter import*
import pyttsx3
import time
from threading import Thread
root=tk.Tk()
root.title("AI Cook Manager")
root.geometry("800x600")
root.configure(bg="#111111")
import sqlite3
from tkinter import messagebox
import datetime
from datetime import datetime
current_datetime = datetime.now()
print(current_datetime)
import dateutil
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime

parsed_date = parse(str(current_datetime))
print(f"Parsed date: {parsed_date}")

# Calculate a relative date
future_date = datetime.now() + relativedelta(months=+1)
print(f"Date one month from now: {future_date}")
conn = sqlite3.connect('myfooddatabaseV3.db')
conn2 = sqlite3.connect('expirydatabase.db')
cursor = conn.cursor()
cursor2 = conn2.cursor()
import cv2
from inference_sdk import InferenceHTTPClient

# Connect to your workflow
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="AWkoe48gfFD2ifjLa1v7" 
    )

cursor2.execute('''
CREATE TABLE IF NOT EXISTS expiry(
    FID INT,
    purchase_date text,
    expiration_date text
)
''')

timecount = 0 
timer_active = False  
timer_thread = None  
S=[0,"Double click to proceed",0,False,0]
def countdown_timer():
    global timecount, timer_active
    timer_active = True
    timecount = 5  
    
    while timecount > 0 and timer_active:
        time.sleep(1)
        timecount -= 1
        print(f"Time remaining: {timecount} seconds") 
def reset_timer():
    global timer_active, timecount
    timer_active = False
    timecount = 0
    if timer_thread and timer_thread.is_alive():
        timer_thread.join(timeout=0.1)
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 140) 
    engine.say(text)
    engine.runAndWait()
    del engine
    
def doubleclick(a,b,c):
    global timer_thread, timecount
    S[0] = S[0] + 1
    if S[0] == 1 or S[4]!=c:
        if S[4]!=c:
            S[0],S[4]=1,c
        speak(S[2])
        speak(S[1])
        reset_timer() 
        timer_thread = Thread(target=countdown_timer)
        timer_thread.daemon = True 
        timer_thread.start()
        S[3]=False
    elif (S[0]==2 and S[4]==c )and timecount > 0: 
        speak("Succeed")
        S[3]=True
        a.pack_forget()
        b.pack()
        S[0] = 0
        reset_timer()
    else:
        S[0] = 0
        reset_timer()
        S[3]=False

def recipegen(x,y):
    if x is True:
        root = tk.Tk()
        if y is True:
            root.title("Recipe Generator")
        else:
            root.title("Ingredients saving for expiration check")
        root.geometry("800x600")

        # Main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Available ingredients section
        available_label = tk.Label(main_frame, text="Available Ingredients:")
        available_label.pack(anchor=tk.W)

        listbox = tk.Listbox(main_frame, width=50, height=10, selectmode=tk.MULTIPLE)
        listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # Get ingredients from database
        cursor.execute("SELECT name, fid FROM ingredient")
        rows = cursor.fetchall()
        ingredient_dict = {row[0]: row[1] for row in rows}  # Store name:fid mapping

        for row in rows:
            listbox.insert(tk.END, row[0])  # Use row[0] since it's the name

        # Selected ingredients section
        selected_label = tk.Label(main_frame, text="Selected Ingredients:")
        selected_label.pack(anchor=tk.W, pady=(10, 0))

        # Listbox for selected ingredients
        selected_listbox = tk.Listbox(main_frame, width=50, height=5, selectmode=tk.MULTIPLE)
        selected_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # List to store selected ingredients (as fid)
        selected_ingredient_ids = []
        selected_ingredient_names = []

        def add_ingredient():
            """Add selected ingredients to the selected ingredients list"""
            selection = listbox.curselection()
            if selection:
                for index in selection:
                    ingredient_name = listbox.get(index)
                    fid = ingredient_dict.get(ingredient_name)
                    if fid and ingredient_name not in selected_ingredient_names:
                        selected_ingredient_ids.append(fid)
                        selected_ingredient_names.append(ingredient_name)
                        selected_listbox.insert(tk.END, ingredient_name)
        
                print(f"Selected ingredient IDs: {selected_ingredient_ids}")
                print(f"Selected ingredient names: {selected_ingredient_names}")
        
                # Update button states
                update_button_states()

        def delete_selected_item():
            """Remove selected items from the selected ingredients list"""
            selection = selected_listbox.curselection()
            if selection:
                # Delete in reverse order to maintain correct indices
                for index in reversed(selection):
                    ingredient_name = selected_listbox.get(index)
                    # Remove from both lists
                    if ingredient_name in selected_ingredient_names:
                        idx = selected_ingredient_names.index(ingredient_name)
                        selected_ingredient_names.pop(idx)
                        selected_ingredient_ids.pop(idx)
                    selected_listbox.delete(index)
        
                print(f"Updated selected ingredient IDs: {selected_ingredient_ids}")
                print(f"Updated selected ingredient names: {selected_ingredient_names}")
        
                # Update button states
                update_button_states()

        def on_available_select(event):
            """Enable add button when items are selected in available list"""
            selection = listbox.curselection()
            if selection:
                add_button.config(state=tk.NORMAL)

        def on_selected_select(event):
            """Enable delete button when items are selected in selected list"""
            selection = selected_listbox.curselection()
            if selection:
                delete_button.config(state=tk.NORMAL)

        def update_button_states():
            """Update the state of buttons based on current selections"""
            # Add button - enabled if items selected in available list
            add_button.config(state=tk.NORMAL if listbox.curselection() else tk.DISABLED)
    
            # Delete button - enabled if items selected in selected list AND there are items
            delete_button.config(state=tk.NORMAL if selected_listbox.curselection() and selected_ingredient_ids else tk.DISABLED)
    
            # Submit button - enabled if there are selected ingredients
            submit_button.config(state=tk.NORMAL if selected_ingredient_ids else tk.DISABLED)

        def clear_selection():
            """Clear all selected ingredients"""
            selected_ingredient_ids.clear()
            selected_ingredient_names.clear()
            selected_listbox.delete(0, tk.END)
            update_button_states()
            print("Cleared all selected ingredients")
            
        def submit():
            """Find recipes that can be made with selected ingredients"""
            if not selected_ingredient_ids:
                messagebox.showwarning("No Ingredients", "Please select some ingredients first!")
                return
            if y is True:
                print(f"Finding recipes for ingredient IDs: {selected_ingredient_ids}")
    
                # Get all f columns from recipe table (f1, f2, f3, etc.)
                cursor.execute("PRAGMA table_info(recipe)")
                f_columns = [col[1] for col in cursor.fetchall() if col[1].startswith('f') and col[1] != 'fid']
    
                print(f"Recipe columns: {f_columns}")
    
                # Build query to find recipes that can be made with available ingredients
                # A recipe can be made if ALL its non-null required ingredients are in our selected list
                conditions = []
                query_params = []
    
                placeholders = ','.join(['?'] * len(selected_ingredient_ids))
    
                for col in f_columns:
                    conditions.append(f"({col} IS NULL OR {col} IN ({placeholders}))")
                    query_params.extend(selected_ingredient_ids)
    
                query = f"SELECT * FROM recipe WHERE {' AND '.join(conditions)}"
                print(f"Executing query: {query}")
                print(f"With parameters: {query_params}")
    
                cursor.execute(query, query_params)
                matching_recipes = cursor.fetchall()
    
                # Display results
                result_window = tk.Toplevel(root)
                result_window.title("Recipe Results")
                result_window.geometry("600x400")
    
                # Create scrollable text area
                text_frame = tk.Frame(result_window)
                text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
                scrollbar = tk.Scrollbar(text_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
                result_text = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
                result_text.pack(fill=tk.BOTH, expand=True)
                scrollbar.config(command=result_text.yview)
    
                if matching_recipes:
                    result_text.insert(tk.END, f"Found {len(matching_recipes)} recipe(s) you can make:\n\n")
                    for recipe in matching_recipes:
                        rid = recipe[0]  # First column is rid
                        recipe_name = recipe[1]  # Second column is name
                        result_text.insert(tk.END, f"Recipe: {recipe_name} (ID: {rid})\n")
                        result_text.insert(tk.END, "Ingredients used: ")
            
                        # Show which ingredients from our selection are used
                        used_ingredients = []
                        for i, col in enumerate(f_columns):
                            ingredient_fid = recipe[i+2]  # +2 because first two columns are rid and name
                            if ingredient_fid and ingredient_fid in selected_ingredient_ids:
                                # Find the ingredient name
                                cursor.execute("SELECT name FROM ingredient WHERE fid=?", (ingredient_fid,))
                                ing_row = cursor.fetchone()
                                if ing_row:
                                    used_ingredients.append(ing_row[0])
            
                        result_text.insert(tk.END, ", ".join(used_ingredients) + "\n\n")
                else:
                    result_text.insert(tk.END, "No recipes found with the selected ingredients.\n\n")
                    result_text.insert(tk.END, f"Your selected ingredients: {selected_ingredient_names}\n")
                    result_text.insert(tk.END, f"Your selected ingredient IDs: {selected_ingredient_ids}")

            else:
                a=datetime.now()
                for i in range (0,len(selected_ingredient_ids)):
                    cursor.execute('select expiration from ingredient where FID=?',(selected_ingredient_ids[i],))
                    rows = cursor.fetchall()
                    c = [int(row[0]) for row in rows]
                    b=a+ relativedelta(days=+c[0])
                    cursor2.execute('insert into expiry (purchase_date, expiration_date, FID) values (?,?,?) ',
                                    (str(a), str(b),selected_ingredient_ids[i],))
                    conn2.commit()
                cursor2.execute('select * from expiry')
                rows=cursor2.fetchall()
                result_window = tk.Toplevel(root)
                result_window.title("Ingredients expiration status")
                result_window.geometry("600x400")
    
                # Create scrollable text area
                text_frame = tk.Frame(result_window)
                text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
                scrollbar = tk.Scrollbar(text_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
                result_text = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
                result_text.pack(fill=tk.BOTH, expand=True)
                scrollbar.config(command=result_text.yview)
                for row in rows:
                    print(row)
                    cursor.execute('select name from ingredient where FID=?',(row[0],))
                    rows2 = cursor.fetchall()
                    c = [str(row2[0]) for row2 in rows2]
                    result_text.insert(tk.END, f"Date recorded: {row[1]} expiration date: {row[2]} Name: {c[0]}\n")
            result_text.config(state=tk.DISABLED)  # Make read-only
            close_button = tk.Button(result_window, text="Close", command=result_window.destroy)
            close_button.pack(pady=5)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, width=15, height=2, text="Add →", 
                              command=add_ingredient, state=tk.DISABLED)
        add_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, width=15, height=2, text="← Remove", 
                                 command=delete_selected_item, state=tk.DISABLED)
        delete_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(button_frame, width=15, height=2, text="Clear All", 
                                command=clear_selection)
        clear_button.pack(side=tk.LEFT, padx=5)
        if y is True:
            s="Find Recipes"
        else:
            s="Store ingredient(s)"
        submit_button = tk.Button(button_frame, width=18, height=2, text=s, 
                                 command=submit, state=tk.DISABLED)
        submit_button.pack(side=tk.LEFT, padx=5)

        # Bind selection events
        listbox.bind('<<ListboxSelect>>', on_available_select)
        selected_listbox.bind('<<ListboxSelect>>', on_selected_select)

        def on_closing():
            conn.close()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        x=False

cursor2.execute("select FID,purchase_date, expiration_date from expiry")
rows= cursor2.fetchall()
expired=[]
pdate1=[]
edate1=[]
going=[]
pdate2=[]
edate2=[]
ok=[]
pdate3=[]
edate3=[]
for row in rows:
    days_until_expiry = (parse(str(row[2])) - datetime.now()).days
    cursor.execute("select name from ingredient where FID=?",(row[0],))
    take=cursor.fetchall()
    a=take[0]
    if days_until_expiry<0:
        expired.append(str(a[0]))
        pdate1.append(str(row[1]))
        edate1.append(str(row[2]))
    elif days_until_expiry<=1:
        going.append(str(a[0]))
        pdate2.append(str(row[1]))
        edate2.append(str(row[2]))
    else:
        ok.append(str(a[0]))
        pdate3.append(str(row[1]))
        edate3.append(str(row[2]))
if len(expired)+len(going)>0:
    messagebox.showwarning("Some ingredients are expired/going to expire", "please check the storage")
    speak("Some ingredients are expired or going to expire, please check the storage")
def storage(x):
    if x is True:
        storage_window = tk.Toplevel(root)
        storage_window.title("Food storage check")
        storage_window.geometry("800x600")
        elabel=tk.Label(storage_window,text="Already expired ingredients")
        elist=tk.Listbox(storage_window,width=100)
        for i in range (0,len(expired)):
            elist.insert(i,f"Name: {expired[i]} || date of purchase: {pdate1[i]} || date of expiry: {edate1[i]}")
        elabel.grid(row=1,column=0,sticky="w")
        elist.grid(row=2,column=0,sticky="ew")
        glabel=tk.Label(storage_window,text="About to expire ingredients")
        glist=tk.Listbox(storage_window,width=100)
        for i in range (0,len(going)):
            glist.insert(i,f"Name: {going[i]} || date of purchase: {pdate2[i]} || date of expiry: {edate2[i]}")
        glabel.grid(row=3,column=0,sticky="w")
        glist.grid(row=4,column=0,sticky="ew")
        olabel=tk.Label(storage_window,text="Available ingredients")
        olist=tk.Listbox(storage_window,width=100)
        for i in range (0,len(ok)):
            olist.insert(i,f"Name: {ok[i]} || date of purchase: {pdate3[i]} || date of expiry: {edate3[i]}")
        olabel.grid(row=5,column=0,sticky="w")
        olist.grid(row=6,column=0,sticky="ew")

def objectdetection(x,y):
    if x is True and y is True:
        speak("Please have your food hold in front of the camera,then press the letter C to take the picture")
        cap = cv2.VideoCapture(0)

        while True:
            # Read a frame from the webcam
            ret, frame = cap.read()
    
            if not ret:
                print("Failed to grab frame")
                break

            # Display the frame
            cv2.imshow("Webcam", frame)

            # Wait for the user to press 'c' to capture the image
            if cv2.waitKey(1) & 0xFF == ord('c'):
                # Save the captured frame as an image
                image_path = "captured_image.jpg"
                cv2.imwrite(image_path, frame)

                # Run the workflow on the captured image
                result = client.run_workflow(
                    workspace_name="519studio",
                    workflow_id="custom-workflow-2",
                    images={"image": image_path},
                    use_cache=True
                )

                # Print the results
                #print(result)
                ingredients = []
                for item in result:
                    if 'predictions' in item and 'predictions' in item['predictions']:
                        for prediction in item['predictions']['predictions']:
                            if 'class' in prediction:
                                ingredients.append(prediction['class'])
                for i in range (0,len(ingredients)):
                    speak(f"Detected {ingredients[i]}")
                speak("Press the letter q to proceed")
                print(ingredients)
            # Exit the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the webcam and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
        
        a=datetime.now()
        for i in range (0,len(ingredients)):
            cursor.execute('select FID,expiration from ingredient where Name=?',(ingredients[i],))
            rows = cursor.fetchall()
            d = [int(row[0]) for row in rows]
            c = [int(row[1]) for row in rows]
            print(c,d)
            b=a+ relativedelta(days=+c[0])
            cursor2.execute('insert into expiry (purchase_date, expiration_date, FID) values (?,?,?) ',
                            (str(a), str(b),int(d[0]),))
            conn2.commit()
        cursor2.execute('select * from expiry')
        rows=cursor2.fetchall()
        result_window = tk.Toplevel(root)
        result_window.title("Ingredients expiration status")
        result_window.geometry("600x400")
    
        # Create scrollable text area
        text_frame = tk.Frame(result_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
        result_text = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        result_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=result_text.yview)
        for row in rows:
            print(row)
            cursor.execute('select name from ingredient where FID=?',(row[0],))
            rows2 = cursor.fetchall()
            c = [str(row2[0]) for row2 in rows2]
            result_text.insert(tk.END, f"Date recorded: {row[1]} expiration date: {row[2]} Name: {c[0]}\n")
    result_text.config(state=tk.DISABLED)  # Make read-only
    close_button = tk.Button(result_window, text="Close", command=result_window.destroy)
    close_button.pack(pady=5)

frame1=tk.Frame(root,width=800, height=600,bg="#111111")
frame2=tk.Frame(root,width=800, height=600,bg="#111111")
frame3=tk.Frame(root,width=800, height=600,bg="#111111")
frame4=tk.Frame(root,width=800, height=600,bg="#111111")
frame1.pack()
label1=tk.Label(frame1, text="Welcome to the AI Food Manager",font=("Arial", 24),fg="#FFFFFF",bg="#111111")
label1.grid(row=1,column=2)
label2=tk.Label(frame1, text="This platform is built by a group of teenagers from CityU GEF programme",font=("Arial",10),fg="#FFFFFF",bg="#111111")
label2.grid(row=3,column=2)
label3=tk.Label(frame1,text="List of contributors",font=("Arial",15),fg="#FFFFFF",bg="#111111")
label3.grid(row=10,column=2)
label4=tk.Label(frame2,text="Please select the mode for recipe generation",font=("Arial",15),fg="#FFFFFF",bg="#111111")
label4.grid(row=1,column=2)
label5=tk.Label(frame3,text="Please select the mode for expiry management",font=("Arial",15),fg="#FFFFFF",bg="#111111")
label5.grid(row=1,column=2)
contributorslist=tk.Listbox(frame1,width=50,height=5,fg="#FFFFFF",bg="#111111")
contributors=("CHAN Nga Wang (04)","LAU Long Yat Damian (23)","POON Kai Hang (36)","YAM Po Sing (44)")
for i in range (1,5):
    contributorslist.insert(i,contributors[i-1])
contributorslist.grid(row=13,column=2)
def button0_click():
    S[2]="the start button for expiry management"
    doubleclick(frame1,frame3,0)
def button1_click():
    S[2]="the start button for recipe generation"
    doubleclick(frame1,frame2,1)
def button2_click():
    S[2]="the return button"
    doubleclick(frame2,frame1,2)
def button3_click():
    S[2]="Normal mode"
    doubleclick(frame2,frame2,3)
    recipegen(S[3],True)
def button4_click():
    S[2]="Artificial Intelligence mode"
    doubleclick(frame2,frame4,4)

def button5_click():
    S[2]="the return button"
    doubleclick(frame3,frame1,5)
def button6_click():
    S[2]="Normal mode"
    doubleclick(frame3,frame3,6)
    recipegen(S[3],False)
def button7_click():
    S[2]="Artificial Intelligence mode"
    doubleclick(frame3,frame3,7)
    objectdetection(S[3],True)
def button8_click():
    S[2]="Food storage checking"
    doubleclick(frame3,frame3,8)
    storage(S[3])
button0=tk.Button(frame1,width=35, height=2,text="Start with food expiry management",command=button0_click,bg="#FFFFFF")
button0.grid(row=24,column=2)
button1=tk.Button(frame1,width=35, height=2,text="Start with recipe generation",command=button1_click,bg="#FFFFFF")
button1.grid(row=26,column=2)
button2=tk.Button(frame2,width=23, height=2,text="Return to the previous page",command=button2_click,bg="#FFFFFF")
button3=tk.Button(frame2,width=15, height=2,text="Normal mode",bg="#FFFFFF",command=button3_click)
button4=tk.Button(frame2,width=15, height=2,text="AI mode",bg="#FFFFFF",command=button4_click)
button2.grid(row=2,column=2)
button3.grid(row=3,column=2,sticky="e")
button4.grid(row=3,column=2,sticky="w")
button5=tk.Button(frame3,width=23, height=2,text="Return to the previous page",command=button5_click,bg="#FFFFFF")
button6=tk.Button(frame3,width=15, height=2,text="Normal mode",bg="#FFFFFF",command=button6_click)
button7=tk.Button(frame3,width=15, height=2,text="AI mode",bg="#FFFFFF",command=button7_click)
button8=tk.Button(frame3,width=15, height=2,text="Storage check",bg="#FFFFFF",command=button8_click)
button5.grid(row=2,column=2)
button6.grid(row=3,column=2,sticky="e")
button7.grid(row=3,column=2,sticky="w")
button8.grid(row=3,column=2)

root.mainloop()
