-- -----------------------------------------------
-- ANALIZA BAZY DANYCH O STUDENTACH W USA
-- -----------------------------------------------

-- 1. procentowy podział na szkoły prywatne non-profit, publiczne, prywatne forprofit
SELECT CONTROL,
count(CONTROL)/(select count(*) from sakila.`most-recent-field-data-elements_`)*100 as Prc 
FROM sakila.`most-recent-field-data-elements_`
group by CONTROL;

-- -----------------------------------------------
-- 2. liczba uniwersytetów i college'ow w USA
drop table univer;
select * from univer;
create table univer
(university_name TEXT,
num INT);

insert into univer values (
"University",
(SELECT count(INSTNM) as University FROM sakila.`most-recent-field-data-elements_`
WHERE INSTNM like "%University%"));

insert into univer values (
"College",
(SELECT count(INSTNM) as University FROM sakila.`most-recent-field-data-elements_`
WHERE INSTNM like "%College%"));
select * from univer;

-- -----------------------------------------------
-- 3. największy średni dług federalny pożyczkobiorców kończoncych studia  w dollarach, 5 uczelni
create table debt
(school TEXT,
debt_mean INT);
drop table debt;

delete from sakila.`most-recent-field-data-elements_`
where DEBTMEAN like "PrivacySuppressed";

select DEBTMEAN from sakila.`most-recent-field-data-elements_`
where DEBTMEAN != 'PrivacySuppressed';

-- -----------------------------------------------
-- 4. porównanie mediany zarobków i długu po ukończeniu danego kierunku
-- wykres kwoty w dollarach w funkcji poziomów edukacji  typu inz, mgr itd na kierunku chemistry

select CREDDESC, (max(DEBTMEAN) + min(DEBTMEAN))/2, min(MD_EARN_WNE),CIPDESC from sakila.`most-recent-field-data-elements_`
group by CREDDESC
having CIPDESC like "Chemistry" and DEBTMEAN not like "PrivacySuppressed" and MD_EARN_WNE not like "PrivacySuppressed";

-- -----------------------------------------------
-- 5. porównanie mediany zarobków bachelor, master, doctor w dollarach
select CREDDESC, median(DEBTMEAN), median(MD_EARN_WNE) from sakila.`most-recent-field-data-elements_`
group by CREDDESC;

-- -----------------------------------------------
-- 6. podział na kampus główny i uczelnie poza nim na przedmiocie Chemistry
create table campus
(campus_name TEXT,
num INT);
insert into campus values (
"Kampus główny",
(SELECT count(MAIN) as campus_ FROM sakila.`most-recent-field-data-elements_`
WHERE MAIN = 1));

insert into univer values (
"Poza kampusem głównym",
(SELECT count(MAIN) as campus_ FROM sakila.`most-recent-field-data-elements_`
WHERE INSTNM = 0));

-- -----------------------------------------------

