# import relevant Flask libraries
from flask import Flask, render_template, request, redirect, url_for

# initialize the application
app = Flask(__name__)

# global id number counter for tasks
id_num = 1
# global list of todo task items
todos = []

# the home page of the application
@app.route("/")
def home():
    # just renders the base HTML page with the full list of todos
    return render_template("base.html", todo_list=todos)


# when user submits the form and wants to add a todo task
@app.route("/add", methods=["POST"])
def add():
    global id_num
    # add the new task to the todos list, with title of what the user inputted
    todos.insert(0, {"title": request.form.get("title"), "id": id_num, "complete": False})
    # increment id_num so that no 2 tasks have same id number
    id_num += 1
    # redirect to the homepage, i.e., the full list of todos
    return redirect(url_for("home"))


# when user clicks the completed button, completed field switches from True to False or False to True 
# when the task is "completed", it goes to the bottom of the todo list 
# when the task is "uncompleted", it goes to the top of the todo list 
@app.route("/complete/<int:todo_id>")
def update(todo_id):
    for idx, todo in enumerate(todos):
        if todo["id"] == todo_id:
            # find the task the user toggles by its id and change its completed status 
            todo["complete"] = not todo["complete"]
            temp = todos[idx]
            # if it goes from not completed to completed, remove that list item from its place in the list
            # append it to the back of the list 
            # now, it will show up at the bottom of the todo list 
            if todo["complete"] == True: 
                todos.pop(idx) 
                todos.append(temp)
            # if it goes from completed to not completed, remove that list item from its lpace in the lsit 
            # insert it to the front of the list 
            # now, it will show up at the top of the todo list 
            elif todo["complete"] == False: 
                todos.pop(idx) 
                todos.insert(0, temp)
            break
    # redirect user to homepage, (full list of todos)
    return redirect(url_for("home"))

# create logic to "prioritize" an item by moving it higher on the todo list 
@app.route("/prioritize/<int:todo_id>")
def prioritize(todo_id):
    # iterate through the list of tasks 
    # find the task we want to prioritize by matching the ids
    for idx, todo in enumerate(todos): 
        if todo["id"] == todo_id: 
            # if the list item we want to prioritize is already at the top of the list, do nothing
            if idx == 0:
                break 
            # move it higher on the list by switching that list item with the list item right before it in the todos list 
            else: 
                todos[idx], todos[idx - 1] = todos[idx - 1], todos[idx]
    # redirect user to homepage, (full list of todos)
    return redirect(url_for("home"))

# create logic to delete a list item 
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # iterate through list of todo items until we find the one with the matching id 
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            # delete the todo item by removing it from the todos list 
            todos.pop(i)
            break
    # redirect user to homepage, (full list of todos)
    return redirect(url_for("home"))