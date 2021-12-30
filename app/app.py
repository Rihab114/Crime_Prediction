import re
from flask import Flask, render_template, request, jsonify
from flask.helpers import flash
from tensorflow import keras

model = keras.models.load_model("XGboost_final")

app = Flask(__name__)
app.secret_key ="crime prediction"
Year =0
Hour =0
Latitude =0
Longitude =0
name =''
Time_Duration =0
Day=0
BORO_NM_BROOKLYN =0
BORO_NM_MANHATTAN =0
BORO_NM_QUEENS =0
BORO_NM_STATEN_ISLAND =0
VIC_SEX_F =0
VIC_SEX_M =0

data = {}
@app.route('/' , methods=[ "GET" ,"POST" ])
def hello():
    
    if (request.method =="POST"):
        name = request.form.get("name")
        Latitude = request.form.get("x")
        Longitude = request.form.get("y")
       
        Time_Duration = request.form.get("duration")
       
       
        boro = request.form.get("boro_state")
        if(int(boro) == 'BROOKLYN '):
            LAW_CAT_CD_BROOKLYN =1
            LAW_CAT_CD_STATEN_ISLAND=1
            LAW_CAT_CD_QUEENS=0
            LAW_CAT_CD_MANHATTAN=0
        if(int(boro) == 'MANHATTAN'):
            LAW_CAT_CD_MANHATTAN=1
            LAW_CAT_CD_STATEN_ISLAND=1
            LAW_CAT_CD_QUEENS=0
            LAW_CAT_CD_BROOKLYN =0
        if(int(boro) == 'QUEENS'):
            LAW_CAT_CD_QUEENS=1
            LAW_CAT_CD_STATEN_ISLAND=1
            LAW_CAT_CD_MANHATTAN=0
            LAW_CAT_CD_BROOKLYN =0
        if(int(boro) == 'STATEN_ISLAND'):
            LAW_CAT_CD_STATEN_ISLAND=1
            LAW_CAT_CD_QUEENS=0
            LAW_CAT_CD_MANHATTAN=0
            LAW_CAT_CD_BROOKLYN =0
      
        time =request.form.get('time')
        date=request.form.get('date')
        gender = request.form.get('gender') 
        cmplnt = date.split("-")
        YEAR=int(cmplnt[0])
        MONTH=int(cmplnt[1])
        Day=int(cmplnt[2])
        
        Hour = int(time.split(":")[0])
     
        if (int(gender)==1):
            VIC_SEX_F=1
            VIC_SEX_M=0
        if (int(gender)==0):
            VIC_SEX_M=1
            VIC_SEX_F=0
        Latitude=float(Latitude)
        Longitude=float(Longitude)
        ky_cd = model.predict(
            [
                [
                    Year ,
                    Hour ,
                    Latitude ,
                    Longitude ,
                    Time_Duration,
                    BORO_NM_BROOKLYN ,
                    BORO_NM_MANHATTAN ,
                    BORO_NM_QUEENS ,
                    BORO_NM_STATEN_ISLAND ,
                    VIC_SEX_F ,
                    VIC_SEX_M    
                ]
            ]
        )
        
        # probability of crimes
            


        data["HARRASSMENT 2 "] = format(ky_cd[0][0]*100, '.2f')
        data["ASSAULT 3 & RELATED OFFENSES"] = format(ky_cd[0][1]*100 , '.2f')
        data["PETIT LARCENY"] = format(ky_cd[0][3]*100, '.2f')
        data["OFF. AGNST PUB ORD SENSBLTY &"] = format(ky_cd[0][4]*100 , '.2f')
        data["CRIMINAL MISCHIEF & RELATED OF"] = format(ky_cd[0][5]*100 , '.2f')
        data["FELONY ASSAULT"] = format(ky_cd[0][6]*100 , '.2f')
        data["GRAND LARCENY"] = format(ky_cd[0][7]*100 , '.2f')
        data["MISCELLANEOUS PENAL LAW"] = format(ky_cd[0][8]*100 , '.2f')
        data["ROBBERY"] = format(ky_cd[0][9]*100 , '.2f')
        data["DANGEROUS DRUGS"] = format(ky_cd[0][10]*100 , '.2f')
        data["OFFENSES AGAINST PUBLIC ADMINI"] = format(ky_cd[0][2]*100 , '.2f')
        data["BURGLARY"] = format(ky_cd[0][11]*100 , '.2f')
        data["DANGEROUS WEAPONS"] = format(ky_cd[0][12]*100 , '.2f')
        data["SEX CRIMES"] = format(ky_cd[0][13]*100 , '.2f')
        data["INTOXICATED & IMPAIRED DRIVING"] = format(ky_cd[0][14]*100 , '.2f')
        data["FORGERY"] = format(ky_cd[0][15]*100 , '.2f')
        data["VEHICLE AND TRAFFIC LAWS"] = format(ky_cd[0][16]*100 , '.2f')
        data["CRIMINAL TRESPASS"] = format(ky_cd[0][17]*100 , '.2f')
        data["RAPE"] = format(ky_cd[0][18]*100 , '.2f')
        data["FELONY ASSAULT"] = format(ky_cd[0][19]*100 , '.2f')
        flash(data)
    return render_template("osm_gs.html" )  
