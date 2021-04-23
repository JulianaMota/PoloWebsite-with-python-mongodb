from flask import Flask, render_template, request
import pymongo
import json
import os

app = Flask(__name__)

#HOME PAGE
@app.route('/', methods=['GET'])
def showindexpage() :
    global mymessage, mydb, mycol, mydata
    return render_template("Index.html")


#PLAYERS PAGE
@app.route('/players', methods=['GET', 'POST'])
def showPlayerspage() :
    global mymessage, mydb, mycol, mydata
    mymessage = ""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["PoloDB"]
    mycol = mydb["Players"]
    mydata = mycol.find()
    mypicturepath = os.path.join('static', 'images')
    myadd = False
    showform = False
    myupdate = False
    mydelete = False
    myformTitle = ''

    if request.method == 'POST':
        if request.form['myform'] == "Add New Player" :
            myformTitle = 'Add New Player'
            showform = True
            myadd = True
        elif request.form['myform'] == "Update Player" :
            myformTitle = 'Update Player'
            showform = True
            myupdate = True
        elif request.form['myform'] == "Delete Player" :
            myformTitle = 'Delete Player'
            showform = True
            mydelete = True
        elif request.form['myform'] == "Add" :
            addPlayer()
        elif request.form['myform'] == "Update" :
            updatePlayer()
        elif request.form['myform'] == "Delete" :
            deletePlayer()
        else :
            showform = False


    return render_template("players.html", values = mydata, message = mymessage, path = mypicturepath, add = myadd, form = showform, update = myupdate, delete = mydelete, formTitle = myformTitle)

#ADD PLAYER
def addPlayer() :
    global mymessage, mydb, mycol, mydata
    try:
        playerid = int(request.form["_id"])
        name = request.form["name"]
        picture = request.form["picture"]
        number = int(request.form["number"])
        age = int(request.form["age"])
        horseName = request.form["horse-name"]
        horsePic = request.form["horse-pic"]
        manager = request.form["manager"]
        myplayer = {"_id": playerid, "name": name, "age": age, "picture": picture, "horse-name": horseName, "horse-picture": horsePic, "number": number,  "manager": manager}
        mycol.insert_one(myplayer)

        mymessage = "Player with id " + str(playerid) + " was interted"
    except Exception as ex:
        mymessage = "Insert Player " + request.form["_id"] + " : error on data"

#UPDATE PLAYER
def updatePlayer() : 
    global mymessage, mydb, mycol, mydata

    try:
        playerid = int(request.form["_id"])
        name = request.form["name"]
        picture = request.form["picture"]
        number = int(request.form["number"])
        age = int(request.form["age"])
        horseName = request.form["horse-name"]
        horsePic = request.form["horse-pic"]
        manager = request.form["manager"]
        mycol.update_one({"_id": playerid}, { "$set": {"name": name, "age": age, "picture": picture, "horse-name": horseName, "horse-picture": horsePic, "number": number,  "manager": manager}})
        

        mymessage = "Player with id " + str(playerid) + " was updated."
    except Exception as ex:
        mymessage = "Updated Player " + request.form["_id"] + " : error on data"

#DELETE PLAYER
def deletePlayer() :
    global mymessage, mydb, mycol, mydata

    try:
        playerid = int(request.form["_id"])
        mycol.delete_one({"_id": playerid})
        mymessage = "Player with id " + str(playerid) + " was deleted."
    except Exception as ex:
        mymessage = "Delete Player" + request.form["_id"] + " : error in data"


#TEAM PAGE
@app.route('/teams', methods=['GET', 'POST'])
def showTeamspage() :
    global mymessage, mydb, mycol, mydata, myTeams, myplayers
    mymessage = ""
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["PoloDB"]
    mycol = mydb["Teams"]
    myplayers = mydb["Players"]
   
    mypicturepath = os.path.join('static', 'images')
    myTeams = []
    myadd = False
    showform = False
    myupdate = False
    mydelete = False
    myformTitle = ''

   
    

    if request.method == 'POST':
        if request.form['myform'] == "Add New Team" :
            myformTitle = 'Add New Team'
            showform = True
            myadd = True
            showAll()
        elif request.form['myform'] == "Update Team Members" :
            myformTitle = 'Update Team Members'
            showform = True
            myupdate = True
            showAll()
        elif request.form['myform'] == "Delete Team" :
            myformTitle = 'Delete Team'
            showform = True
            mydelete = True
            showAll()
        elif request.form['myform'] == "Add" :
            addTeam()
        elif request.form['myform'] == "Update" :
            updateTeamMembers()
        elif request.form['myform'] == "Delete" :
            deleteTeam()
        else :
            showform = False
            showAll()
    else :
        showAll()



    return render_template("teams.html", values = myTeams, message = mymessage, path = mypicturepath, add = myadd, form = showform, update = myupdate, delete = mydelete, formTitle = myformTitle)

#SHOW ALL TEAMS
def showAll():
    global mymessage, mydb, mycol, mydata, myTeams, myplayers
    mydata = mycol.find()

    for team in mydata :
        myplayersList = []
        myTeams.append({"id": team["_id"], "name" : team["name"], "year": team["year"], "team" : myplayersList })
        playerslist = team["team-menbers"]
        for d in playerslist :
            myquery = {"_id": d}
            theplayer = myplayers.find(myquery)
            for p in theplayer : 
                myplayersList.append({"name" : p["name"], "picture": p["picture"], "number": p["number"]})

#ADD TEAM
def addTeam():
    global mymessage, mydb, mycol, mydata, myTeams, myplayers

    try:
        teamid = int(request.form["_id"])
        name = request.form["name"]
        year = int(request.form["year"])
        if "," in request.form["team"] :
            listP = request.form["team"].split(',')
            team = [int(i) for i in listP]
            print(team)
        else :
            team = [int(request.form["team"])]
            print(team)

        myteam = {"_id": teamid, "name": name, "year": year, "team-menbers": team }
        mycol.insert_one(myteam)

        mymessage = "Team with id " + str(teamid) + " was interted"
        
    except Exception as ex:
        mymessage = "Insert Team " + request.form["_id"] + " : error on data"
    showAll()

#UPDATE TEAM
def updateTeamMembers() :
    global mymessage, mydb, mycol, mydata, myTeams, myplayers

    try:
        teamid = int(request.form["_id"])
        if "," in request.form["team"] :
            listP = request.form["team"].split(',')
            team = [int(i) for i in listP]
            print(team)
        else :
            team = [int(request.form["team"])]
            print(team)

        mycol.update_one({"_id": teamid}, { "$set": {"team-menbers": team}})

        mymessage = "Team membes of Team with id " + str(teamid) + " was updates"
        
    except Exception as ex:
        mymessage = "Insert Team " + request.form["_id"] + " : error on data"

    showAll()


#DELETE TEAM
def deleteTeam() :
    global mymessage, mydb, mycol, mydata, myTeams, myplayers

    try:
        teamid = int(request.form["_id"])
        mycol.delete_one({"_id": teamid})
        mymessage = "Team with id " + str(teamid) + " was deleted."
    except Exception as ex:
        mymessage = "Delete Team" + request.form["_id"] + " : error in data"

    showAll()

if __name__ == '__main__':
    app.run('localhost', 4449)