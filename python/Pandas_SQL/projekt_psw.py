"""Projekt wykonany w czasie studiów - analiza danych z bazy danych CSV i wykresy"""


import matplotlib.pyplot as plt
import pandas as pd


def chart1(data):
    # Podzial na szkoly prywante non-profit, prywatne for-profit, publiczne
    public = data.CONTROL =="Public" # sprawdzenie czy w danej komórce w kolumnie CONTROL występuje tekst "Public"
    
    # (zwracany obiekt zawierający boolowskie wartosci)
    new = data[public] # odczyt danych dla wierszy zawierających True/ pominiecie niepotrzebnych danych
    pb = new.INSTNM.drop_duplicates(keep='last').shape # wymiar obiektu po usunieciu powtarzających się wierszy w kolumnie INSTNM

    non_profit = data.CONTROL == "Private, nonprofit" # analogicznie dla koljenych szkół
    new2 = data[non_profit]
    non = new2.INSTNM.drop_duplicates(keep='last').shape

    for_profit = data.CONTROL == "Private, for-profit"
    new3 = data[for_profit]
    for_ = new3.INSTNM.drop_duplicates(keep = 'last').shape
    
    #tworzenie wykresu
    tab = [pb[0], non[0], for_[0]] # tablica przechowująca liczby danych szkół
    labels = ["Public", "Private, nonprofit", "Private, forprofit"]
    explode = (0.1,0.1,0.1) # rozsuniecie wykresu
    
    plt.pie(tab, labels = labels, autopct= '%.2f %%', shadow= True, explode = explode) # utworzenie wykresu kołowego
    plt.title("Procentowy podział na prywatne i publiczne uczelnie")
    plt.show() # wyświetlenie wykresu


def chart2(data):
    # Liczba uniwerstytetów i collegeów w USA
    new = data[data['INSTNM'].astype(str).str.contains("University")] # szukanie po stringu w kolumnie INSTNM "Universytet"
    x1 = new.INSTNM.drop_duplicates(keep='last').shape # Pominiecie powtórzen nazw
    
    new2 = data[data['INSTNM'].astype(str).str.contains("College")] # szukanie po stringu w kolumnie INSTNM "College"
    x2 = new2.INSTNM.drop_duplicates(keep='last').shape
    
    tabx = [x1[0],x2[0]]
    taby = ["University", "College"]
    
    plt.bar(taby,tabx) # wykres słupkowy
    plt.title("Liczba uniwersytetów i college'ów w USA")
    plt.show()
    return


def chart3(data):
    # Kierunki o największym średnim długu
    data = data[data.DEBTMEAN !="PrivacySuppressed"]
    data2 = data.astype({'DEBTMEAN': 'int32'}) # zamiana wartości kolumny "Debtmean" na int
    
    new = data2.sort_values(by =["DEBTMEAN"], ascending=False)
    new = new[new.DEBTMEAN > 350000] # filtrowanie długach większych niż 350 000 dolarów
    
    print(new["CIPDESC"],new["DEBTMEAN"], new["CREDDESC"])
    
    plt.plot(new.INSTNM,new.DEBTMEAN, 'ro')
    plt.xticks(new.INSTNM,  rotation= 90)
    plt.subplots_adjust(bottom=0.65)
    plt.title("Największy średni dług federalny pożyczkobiorów\n kończących studia") # spośród tych których są podane kwoty
    plt.subplots_adjust(left=0.2)
    plt.ylabel("Kwota [$]")
    plt.xlabel("Uczelnia")
    plt.show()
    return


def chart4(data):
    # Porównanie mediany zarobków i długu w zalezności od stopnia naukowego
    ylabel = ["Undergraduate Certificate or Diploma",
              "Bachelors Degree", "Master's Degree", 
              "Doctoral Degree", "First Professional Degree", 
              "Graduate/Professional Certificate"]
    data_ = data[data.MD_EARN_WNE !="PrivacySuppressed"] # pominiecie wierszy ktore nie zawierają danych
    data2 = data_.astype({'MD_EARN_WNE': 'int32'})

    data_1 = data[data.DEBTMEDIAN !="PrivacySuppressed"]
    data3 = data_1.astype({'DEBTMEDIAN': 'int32'})
    y = []  # tablice ktore beda przechowywac dane
    y2 = []

    under = data2.CREDDESC == ylabel[0] #filtrowanie po stopniach naukowych
    under.head()
    under_data = data2[under]
    y.append(round(under_data["MD_EARN_WNE"].mean(),2)) # odczyt zarobków i przypisanie ich średniej wartości do tablicy

    under_ = data3.CREDDESC == ylabel[0]
    under_.head()
    under_data2 = data3[under_]
    y2.append(round(under_data2["DEBTMEDIAN"].mean(),2)) # odczyt długów i przypisanie ich średniej wartości do tablicy

    bachelor = data2.CREDDESC == ylabel[1]
    bachelor.head()
    bachelor_data = data2[bachelor]
    y.append(round(bachelor_data["MD_EARN_WNE"].mean(),2)) # odczyt zarobków i przypisanie ich średniej wartości do tablicy

    bachelor_ = data3.CREDDESC == ylabel[1]
    bachelor_.head()
    bachelor_data2 = data3[bachelor_]
    y2.append(round(bachelor_data2["DEBTMEDIAN"].mean(),2)) # odczyt długów i przypisanie ich średniej wartości do tablicy

    master = data2.CREDDESC == ylabel[2]
    master.head()
    master_data = data2[master]
    y.append(round(master_data["MD_EARN_WNE"].mean(),2)) # odczyt zarobków i przypisanie ich średniej wartości do tablicy

    master_ = data3.CREDDESC == ylabel[2]
    master_.head()
    master_data2 = data3[master_]
    y2.append(round(master_data2["DEBTMEDIAN"].mean(),2)) # odczyt długów i przypisanie ich średniej wartości do tablicy

    doctoral = data2.CREDDESC == ylabel[3]
    doctoral.head()
    doctoral_data = data2[doctoral]
    y.append(round(doctoral_data["MD_EARN_WNE"].mean(),2)) # odczyt zarobków i przypisanie ich średniej wartości do tablicy

    doctoral_ = data3.CREDDESC == ylabel[3]
    doctoral_.head()
    doctoral_data2 = data3[doctoral_]
    y2.append(round(doctoral_data2["DEBTMEDIAN"].mean(),2)) # odczyt długów i przypisanie ich średniej wartości do tablicy

    prof = data2.CREDDESC == ylabel[4]
    prof.head()
    prof_data = data2[prof]
    y.append(round(prof_data["MD_EARN_WNE"].mean(),2)) # odczyt zarobków i przypisanie ich średniej wartości do tablicy

    prof_ = data3.CREDDESC == ylabel[4]
    prof_.head()
    prof_data2 = data3[prof_]
    y2.append(round(prof_data2["DEBTMEDIAN"].mean(),2)) # odczyt długów i przypisanie ich średniej wartości do tablicy

    prof2 = data2.CREDDESC == ylabel[5]
    prof2.head()
    prof2_data = data2[prof2]
    y.append(round(prof2_data["MD_EARN_WNE"].mean(),2)) # odczyt zarobków i przypisanie ich średniej wartości do tablicy

    prof2_ = data3.CREDDESC == ylabel[5]
    prof2_.head()
    prof2_data2 = data3[prof2_]
    y2.append(round(prof2_data2["DEBTMEDIAN"].mean(),2)) # odczyt długów i przypisanie ich średniej wartości do tablicy

    xlabel = ["Undergraduate Certificate\n or Diploma",
              "B. Degree", "M. Degree", 
              "PhD Degree", 
              "1. Prof. Degree",
              "Graduate/Prof.\n Certificate"]
    
    plot_ = pd.DataFrame({"Mediana długu": y2, "Mediana zarobków": y}, index = xlabel )
    plot_.plot.bar(rot = 90)
    
    plt.subplots_adjust(bottom=0.5) # przesuniecie wykresu zeby zmieścić opis
    plt.subplots_adjust(left=0.2)
    plt.ylabel("Kwota [$]")
    plt.xlabel("Uczelnia")
    plt.title("Porównanie mediany zarobków i długu\n po ukończeniu danego kierunku")
    plt.show()
    return


def chart5(data):
    #Wykres wydatków i zarobków dla konkretnego kierunku (Chemistry)
    data = data[data.CIPCODE == 4005] # filtrowanie po numerze odpowiadającym kierunkowi Chemistry
    data2 = data[data.MD_EARN_WNE !="PrivacySuppressed"] #pomieniecie  wierszy nie zawierajacych danych
    data2 = data2.astype({'MD_EARN_WNE': 'int32'})

    data3 = data[data.DEBTMEDIAN !="PrivacySuppressed"]
    data3 = data3.astype({"DEBTMEDIAN": 'int32'})

    x = []
    x2 = []
    ylabel = ["Bachelors Degree", "Master's Degree", "Doctoral Degree"] #bląd w pliku csv w nazwie bachelor's stad inny znak

    bachelor = data2.CREDDESC == ylabel[0]
    bachelor.head()
    bachelor_data = data2[bachelor]
    x.append(round(bachelor_data["MD_EARN_WNE"].mean(),2))

    bachelor_ = data3.CREDDESC == ylabel[0]
    bachelor_.head()
    bachelor2_data = data3[bachelor_]
    x2.append(round(bachelor2_data["DEBTMEDIAN"].mean(),2))

    master = data2.CREDDESC == ylabel[1]
    master.head()
    master_data = data2[master]
    x.append(round(master_data["MD_EARN_WNE"].mean(),2))

    master_ = data3.CREDDESC == ylabel[1]
    master_.head()
    master2_data = data3[master_]
    x2.append(round(master2_data["DEBTMEDIAN"].mean(),2))

    doctoral = data2.CREDDESC == ylabel[2]
    doctoral.head()
    doctoral_data = data2[doctoral]
    x.append(round(doctoral_data["MD_EARN_WNE"].mean(),2))

    doctoral_ = data3.CREDDESC == ylabel[2]
    doctoral_.head()
    doctoral2_data = data3[doctoral_]
    x2.append(round(doctoral2_data["DEBTMEDIAN"].mean(),2))
    
    #wykres słupkowy o 2 seriach długu i zarobkach
    plot_ = pd.DataFrame({"Mediana długu": x2, "Mediana zarobków": x}, index = ylabel )
    plot_.plot.bar(rot = 90)
    plt.subplots_adjust(bottom=0.4)
    plt.subplots_adjust(left=0.2)
    plt.ylabel("Kwota [$]")
    plt.xlabel("Uczelnia")
    plt.title("Porównanie mediany zarobków i długu\n na kierunku: Chemistry")
    plt.show()
    return


def chart6(data):
    #Podzial na kampus główny i nie dla wydzialu Chemistry
    data = data[data.CIPCODE ==4005] # filtrowanie po numerze odpowiadającym kierunkowi Chemistry
    main1 = len(data[data.MAIN == 1])
    main0 = len(data[data.MAIN == 0])
    tab1 = [main1, main0]
    label = ["Kampus główny", "Poza kampusem \ngłównym"]
    colors = ["#abbbef","#ffaacc"] #zmiana kolorów danych
    
    plt.title("Podział na kampus główny i uczelnie poza nim \nna przedmiocie Chemistry")
    plt.pie(tab1,labels = label, autopct= '%.2f %%', colors = colors) #wykres kołowy o zmienionych kolorach danych
    plt.show()
    return


def main():
    data = pd.read_csv("Most-Recent-Field-Data-Elements_.csv",encoding='cp1252', sep=';')
    
    chart1(data)
    chart2(data)
    chart3(data)
    chart4(data)
    chart5(data)
    chart6(data)


if __name__ == "__main__":
    main()