#include <iostream>
#include <stdlib.h>
#include <windows.h> //do sleep i beep
#include <conio.h> //do obsługi klawiatury
#include <fstream> //zapis do pliku
#include <time.h>

//using namespace std::literals::chrono_literals;
using namespace std;
#define L_MENU 5
//Poprawione funkcje obsugi menu, dodane timery i obsluga detergentow

class tryb
{
    class program
    {
    public:
        int temp;
        int czas;
        void UstawTemp(int x) {temp = x;}
        void UstawCzas(int y) {czas = y;}
        int PodajTemp(void) {return temp;}
        int PodajCzas(void) {return czas;}
    };
    public:
        program Wstepne;
        program Zasadnicze;
        program Plukanie;
        program Zmoczenie;
        program Suszenie;
        program Plukanie_na_zimno;
        tryb();
        void zmien_temp_krotki(int x)
        {
            Zmoczenie.UstawTemp(x);
            Zasadnicze.UstawTemp(x);
            Plukanie.UstawTemp(x);
        }
        void zmien_temp_standardowy(int x)
        {
            Zmoczenie.UstawTemp(x);
            Zasadnicze.UstawTemp(x);
            Plukanie.UstawTemp(x);
            Suszenie.UstawTemp(x);
        }
        void zmien_temp_dodatkowy(int x)
        {
            Zmoczenie.UstawTemp(x);
            Zasadnicze.UstawTemp(x);
            Plukanie.UstawTemp(x);
            Suszenie.UstawTemp(x);
            Wstepne.UstawTemp(x);

        }
};

tryb::tryb()
{
    Wstepne.UstawCzas(15);
    Zasadnicze.UstawCzas(25);
    Plukanie.UstawCzas(10);
    Zmoczenie.UstawCzas(5);
    Suszenie.UstawCzas(15);
    Plukanie_na_zimno.UstawCzas(10);

    Wstepne.UstawTemp(50);
    Zasadnicze.UstawTemp(50);
    Plukanie.UstawTemp(50);
    Zmoczenie.UstawTemp(50);
    Suszenie.UstawTemp(50);
    Plukanie_na_zimno.UstawTemp(50);
}
void zapisz(int x, int y, int z) //zapis detergerntow do pliku (konieczne do zasobnikow magazynowych)
{
    ofstream  myfile("zasoby.txt");
    if(myfile.is_open())
        myfile <<x<<" "<<y<<" "<< z;
    else cout <<"Unable to open file\n";
    myfile.close();
    return;
}
int watchdog(int StartTime)
{
    int EndTime = GetTickCount();
    int DeltaTime = EndTime - StartTime;
    return DeltaTime;
}

void det(int& x, int& y, bool& w,int limit)  //wybor detergentu
{
    int StartTime = GetTickCount();
    char c;
    do{
    system("cls");
    cout<<"\t\t\t============================WYBIERZ ZASOBNIK=============================="<<endl;
    cout<<"\t\t\t\t\t\tWybierz zasobnik:\n";
    cout<<"\t\t\t\t\t\t1. Magazynowy\n";
    cout<<"\t\t\t\t\t\t2. Jednorazowy\n";
    cout<<"\t\t\t\t\t\t3. Pomin\n\n";
    cout<<"\t\t\t========================================================================="<<endl;
    c=getch();
    if(watchdog(StartTime)> limit)
    {
        w = false;
        return;
    }
    switch(c)
    {
    case '1':
        char e;
        StartTime = GetTickCount();
        do{
        system("cls");
        cout<<"\t\t\t=======================WYBIERZ ZASOBNIK MAGAZYNOWY========================"<<endl; //jak starczy czasu zrobic zapis i odczyt z pliku parametru 'y'
        cout<<"\t\t\t\t\t\t1. 3 kapsulki\n";
        cout<<"\t\t\t\t\t\t2. 5 kapsulek\n";
        cout<<"\t\t\t\t\t\t3. Cofnij\n\n";
        cout<<"\t\t\t========================================================================="<<endl;
        e=getch();
        if(watchdog(StartTime)> limit)
        {
            w = false;
            return;
        }
        switch(e)
        {
        case '1':
            system("cls");
            cout<<"\t\t\t\t\t\tWybrano zestaw 3 kapsulek\n";
            if (y == 0) {y =3; cout<<"\t\t\t\t\t\tWlozono "<<y<<" kapsulki\n"; }
            else {cout <<"\t\t\t\t Operacja niedostepna, w zmywarce jest jeszcze: " <<y<< " kapsulek\n";}
            getch();
            return;
            break;
        case '2':
            system("cls");
            cout<<"\t\t\t\t\t\tWybrano zestaw 5 kapsulk\n";
            if (y == 0) {y =5; cout<<"\t\t\t\t\t\tWlozono "<<y<<" kapsulek\n";}
            else {cout <<"\t\t\t\tOperacja niedostepna, w zmywarce jest jeszcze: " <<y<< " kapsulek\n";}
            getch();
            return;
            break;
        case '3':
            break;
        default:
        StartTime = GetTickCount();
        cout<<"\t\t\t\t\t\tNieprawidlowy znak\n";
        getch();
        break;
        }
        }while(e!=3);
        break;
    case '2':
        char f;
        StartTime = GetTickCount();
        do{
        system("cls");
        cout<<"\t\t\t======================WYBIERZ ZASOBNIK JEDNORAZOWY========================\n";
        cout<<"\t\t\t\t\t\t1. Plyn do mycia wstepnego\n";
        cout<<"\t\t\t\t\t\t2. Kapsulka\n";
        cout<<"\t\t\t\t\t\t3. Cofnij\n";
        cout<<"\t\t\t\t\t\t4. Przejdz dalej\n\n";
        cout<<"\t\t\t========================================================================="<<endl;
        f=getch();
        if(watchdog(StartTime)> limit)
        {
            w = false;
            return;
        }
        switch(f)
        {
        case '1':
            system("cls");
            cout<<"\t\t\t\t\t\tWybrano plyn do mycia wstepnego\n";
            x =1;
            cout<<"\t\t\t\t\t\tWlano plyn do mycia wstepnego\n";
            getch();
            return;
            break;
        case '2':
            system("cls");
            cout<<"\t\t\t\t\t\tWybralno kapsulke\n";
            if (y == 0)
                {
                    y = 1;
                    cout<<"\t\t\t\t\t\tWlozono "<<y<<" kapsulke\n";
                }
            else {cout <<"\t\t\t\tOperacja niedostepna, w zmywarce jest jeszcze: " <<y<< " kapsulek\n";}
            return;
            getch();
            break;
        case '3':
            break;
        case '4':
            return;
        default:
        StartTime = GetTickCount();
        cout<<"\t\t\t\t\t\tNieprawidlowy znak, wpisz ponownie:\n";
        getch();
        break;
        }
        }while(f!='3');
        break;
    case '3':
        return;
        break;
    default:
        StartTime = GetTickCount();
        cout<<"\t\t\t\t\t\tNieprawidlowy znak,wpisz ponownie:\n "<<endl;
        break;
    }
    }while(c!='3');
}
void time_k(int hours, int minutes, int seconds, tryb& krotki, int t_)
{
    int poczatek = GetTickCount();
    int czas = t_*60*10; //czas w sek bedzie odliczany przeskalowany
    for(;;)
    {
        system("cls");
        cout<<"TRYB KROTKI\t\n";
        cout<<"\t\t\t\t\t\tTemperatura: " <<krotki.Zasadnicze.temp<<" stopni Celcjusza\n";
        cout<< "\t\t\t\t\t\tProgram:\n Zmoczenie: "<<krotki.Zmoczenie.czas<<" min\n \t\t\t\t\t\tMycie zasadnicze: "<<krotki.Zasadnicze.czas<< " min\n";
        cout<< " \t\t\t\t\t\tPlukanie: "<< krotki.Plukanie.czas<< " min\n\n TRWA: \n";
        int time =  watchdog(poczatek);
        if(time > czas ) return;
        else if(time < krotki.Zmoczenie.czas*60*10) cout<<"\t\t\t\t\t\tMoczenie naczyn\n";
        else if(time <= (t_- krotki.Plukanie.czas)*60*10 && (time > krotki.Zmoczenie.czas*60*10))
            {cout<<"\t\t\t\t\t\tMycie zasadnicze\n";}
        else if (time > (krotki.Zmoczenie.czas + krotki.Zasadnicze.czas)*60*10)cout<<"\t\t\t\t\t\tPlukanie\n";
        cout<<"\t\t\t\t\t\tDo konca pozostalo: "<<(czas - time)/60/10<<"min"<<endl;
    }
}


void timer_k (int hours, int minutes, int seconds, tryb& krotki, int t_) //timer mycia krotkiego
{
    int koniec;
    for(;;)
    {

        if(hours == 0 && minutes==0 && seconds ==0) break;
        if(minutes == 0 && seconds==0)
        {
            minutes = 60;
            hours--;
        }
        if(seconds ==0)
        {
            seconds = 60;
            minutes--;
        }
        system("cls");
        koniec =  hours*60 + minutes;
        cout<<"\t\t\t===============================TRYB KROTKI===============================\n";
        cout<<"\t\t\t\t\t\tTemperatura: " <<krotki.Zasadnicze.temp<<" stopni Celcjusza\n";
        cout<< "\t\t\t\t\t\tProgram:\n \t\t\t\t\t\tZmoczenie: "<<krotki.Zmoczenie.czas<<" min\n \t\t\t\t\t\tMycie zasadnicze: "<<krotki.Zasadnicze.czas<< " min\n";
        cout<< "\t\t\t\t\t\tPlukanie: "<< krotki.Plukanie.czas<< " min\n\n \t\t\t\t\t\tTRWA: \n";
        if(koniec >= (t_- krotki.Zmoczenie.czas)) {cout<<"\t\t\t\t\t\tMoczenie naczyn\n";}
        if(koniec < (t_- krotki.Zmoczenie.czas) && (koniec > ( t_ -(krotki.Zmoczenie.czas + krotki.Zasadnicze.czas))))
            {cout<<"\t\t\t\t\t\tMycie zasadnicze\n";}
        if (koniec <= (t_- krotki.Zmoczenie.czas - krotki.Zasadnicze.czas))cout<<"\t\t\t\t\t\tPlukanie\n";
        cout<<"\t\t\t\t\t\tDo konca pozostalo: "<<hours<<":"<<minutes<<":"<<seconds--<<endl<<endl;
        cout<<"\n\t\t\t======================================================================"<<endl;

        Sleep(1); //przyspieszone dla sprawdzenia symulacji, w czasie rzeczywistym dac 1000ms->1s
    }
}
void timer_s (int hours, int minutes, int seconds, tryb& standardowy, int t_) //timer mycia standardowego
{
    int koniec;
    for(;;)
    {
        if(hours == 0 && minutes==0 && seconds ==0) break;
        if(minutes == 0 && seconds==0)
        {
            minutes = 60;
            hours--;
        }
        if(seconds ==0)
        {
            seconds = 60;
            minutes--;
        }
        system("cls");
        koniec =  hours*60 + minutes;
        cout<<"\t\t\t============================TRYB STANDARDOWY=============================\n";
        cout<<"\t\t\t\t\t\tTemperatura: " <<standardowy.Zasadnicze.temp<<" stopni Celcjusza\n";
        cout<< "\t\t\t\t\t\tProgram:\n \t\t\t\t\t\tZmoczenie "<<standardowy.Zmoczenie.czas<<" min\n \t\t\t\t\t\tMycie zasadnicze: "<<standardowy.Zasadnicze.czas<< " min\n";
        cout<< "\t\t\t\t\t\tPlukanie: "<< standardowy.Plukanie.czas<< " min\n\t\t\t\t\t\tSuszenie: "<<standardowy.Suszenie.czas << " min\n\n \t\t\t\t\t\tTRWA: \n";
        if(koniec >= (t_- standardowy.Zmoczenie.czas)) {cout<<"\t\t\t\t\t\tMoczenie naczyn\n";}
        if(koniec < (t_- standardowy.Zmoczenie.czas) && (koniec >  (t_ -(standardowy.Zmoczenie.czas + standardowy.Zasadnicze.czas))))
            {cout<<"\t\t\t\t\t\tMycie zasadnicze\n";}
        if((koniec <= (standardowy.Plukanie.czas + standardowy.Suszenie.czas)) && (koniec > standardowy.Suszenie.czas))cout<<"\t\t\t\t\t\tPlukanie\n";
        if(koniec <= (standardowy.Suszenie.czas))cout<<"\t\t\t\t\t\tSuszenie\n";
        cout<<"\t\t\t\t\t\tDo konca pozostalo: "<<hours<<":"<<minutes<<":"<<seconds--<<endl;
        cout<<"\n\t\t\t======================================================================"<<endl;
        Sleep(1); //przyspieszone dla sprawdzenia symulacji, w czasie rzeczywistym dac 1000ms->1s
    }
}
void timer_dodatkowy (int hours, int minutes, int seconds, tryb& dodatkowy, int t_, int tryb) //timery trybow dodatkowych
{
    int koniec;
    for(;;)
    {
        if(hours == 0 && minutes==0 && seconds ==0) break;
        if(minutes == 0 && seconds==0)
        {
            minutes = 60;
            hours--;
        }
        if(seconds == 0)
        {
            seconds = 60;
            minutes--;
        }
        system("cls");
        koniec =  hours*60 + minutes;
        if (tryb == 3 || tryb == 5)
        {
            if(tryb == 3) cout<<"\t\t\t===================TRYB KROTKI + MYCIE WSTEPNE=================\n";
            if(tryb == 5) cout<<"\t\t\t==================TRYB STRANDARDOWY + MYCIE WSTEPNE============\n";
            if(koniec >= (t_ - dodatkowy.Zmoczenie.czas)) cout<<"\t\t\t\t\t\tTrwa moczenie naczyn \n\t\t\t\t\t\tTemperatura: "<<dodatkowy.Zmoczenie.temp<<" stopni\n";
            if((koniec < t_- dodatkowy.Zmoczenie.czas)&&(koniec >= t_ - (dodatkowy.Wstepne.czas + dodatkowy.Zmoczenie.czas)))
               cout<<"\t\t\t\t\t\tMycie wstepne \n\t\t\t\t\t\tTemperatura: "<<dodatkowy.Wstepne.temp <<" stopni\n";
            if((koniec <( t_-(dodatkowy.Wstepne.czas+dodatkowy.Zmoczenie.czas)))&&(koniec >= (t_-(dodatkowy.Wstepne.czas + dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas))))
            cout <<"\t\t\t\t\t\tZasadnicze\n\t\t\t\t\t\tTemperatura: "<<dodatkowy.Zasadnicze.temp <<"stopni\n";
            if((koniec < t_ -(dodatkowy.Wstepne.czas + dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas ))&& (koniec >= (t_ -(dodatkowy.Wstepne.czas + dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas+dodatkowy.Plukanie.czas))))
                cout<<"\t\t\t\t\t\tPlukanie\n\t\t\t\t\t\tTemperatura: "<<dodatkowy.Plukanie.temp <<"stopni\n";
            if(koniec < t_ -(dodatkowy.Wstepne.czas + dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas + dodatkowy.Plukanie.czas))
                cout<<"\t\t\t\t\t\tSuszenie\n\t\t\t\t\t\tTemperatura: "<<dodatkowy.Suszenie.temp <<"stopni\n";

        }
        else if(tryb == 4 || tryb == 6)
        {
            if(tryb == 4) cout<<"\t\t\t====================TRYB KROTKI + ZIMNE PLUKANIE===================\n";
            if(tryb == 6) cout<<"\t\t\t===================TRYB STRANDARDOWY + ZIMNE PLUKANIE==============\n";
            cout<<"\t\t\t\t\t\tTRWA: \n";
            if(koniec >= (t_ - dodatkowy.Zmoczenie.czas)) cout<<"\t\t\t\t\t\tTrwa moczenie  \n\t\t\t\t\t\tTemperatura: "<<dodatkowy.Zmoczenie.temp<<" stopni\n";
            if((koniec <( t_-(dodatkowy.Zmoczenie.czas)))&&(koniec >= (t_-(dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas))))
            cout <<"\t\t\t\t\t\tZasadnicze\n\t\t\t\t\t\tTemperatura: "<<dodatkowy.Zasadnicze.temp <<" stopni\n";
            if((koniec < t_ -(dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas ))&& (koniec >= (t_ -(dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas+dodatkowy.Plukanie.czas))))
                cout<<"\t\t\t\t\t\tPlukanie\n\t\t\t\t\t\tTemperatura: "<<dodatkowy.Plukanie.temp <<" stopni\n";
            if((koniec < t_ -(dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas+dodatkowy.Plukanie.czas))&&(koniec >= t_-(dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas + dodatkowy.Plukanie.czas+ dodatkowy.Plukanie_na_zimno.czas)))
            cout<<"\t\t\t\t\t\tPlukanie na zimno \n\t\t\t\t\t\tTemperatura: "<<dodatkowy.Plukanie_na_zimno.temp<<" stopni\n";
            if((koniec < (t_-(dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas + dodatkowy.Plukanie.czas+ dodatkowy.Plukanie_na_zimno.czas))))
            cout<<"\t\t\t\t\t\tSuszenie \n\t\t\t\t\t\tTemperatura: "<<dodatkowy.Suszenie.temp<<" stopni\n";
        }
        cout<<"\t\t\t\t\t\tDo konca pozostalo: "<<hours<<":"<<minutes<<":"<<seconds--<<"\n\n";
        cout<<"\n\t\t\t======================================================================"<<endl;
        Sleep(1); //przyspieszone dla sprawdzenia symulacji, w czasie rzeczywistym dac 1000ms->1s
    }
}

void uruchom(int t_, int tryb_, tryb& krotki,tryb& standardowy, tryb& dodatkowy) //wywolanie timerow
{
    int h = int(t_/60);
    char c;
    do{
    cout<< "\t\t\t\t\t\tBy rozpoczac wcisnij 'y', cofnac 'b'\n";
    cin>>c;
    switch(c)
    {
    case 'y':
        if (tryb_ == 1){timer_k(h,t_%60,0,krotki,t_);}
        else if (tryb_ == 2){timer_s(h,t_%60,0,standardowy,t_);}
        else if (tryb_ > 2){timer_dodatkowy(h,t_%60,0,dodatkowy,t_,tryb_);}
        cout<<"\t\t\t\t\t\tZmywanie zakonczone"<<endl;
        for (int i = 100; i< 400 ; i = i + 50)
            Beep(i,1000); //sygnalizacja dzwiekowa o zakonczeniu mycia
        getch();
        return;
    case 'b':
        break;
    default:
        cout<<"\t\t\t\t\t\tNieprawidlowy znak, wprowadz ponownie\n";
    }
    }while(c!='b');
}

void change_temp(int z,tryb& krotki,tryb& standardowy,tryb& dodatkowy,int limit,bool& w) //zmiana temperatury
{
    int StartTime = GetTickCount();
    int c;
    char x;
    do{
    cout<<"\t\t\t============================ZMIEN TEMPERATURE=============================="<<endl;
    cout<<"\t\t\t\t\tWpisz numer pozycji wybranej temperatury \n";
    cout<<"\t\t\t\t\t\t\t1. 35 stopni\n \t\t\t\t\t\t\t2. 40 stopni\n \t\t\t\t\t\t\t3. 45 stopni \n \t\t\t\t\t\t\t4. 50 stopni\n \t\t\t\t\t\t\t5. 55 stopni\n \t\t\t\t\t\t\t6. 60 stopni\n \t\t\t\t\t\t\t7. 65 stopni\n \t\t\t\t\t\t\t8. 70 stopni\n"<<endl;
    cout<<"\n\t\t\t======================================================================"<<endl;

    x= getch();
    if(watchdog(StartTime) > limit)
    {
        w = false;
        return;
    } else{
    switch (x)
        {
        case '1':
            c = 35;
            break;
        case '2':
            c = 40;
            break;
        case '3':
            c =45;
            break;
        case '4':
            c = 50;
            break;
        case '5':
            c=55;
            break;
        case '6':
            c=60;
            break;
        case '7':
            c=65;
            break;
        case '8':
            c=70;
            break;
        default:
            system("cls");
            //StartTime = GetTickCount();
            cout<<"\t\t\tNieprawidlowy znak, wpisz ponownie:"<<endl;
            break;
        }
    }
    }while((x != '1') && (x !='2') && (x !='3') && (x !='4') && (x !='5') && (x !='6') && (x !='7') && (x !='8'));
        if(z == 1)
        {
            krotki.zmien_temp_krotki(c);
            cout << "\t\t\t\t\tNowa temperatura zmywania: "<< krotki.Zasadnicze.temp<<endl;
        }
        if(z == 2)
        {
            standardowy.zmien_temp_standardowy(c);
            cout << "\t\t\t\t\tNowa temperatura zmywania: "<< standardowy.Zasadnicze.temp<<endl;
        }
        if(z > 2)
        {
            dodatkowy.zmien_temp_dodatkowy(c);
            cout << "\t\t\t\t\tNowa temperatura zmywania: " << dodatkowy.Zasadnicze.temp<<endl;
        }
        cout<<"\t\t\t\t\tWcisnij dowolny przycisk by kontynuowac"<<endl;
        getch();
        return;
}
void menu(int iPozycja)
{   system("cls");
    cout<<"\t\t\t================================ZMYWARKA================================"<<endl;
    cout<< "\t\t\t\t\t\tWybierz tryb pracy\n";
    cout << "\t\t\t\t\t\t1" << ((iPozycja == 1) ? "*" : ".") << "Tryb krotki" << endl;
    cout << "\t\t\t\t\t\t2" << ((iPozycja == 2) ? "*" : ".") << "Tryb standardowy" << endl;
    cout << "\t\t\t\t\t\t3" << ((iPozycja == 3) ? "*" : ".") << "Dodatkowy" << endl;
  	cout << "\t\t\t\t\t\t4" << ((iPozycja == 4) ? "*" : ".") << "Wylacz zmywarke" << endl;
    cout << "\t\t\t\t\t\t5" << ((iPozycja == 5) ? "*" : ".") << "Wlacz blokade ekranu" << endl;
  	//cout<<endl<<"\t\t\t\t<Zmien pozycje: strzala w gore/dol lub, wybierz: enter>"<<endl;
    cout<<"\t\t\t======================================================================"<<endl;

}
void krotki_f(int tryb_, tryb& krotki,tryb& standardowy, tryb& dodatkowy,int t,int limit, int plyn, int kapsulka, int& mycie)
{
    bool wykonaj = true;
    char a;
    int StartTime = GetTickCount();
    do{
    system("cls");
    cout << "\t\t\t===============================TRYB KROTKI===============================" << endl;
    int t = krotki.Zmoczenie.czas + krotki.Zasadnicze.czas + krotki.Plukanie.czas;
    cout << "\t\t\t\t\t\tCzas trwania: "<< int(t/60)<<" h " << (t%60)<<" min" << endl;
    cout << "\t\t\t\t\t\tDomyslna temperatura: 50 stopni Celcjusza"<<endl;
    cout<<"\t\t\t========================================================================="<<endl;
    cout << "\t\t\t\t\t\tProgram:\n \t\t\t\t\t\t zmoczenie\n \t\t\t\t\t\t zmywanie zasadnicze\n\t\t\t\t\t\t plukanie\n"<<endl;
    cout << endl;
    cout << "\t\t\t  By zmienic temperature wpisz: y, jesli nie i kontynuowac : n, cofnac: b" <<endl;
    cout<<"\t\t\t========================================================================="<<endl;
    a= getch();
    if(watchdog(StartTime) > limit)
    {
        return;
    }
    else{
    switch (a)
     {
         case 'y':
            system("cls");
            change_temp(tryb_,krotki,standardowy,dodatkowy,limit,wykonaj); //zmiana temperatury
            if(wykonaj == false) return;
            while(true){
            det(plyn, kapsulka, wykonaj,limit); //wybor detergentu
            if(wykonaj == false) return;
            if(kapsulka > 0)
            {
                kapsulka--;
                mycie++;
                zapisz(plyn,kapsulka,mycie);
                uruchom(t,tryb_,krotki,standardowy,dodatkowy); //rozpoczecie zmywania
                cout<<"Nacisnij dowolny przycisk by wylaczyc"<<endl;
                return;
            }
            else {cout<<"Nie dodano kapsulki, wybierz zasobnik"<<endl; getch();}
            }
            break;
        case 'n':
            system("cls");
            krotki.zmien_temp_krotki(50); //domyslna temperatura
            while(true){
            det(plyn, kapsulka, wykonaj, limit);
            if(wykonaj == false) return;
            if(kapsulka > 0)
            {
                kapsulka--;
                mycie++;
                zapisz(plyn,kapsulka,mycie);
                uruchom(t,tryb_,krotki,standardowy,dodatkowy); //rozpoczecie zmywania
                cout<<"Nacisnij dowolny przycisk by wylaczyc"<<endl;
                return;
            }
            else {cout<<"Nie dodano kapsulki, wybierz zasobnik"<<endl; getch();}
            }
            break;
        case 'b':
            break;
        default:
            cout<<"Bledny parametr, wybierz ponownie:"<<endl;
            StartTime = GetTickCount();
            break;
     }
     }
     }while(a != 'b');
}
void standardowy_f(int tryb_, tryb& krotki,tryb& standardowy, tryb& dodatkowy,int t,int limit, int plyn, int kapsulka, int& mycie)
{
    bool wykonaj = true;
    int StartTime = GetTickCount();
    char b;
    do{
    system("cls");
    cout << "\t\t\t===============================TRYB STANDARDOWY===============================" << endl;
    t = standardowy.Zmoczenie.czas + standardowy.Zasadnicze.czas + standardowy.Plukanie.czas + standardowy.Suszenie.czas;
    cout << "\t\t\t\t\t\tCzas trwania:"<< int(t/60)<< " h " << t%60 <<" min" << endl;
    cout << "\t\t\t\t\t\tDomyslna temperatura: 50 stopni Celcjusza"<<endl;
    cout<<"\t\t\t========================================================================="<<endl;
    cout << "\t\t\t\t\t\tProgram:\n\t\t\t\t\t\t zmoczenie\n\t\t\t\t\t\t zmywanie zasadnicze\n\t\t\t\t\t\t plukanie\n\t\t\t\t\t\t suszenie\n"<<endl;
    cout << endl;
    cout << "\t\t\tBy zmienic temperature wpisz: y, jesli nie i kontynuowac: n, cofnac: b" <<endl;
    cout<<"\t\t\t========================================================================="<<endl;
    b=getch();
    if(watchdog(StartTime) > limit)
    {
        return;
    }
    else{
    switch (b)
     {
         case 'y':
            system("cls");
            change_temp(tryb_,krotki,standardowy,dodatkowy,limit,wykonaj);
            cout<<endl;
            if(wykonaj == false) return;
            while(true){
            det(plyn, kapsulka, wykonaj,limit); //wybor detergentu
            if(wykonaj == false) return;
            if(kapsulka > 0)
            {
                kapsulka--;
                mycie++;
                zapisz(plyn,kapsulka, mycie);
                uruchom(t,tryb_,krotki,standardowy,dodatkowy); //rozpoczecie zmywania
                cout<<"Nacisnij dowolny przycisk by wylaczyc"<<endl;
                return;
            }
            else {cout<<"Brak kapsulki, wybierz ponownie"<<endl; getch();}
            }
            break;
        case 'n':
            system("cls");
            standardowy.zmien_temp_standardowy(50);
            while(true){
            det(plyn, kapsulka, wykonaj,limit); //wybor detergentu
            if(wykonaj == false) return;
            if(kapsulka > 0)
            {
                kapsulka--;
                mycie++;
                zapisz(plyn,kapsulka,mycie);
                uruchom(t,tryb_,krotki,standardowy,dodatkowy); //rozpoczecie zmywania
                cout<<"Nacisnij dowolny przycisk by wylaczyc"<<endl;
                return;
            }
            else {cout<<"Brak kapsulki, wybierz ponownie"<<endl; getch();}
            }
            break;
        case 'b':
            break;
        default:
            cout<<"Błędny parametr, wpisz ponownie:"<<endl;
            break;
     }
    }
    }while(b != 'b');
}

void dodatkowy_f(int tryb_, tryb& krotki,tryb& standardowy, tryb& dodatkowy,int t,int limit, int plyn, int kapsulka, int& mycie)
{
    bool wykonaj  = true;
    int StartTime = GetTickCount();
    char i;
    char d;
    do{
    system("cls");
    cout << "\t\t\t==============================TRYBY DODATKOWE==============================" << endl;
    cout << "\t\t\t\t\t\t1. Tryb krotki + mycie wstepne\n";
    cout << "\t\t\t\t\t\t2. Tryb krotki + plukanie na zimno\n";
    cout << "\t\t\t\t\t\t3. Tryb standardowy + mycie wstepne\n";
    cout << "\t\t\t\t\t\t4. Tryb standardowy + plukanie na zimno\n";
    cout << "\t\t\t\t\t\t5. Cofnij\n";
    cout<< "\n\t\t\t\t\t\tWybierz tryb"<<endl<<endl;
    cout<<"\t\t\t========================================================================="<<endl;
    i = getch();
    if(watchdog(StartTime) > limit)
    {
        return;
    }
    switch(i)
    {
    case '1':
        tryb_ = 3;
        t = dodatkowy.Wstepne.czas + dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas + dodatkowy.Plukanie.czas;
        cout << "\t\t\t\t\t\tCzas trwania:"<< int(t/60)<<" h "<<t%60 <<" min" << endl;
        dodatkowy.zmien_temp_dodatkowy(50);
        cout << "\t\t\t\t\t\tDomyslna temperatura: "<<dodatkowy.Zasadnicze.temp << endl;
        break;
    case '2':
        tryb_ = 4;
        t = dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas + dodatkowy.Plukanie.czas + dodatkowy.Plukanie_na_zimno.czas;
        cout << "\t\t\t\t\t\tCzas trwania:"<< int(t/60)<<" h "<<t%60 <<" min" << endl;
        dodatkowy.zmien_temp_dodatkowy(50);
        cout << "\t\t\t\t\t\tDomyslna temperatura: "<<dodatkowy.Zasadnicze.temp << endl;
        break;
    case '3':
        tryb_ = 5;
        t = dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas + dodatkowy.Plukanie.czas + dodatkowy.Wstepne.czas + dodatkowy.Suszenie.czas;
        cout << "\t\t\t\t\t\tCzas trwania: "<< int (t/60) <<" h "<< t%60 <<" min" << endl;
        dodatkowy.zmien_temp_dodatkowy(50);
        cout << "\t\t\t\t\t\tDomyslna temperatura: "<<dodatkowy.Zasadnicze.temp << endl;
        break;
    case '4':
        tryb_ = 6;
        t = dodatkowy.Zmoczenie.czas + dodatkowy.Zasadnicze.czas + dodatkowy.Plukanie.czas + dodatkowy.Plukanie_na_zimno.czas +dodatkowy.Suszenie.czas;
        cout << "\t\t\t\t\t\tCzas trwania: "<< int(t/60)<<" h "<<t%60 <<" min" << endl;
        dodatkowy.zmien_temp_dodatkowy(50);
        cout << "\t\t\t\t\t\tDomyslna temperatura: "<<dodatkowy.Zasadnicze.temp << endl;
        break;
    case '5':
        //return;
        break;
    default:
        StartTime = GetTickCount();
        cout<<"\t\t\t\t\t\tBledny parametr, wpisz ponownie:"<<endl;
        break;
    }
    }while((i!= '1') && (i!='2') && (i!='3') && (i != '4') && (i!='5'));
    if(tryb_ !=0)
        {   StartTime = GetTickCount();
            cout << "\t\tBy zmienic temperature wpisz: y, jesli nie i kontynuowac: n, cofnac: b" << endl;
            d = getch();
            if(watchdog(StartTime) > limit)
            {
                return;
            }
        }
    switch(d)
{
case 'y':
    system("cls");
    change_temp(tryb_,krotki,standardowy,dodatkowy,limit,wykonaj);
    cout<<endl;
    if(wykonaj == false) return;
    while(true){
    det(plyn, kapsulka, wykonaj,limit); //wybor detergentu
    if(wykonaj == false) return;
    if((kapsulka > 0)&&((tryb_ == 4)||(tryb_ == 6)))
    {
        kapsulka--;
        mycie++;
        zapisz(plyn,kapsulka,mycie);
        uruchom(t,tryb_,krotki,standardowy,dodatkowy); //rozpoczecie zmywania
        cout<<"Nacisnij dowolny przycisk by wylaczyc"<<endl;
        return;
    }
    else if(((tryb_ == 3) || (tryb_ ==5)) && (kapsulka > 0))
    {
        if(plyn > 0)
        {
            kapsulka--;
            plyn--;
            mycie++;
            zapisz(plyn,kapsulka,mycie);
            uruchom(t,tryb_,krotki,standardowy,dodatkowy); //rozpoczecie zmywania
            cout<<"Nacisnij dowolny przycisk by wylaczyc"<<endl;
            return;
        }
        else
        {
            cout<<"Brak plynu do mycia wstepnego, wybierz ponownie"<<endl;
            getch();
        }
    }
    if(kapsulka == 0) {cout<<"Brak kapsulki, wybierz ponownie"<<endl; getch();}
    }
    break;
case 'n':
    while(true){
    det(plyn, kapsulka, wykonaj,limit); //wybor detergentu
    if(wykonaj == false) return;
    if((kapsulka > 0)&&((tryb_ == 4)||(tryb_ ==6)))
    {
        kapsulka--;
        mycie++;
        zapisz(plyn,kapsulka, mycie);
        uruchom(t,tryb_,krotki,standardowy,dodatkowy); //rozpoczecie zmywania
        return;
    }
    else if(((tryb_ == 3) || (tryb_ ==5)) && (kapsulka > 0))
    {
        if(plyn > 0)
        {
            kapsulka--;
            plyn--;
            mycie++;
            zapisz(plyn,kapsulka,mycie);
            uruchom(t,tryb_,krotki,standardowy,dodatkowy); //rozpoczecie zmywania
            return;
        }
        else
        {
            cout<<"Brak plynu do mycia wstepnego, wybierz ponownie"<<endl;
            getch();
        }
    }
    if(kapsulka == 0) {cout<<"Brak kapsulki, wybierz ponownie"<<endl; getch();}
    }
    break;
case 'b':
    break;
default:
        StartTime = GetTickCount();
        cout<<"Bledny parametr"<<endl;
        break;
}
}
void czyszczenie(int& plyn,int& kapsulka, int& mycie, int& znak2)
{
    ifstream myfile;
    if(mycie==3)
    {
        cout<<"Zmywarka wymaga czyszczenia"<<endl;
        cout<<"Czy chcesz teraz ja oczyscic? \nJesli tak, wpisz 'y', by zignorowac wcisnij 'n'"<<endl;
        char c;
        cin>>c;
        switch(c)
        {
        case 'y':
            mycie = 0;
            zapisz(plyn,kapsulka,mycie);
            myfile.open("zasoby.txt");
            myfile >>plyn>>kapsulka>>mycie;
            myfile.close();
            getch();
            break;
        case 'n':
            break;
        }
    }
    else if( mycie > 5)
    {
        cout<<"Zmywarka zostala uszkodzona\n";
        cout<<" Aby naprawic wcisnij 'y', aby wylaczyc 'n'"<<endl;
        char d;
        int czaas;
        cin>>d;
        switch(d)
        {
        case 'y':
            czaas = GetTickCount();
            do{
                system("cls");
                cout<<"Trwa naprawa, prosze czekac"<<endl;
                if(watchdog(czaas)>=5000) //w ms
                {
                    cout<<"Naprawa przebiegla pomyslnie, nacisnij dowolny klawisz by kontynuowac"<<endl;
                    mycie = 0;
                    zapisz(plyn,kapsulka,mycie);
                    myfile.open("zasoby.txt");
                    myfile >>plyn>>kapsulka>>mycie;
                    myfile.close();
                    getch();
            }}while(mycie!= 0);
            break;
        case 'n':
            znak2 =1;
            return;
            break;
        }
    }

}
int main()
{
    int limit = 10*1000; //w ms
    ////////////Odczyt zasobów z pliku////////////////
    int kapsulka = 0;
    int plyn = 0;
    int mycie = 0;
    ifstream myfile;
    myfile.open("zasoby.txt");
    myfile >>plyn>>kapsulka>>mycie;
    myfile.close();
    /////////////////////////////////////////////////
    tryb krotki,standardowy,dodatkowy;     //inicjalizacja atrybutów klasy
    int t;
    string r;
    int tryb_ = 0; //numer trybu krotki,standardowy, i kolejno dodatkowych itd
	int znak = -1; //znaki do obslugi menu glownego
    int znak2 = 0;
    czyszczenie(plyn,kapsulka,mycie,znak2);
    int PozycjaMenu = 1;
    menu(PozycjaMenu);
    while (true)
    {
        if (_kbhit())
            znak = _getch();
        if (znak != -1)
        {
            switch (znak)
            {
            case '1':
                 tryb_ = 1;
                 krotki_f(tryb_,krotki,standardowy,dodatkowy,t,limit,plyn,kapsulka,mycie);
                 menu(PozycjaMenu);
                 znak = -1;
                 break;
            case '2':
                tryb_ = 2;
                standardowy_f(tryb_,krotki,standardowy,dodatkowy,t,limit,plyn,kapsulka,mycie);
                menu(PozycjaMenu);
                znak = -1;
                break;
            case '3':
                dodatkowy_f(tryb_,krotki,standardowy,dodatkowy,t,limit,plyn,kapsulka,mycie);
                getch();
                menu(PozycjaMenu);
                znak = -1;
            	break;
            case '4':
                cout << "Nacisnij dowolny klawisz, aby zakonczyc program"<< endl;
                znak2 = 1;
                break;
            case '5':
                do{
                    system("cls");
                    cout<<"Blokada klawiatury wlaczona"<<endl;
                    cout<<"By wylaczyc blokade pisz: 1532 "<<endl;
                    cin>>r;
                }while(r != "1532");
                cout<<"Blokada wylaczona\nNacisnij dowolny klawisz by wrocic do menu glownego"<<endl;
                getch();
                menu(PozycjaMenu);
                znak = -1;
                break;
    // ENTER i klawisze steruj1ce
            case 13:
                znak = '1'+ PozycjaMenu-1;
                break;
            case 224: //klawisz sterujacy
                znak = _getch();
                switch (znak)
                {
                case 80: //klawisz dó³
                    if (PozycjaMenu < L_MENU)
                        PozycjaMenu++;
                    break;
                case 72: //klawisz góra
                    if (PozycjaMenu > 1)
                        PozycjaMenu--;
                    break;
                default:
                    cout << "224."<< znak << ":" << (char)znak << endl;
                }
    // koniec klawiszy steruj1cych
                menu(PozycjaMenu);
                znak = -1;
                break;
            default:
                cout << znak <<":"<<(char)znak<< endl;
                cout << "Nieprawidlowy przycisk!" << endl;
                znak = -1;
            }
        }
        if(znak2==1)
    	{
    		break;
		}
	}
    return 0;
}
