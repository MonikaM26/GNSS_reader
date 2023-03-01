from flask import Flask,request, render_template, url_for,redirect,session
import numpy as np
import pygal
from markupsafe import escape

APP = Flask(__name__)
APP.secret_key = 'qsefthukooo'

@APP.route('/' , methods = ['GET', 'POST'])
def home():
    return render_template("index.html")

@APP.route('/step1' , methods = ['GET', 'POST'])
def rootpage():
    if request.method == 'POST':
        session.clear()
        height = float(request.form.get('val'))
        substance = float(request.form.get('val2'))
        r1 = float(request.form.get('val3'))
        session["height"] = height
        session["substance"] = substance
        session["r1"] = r1
        return redirect(url_for("user"))
    else:
        return render_template("nowy.html")
@APP.route("/user", methods = ['GET', 'POST'])
def user():
    if "height" and "substance" and "r1" in session:
        height = session["height"]
        r1 = session["r1"]
        substance = session["substance"]
        sub_tab =[80.0, 47.0, 3.0, 84.0, 17.0]
        sub_text = ["water","glycerin","salt","H2SO4","ammonia"]
        l_tab = [height*0.0001, height*0.1,height*0.20, height*0.3,height*0.4,height*0.5,height*0.6,height*0.7, height*0.8, height*0.9, height*1.0]
        x = None
        C1 =[]; C2=[]; C3=[]; C4=[]; C5 = []
        C1.extend([x]*11); C2.extend([x]*11); C3.extend([x]*11); C4.extend([x]*11); C5.extend([x]*11)
        L1 =[]; L2=[]; L3=[]; L4=[]; L5 = []
        L1.extend([x]*11); L2.extend([x]*11); L3.extend([x]*11); L4.extend([x]*11); L5.extend([x]*11)
        C_tot = [C1,C2,C3,C4,C5]
        lvl_tot = [L1, L2, L3, L4, L5]
        C_tab = []
        lvl_tab = []
        if request.method == 'POST':
            if request.form.get("Submit"):
                level = float(request.form.get('val'))
                perc_lvl = level
                level = height * level
                if request.form.get('C_out'):
                    C_out = float(request.form.get('C_out'))
                    C_obl = C_calc2(level, r1, height, substance)
                    if C_out != C_obl:
                        err = 1
                        return render_template("step2.html",
                                               err=err,
                                               C_obl=C_obl,
                                               r1 =r1)
                    else:
                        for i in range(len(sub_tab)):
                            if substance == sub_tab[i]:
                                substance_text = sub_text[i]
                                if "poj" and "lvl" in session:
                                    C_tot = session["poj"]
                                    lvl_tot = session["lvl"]
                                    print("tutaj")
                                    pass
                                if C_out in C_tot[i]:
                                    pass
                                else:
                                    C_tot = functt(C_tot, C_obl, i, l_tab, level)
                                    print(C_tot)
                                    #lvl_tot = level*height/100
                        session["poj"] = C_tot
                        session["lvl"] = lvl_tot
                        return render_template("step2.html",
                                               height=height,
                                               r1=r1,
                                               substance=substance,
                                               substance_text=substance_text,
                                               level=level,
                                               C_out=C_out,
                                               C_tot=C_tot,
                                               lvl_tot=lvl_tot,
                                               perc_lvl= perc_lvl)
                else:
                    err1 = 1
                    return render_template("step2.html",
                                           err1=err1)
            elif request.form.get("button1"):
                return redirect(url_for("substance"))
            elif request.form.get("button"):
                try:
                    lvl_tot = session['lvl']
                    C_tot = session['poj']
                    height = session["height"]
                    tab = [0, 0.25, 0.5, 0.75, 1]
                    tab2 =[]
                    for i in tab:
                        tab2.append(i*float(height))
                    line_chart = pygal.Line(height = 450,legend_box_size=18, legend_at_bottom=True)
                    line_chart.title = 'Output capacitance in function of substance level [cm]'
                    line_chart.x_labels = map(str, tab2)
                    line_chart.add('C_out [nF] for water', C_tot[0])
                    line_chart.add('C_out [nF] for glycerin', C_tot[1])
                    line_chart.add('C_out [nF] for salt', C_tot[2])
                    line_chart.add('C_out [nF] for H2SO4', C_tot[3])
                    line_chart.add('C_out [nF] for ammonia', C_tot[4])
                    graph_data = line_chart.render_data_uri()
                    session["graf"] = graph_data
                    return render_template("step2.html", graph_data=graph_data, C_tot=C_tot, lvl_tot=lvl_tot)
                except:
                    err1 = 1
                    print("blad err1")
                    return render_template("step2.html",
                                           err1=err1,r1=r1)
            return f"<p>error</p>"
        return render_template("step2.html",
                               substance=substance,
                               height=height,
                               r1=r1)
    else:
        return f"<p>error</p>"
def C_calc(level,r1,height,substance):
    eps0 = 0.00000000000885
    eps_pow = 1.0
    pi = 3.14
    r2 = 2.5
    air = height - level
    C = round(2.0*pi*eps0*(substance*level + eps_pow*air)/np.log(r2/r1)*10**9,2)
    return C

def functt(C_tot,C_obl,i,l_tab,level):
    for a in range(len(l_tab)):
        if level == l_tab[a]:
            C_tot[i][a] = C_obl
            print(level,l_tab[a],a,i)
            return C_tot

@APP.route("/theory", methods = ['GET', 'POST'])
def theory():
    return render_template('teoria.html')

@APP.route("/instr", methods = ['GET', 'POST'])
def instr():
    return render_template('instrukcja.html')

@APP.route("/step3", methods = ['GET', 'POST'])
def step3():
    if "height" and "substance" and "r1" in session:
        if request.method == 'POST' and 'Submit':
            r1 = float(request.form.get('val'))
            if r1 == 0.0:
                return render_template('step3.html')
            else:
                session['r1'] = r1
                return redirect(url_for("step2v2"))
        return render_template('step3.html')
    else:
        return f"<p>error<p>"

@APP.route("/substance", methods = ['GET', 'POST'])
def substance():
    if "height" and "substance" and "r1" in session:
        if request.method == 'POST' and 'Submit':
            substance = float(request.form.get('val'))
            if substance == 0.0:
                return render_template('substanca.html')
            else:
                session['substance'] = substance
                return redirect(url_for("user"))
        return render_template('substanca.html')
    else:
        return f"<p>error<p>"

@APP.route("/step2v2", methods = ['GET', 'POST'])
def step2v2():
    if "height" and "substance" and "r1" in session:
        height = session["height"]
        r1 = session["r1"]
        substance = session["substance"]
        sub_text = ["water","glycerin","salt","H2SO4","ammonia"]
        sub_tab =[80.0, 47.0, 3.0, 84.0, 17.0]

        r1_tab =[0.1, 0.2, 0.3, 0.5, 0.7]
        l_tab = [height*0.0001, height*0.1,height*0.20, height*0.3,height*0.4,height*0.5,height*0.6,height*0.7, height*0.8, height*0.9, height*1.0]
        x = None
        C1 =[]; C2=[]; C3=[]; C4=[]; C5 = []
        C1.extend([x]*11); C2.extend([x]*11); C3.extend([x]*11); C4.extend([x]*11); C5.extend([x]*11)
        L1 =[]; L2=[]; L3=[]; L4=[]; L5 = []
        L1.extend([x]*11); L2.extend([x]*11); L3.extend([x]*11); L4.extend([x]*11); L5.extend([x]*11)
        C_tot = [C1,C2,C3,C4,C5]
        lvl_tot = [L1, L2, L3, L4, L5]
        if request.method == 'POST':
            if request.form.get("Submit"):
                level = float(request.form.get('val'))
                perc_lvl = level
                level = height * level
                if request.form.get('C_out'):
                    C_out =float(request.form.get('C_out'))
                    C_obl = C_calc2(level, r1, height, substance)
                    if C_out != C_obl:
                        err = 1
                        print("error")
                        return render_template("step2v2.html",
                                               err=err,
                                               C_obl=C_obl,
                                               r1 =r1)
                    else:
                        for i in range(len(r1_tab)):
                            for g in range(len(sub_tab)):
                                if sub_tab[g] == substance:
                                    substance_text = sub_text[g]
                            if r1 == r1_tab[i]:
                                if "poj1" and "lvl1" in session:
                                    C_tot = session["poj1"]
                                    lvl_tot = session["lvl1"]
                                if C_out in C_tot[i]:
                                    pass
                                else:
                                    C_tot = funct(C_tot,C_obl,i,l_tab,level)
                        session["poj1"] = C_tot
                        session["lvl1"] = lvl_tot
                        return render_template("step2v2.html",
                                               height=height,
                                               r1=r1,
                                               substance=substance,
                                               substance_text=substance_text,
                                               level=level,
                                               C_out=C_out,
                                               C_tot=C_tot,
                                               lvl_tot=lvl_tot,
                                               perc_lvl= perc_lvl)
                else:
                    err1 = 1
                    print("blad err1")
                    return render_template("step2v2.html",
                                           err1=err1)
            elif request.form.get("button1"):
                return redirect(url_for("step3"))
            elif request.form.get("button"):
                try:
                    lvl_tot = session['lvl1']
                    height = session["height"]
                    tab = [0, 0.25, 0.5, 0.75, 1]
                    tab2 =[]
                    for i in tab:
                        tab2.append(i*float(height))
                    C_tot = session['poj1']
                    line_chart = pygal.Line(height = 450,legend_box_size=18,legend_at_bottom=True)
                    line_chart.title = 'Output capacitance in function of electrode diameter size r1 [cm]'
                    line_chart.x_labels = map(str, tab2)
                    line_chart.add('C_out [nF] for r1=0.1cm', C_tot[0])
                    line_chart.add('C_out [nF] for r1=0.2cm', C_tot[1])
                    line_chart.add('C_out [nF] for r1=0.3cm', C_tot[2])
                    line_chart.add('C_out [nF] for r1=0.5cm', C_tot[3])
                    line_chart.add('C_out [nF] for r1=0.7cm', C_tot[4])
                    graph_data = line_chart.render_data_uri()
                    session["graf"] = graph_data
                    return render_template("step2v2.html", graph_data = graph_data,C_tot =C_tot, lvl_tot=lvl_tot,r1=r1)
                except:
                    err1 = 1
                    print("blad err1")
                    return render_template("step2v2.html",
                                           err1=err1,r1=r1)
            return f"<p>blad3</p>"
        return render_template("step2v2.html",
                                substance = substance,
                                height = height,
                                r1= r1)
    else:
        return f"<p>error</p>"

def C_calc2(level,r1,height,substance):
    eps0 = 0.00000000000885
    eps_pow = 1.0
    pi = 3.14
    r2 = 2.5
    air = height - level
    C = round(2.0*pi*eps0*(substance*level + eps_pow*air)/np.log(r2/r1)*10**9, 2)
    return C
def funct(C_tot,C_obl,i,l_tab,level):
    for a in range(len(l_tab)):
        if level == l_tab[a]:
            C_tot[i][a] = C_obl
            print(level,l_tab[a],a,i)
            return C_tot

@APP.route("/temp_substance", methods = ['GET', 'POST'])
def temp_substance():
    if "height" and "substance" and "r1" in session:
        if request.method == 'POST' and 'Submit':
            substance = float(request.form.get('val'))
            if substance == 0.0:
                return render_template('substanca2.html')
            else:
                session['substance'] = substance
                return redirect(url_for("temp_"))
        return render_template('substanca2.html')
    else:
        return f"<p>nie dzialam<p>"
@APP.route("/step2v3", methods = ['GET', 'POST'])
def temp_():
    if "height" and "substance" and "r1" in session:
        height = session["height"]
        r1 = session["r1"]
        substance = session["substance"]
        x= None
        C1 =[]; C2=[]; C3=[];C4=[]; C5=[];
        sub_text = ["water","glycerin","salt","H2SO4","ammonia"]
        C1.extend([x]*3); C2.extend([x]*3); C3.extend([x]*3); C4.extend([x]*3); C5.extend([x]*3);
        T1 =[]; T2=[]; T3=[]; T4=[]; T5=[];
        T1.extend([x]*3); T2.extend([x]*3); T3.extend([x]*3);T4.extend([x]*3); T5.extend([x]*3);
        C_tot = [C1,C2,C3,C4,C5]
        temp_tot = [T1, T2, T3, T4, T5]

        water = [88.0, 80.0, 78.0]
        glycerin = [41.2, 47.0, 42.7]
        salt = [1.0,3.0,15.0]
        h2so4 = [65.0,84.0,100.0]
        ammonia = [20.0, 17.0, 15.0]
        subst = [water, glycerin, salt, h2so4, ammonia]
        temp_tab = [0.0, 20.0, 25.0]
        s = [80.0, 47.0, 3.0, 84.0, 17.0]
        if request.method == 'POST':
            if request.form.get("Submit"):
                level = 0.5
                temp = float(request.form.get('val'))
                perc_lvl = level
                level = height * level
                substance = permittiti_check(temp,temp_tab,s,subst, substance)
                print(substance)
                if request.form.get('C_out'):
                    C_out = float(request.form.get('C_out'))
                    C_obl = C_calc2(level, r1, height, substance)
                    if C_out != C_obl:
                        err = 1
                        return render_template("step2v3.html",
                                               err=err,
                                               C_obl=C_obl,
                                               r1=r1)
                    else:
                        for i in range(len(subst)):
                            for j in range(len(subst[i])):
                                if substance == subst[i][j]:
                                    substance_text= sub_text[j]
                                    if "poj2" and "temp" in session:
                                        C_tot = session["poj2"]
                                        temp_tot = session["temp"]
                                    if C_out in C_tot[i]:
                                        pass
                                    else:
                                        C_tot[i][j] = C_obl
                                        temp_tot[i][j]= temp
                        session["poj2"] = C_tot
                        session["temp"] = temp_tot
                        return render_template("step2v3.html",
                                               height=height,
                                               r1=r1,
                                               substance=substance,
                                               substance_text=substance_text,
                                               level=level,
                                               C_out=C_out,
                                               C_tot=C_tot,
                                               temp_tot= temp_tot,
                                               perc_lvl=perc_lvl,
                                               glycerin =glycerin,
                                               water =water,
                                               salt=salt,
                                               h2so4=h2so4,
                                               ammonia=ammonia)
                else:
                    err1 = 1
                    return render_template("step2v3.html",
                                           err1=err1,
                                           r1 = r1)
            elif request.form.get("button1"):
                return redirect(url_for("temp_substance"))
            elif request.form.get("button"):
                try:
                    temp_tot = session['temp']
                    C_tot = session['poj2']
                    line_chart = pygal.Line(height=450, legend_box_size=18, legend_at_bottom=True)
                    line_chart.title = 'Output capacitance in function of substance temperature [degrees of Celsius]'
                    line_chart.x_labels = map(str, temp_tab)
                    line_chart.add('C_out [nF] for water', C_tot[0])
                    line_chart.add('C_out [nF] for glycerin', C_tot[1])
                    graph_data = line_chart.render_data_uri()
                    session["graf"] = graph_data
                    return render_template("step2v3.html", graph_data=graph_data, C_tot=C_tot, temp_tot=temp_tot, r1 = r1)
                except:
                    err1 = 1
                    print("blad err1")
                    return render_template("step2v3.html",
                                           err1=err1,r1=r1)
            return f"<p>error</p>"
        return render_template("step2v3.html",
                               substance=substance,
                               height=height,
                               r1=r1)
    else:
        return f"<p>error</p>"

def permittiti_check(temp,temp_tab,s,subst, substance):
    for i in range(len(subst)):
        if substance == subst[i][1]:
            print(subst[i][1])
            for j in range(len(temp_tab)):
                if temp == temp_tab[j]:
                    return subst[i][j]

def C_calc2(level, r1, height, substance):
    eps0 = 0.00000000000885
    eps_pow = 1.0
    pi = 3.14
    r2 = 2.5
    air = height - level
    C = round(2.0 * pi * eps0 * (substance * level + eps_pow * air) / np.log(r2 / r1) * 10 ** 9, 2)
    return C

if __name__ == "__main__":
    APP.run()
