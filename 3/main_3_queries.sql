use psz_baza;

-- 2a)
-- grupisanje blokova Novog Beograda
select (CASE
    WHEN substring(substring_index(lokacija, ' (', 1), 10, 12) = 'Novi Beograd' THEN 'Novi Beograd'
    ELSE substring(substring_index(lokacija, ' (', 1), 10)
END) as 'Deo Beograda', count(*) as 'Broj nekretnina u ponudi'
from nekretnina
where substring_index(lokacija, ',', 1) = 'Beograd'
group by (CASE
    WHEN substring(substring_index(lokacija, ' (', 1), 10, 12) = 'Novi Beograd' THEN 'Novi Beograd'
    ELSE substring(substring_index(lokacija, ' (', 1), 10)
END)
order by count(*) desc
limit 10;
-- bez grupisanja blokova Novog Beograda
select substring(substring_index(lokacija, '(', 1), 9) as 'Deo Beograda', count(*) as 'Broj nekretnina u ponudi'
from nekretnina
where substring_index(lokacija, ',', 1) = 'Beograd'
group by substring(substring_index(lokacija, '(', 1), 9)
order by count(*) desc
limit 10;

-- 2b)
select (CASE
	WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 35 THEN '<= 35m²'
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 50 THEN '36m² - 50m²'
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 65 THEN '51m² - 65m²'
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 80 THEN '66m² - 80m²'
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 95 THEN '81m² - 95m²'
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 110 THEN '96m² - 110m²'
    ELSE '>= 111m²'
END) as 'Kvadratura', count(*) as 'Broj stanove ove kvadrature'
from nekretnina
where tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja'
group by (CASE
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 35 THEN '<= 35m²'
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 50 THEN '36m² - 50m²'
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 65 THEN '51m² - 65m²'
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 80 THEN '66m² - 80m²'
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 95 THEN '81m² - 95m²'
    WHEN truncate(convert(left(kvadratura, char_length(kvadratura)-3), signed integer), 0) <= 110 THEN '96m² - 110m²'
    ELSE '>= 111m²'
END);

-- 2c)
select (CASE
		WHEN godina_izgradnje NOT REGEXP '^-?[0-9]+$' THEN (CASE WHEN stanje_nekretnine = '' THEN 'Nepoznatno' ELSE stanje_nekretnine END)
    WHEN convert(godina_izgradnje, signed integer) <= 1950 THEN '<= 1950'
    WHEN convert(godina_izgradnje, signed integer) <= 1960 THEN '1951-1960'
    WHEN convert(godina_izgradnje, signed integer) <= 1970 THEN '1961-1970'
    WHEN convert(godina_izgradnje, signed integer) <= 1980 THEN '1971-1980'
    WHEN convert(godina_izgradnje, signed integer) <= 1990 THEN '1981-1990'
    WHEN convert(godina_izgradnje, signed integer) <= 2000 THEN '1991-2000'
    WHEN convert(godina_izgradnje, signed integer) <= 2010 THEN '2001-2010'
    WHEN convert(godina_izgradnje, signed integer) <= 2020 THEN '2011-2020'
    ELSE '>= 2021'
END) as 'Godina izgradnje/stanje objekta', count(*) as 'Broj nekretnina'
from nekretnina
group by (CASE
	WHEN godina_izgradnje NOT REGEXP '^-?[0-9]+$' THEN (CASE WHEN stanje_nekretnine = '' THEN 'Nepoznatno' ELSE stanje_nekretnine END)
    WHEN convert(godina_izgradnje, signed integer) <= 1950 THEN '<= 1950'
    WHEN convert(godina_izgradnje, signed integer) <= 1960 THEN '1951-1960'
    WHEN convert(godina_izgradnje, signed integer) <= 1970 THEN '1961-1970'
    WHEN convert(godina_izgradnje, signed integer) <= 1980 THEN '1971-1980'
    WHEN convert(godina_izgradnje, signed integer) <= 1990 THEN '1981-1990'
    WHEN convert(godina_izgradnje, signed integer) <= 2000 THEN '1991-2000'
    WHEN convert(godina_izgradnje, signed integer) <= 2010 THEN '2001-2010'
    WHEN convert(godina_izgradnje, signed integer) <= 2020 THEN '2011-2020'
    ELSE '>= 2021'
END);

-- 2d)
select substring_index(lokacija, ',', 1) as top_5_town, 
(select count(*) from nekretnina where substring_index(lokacija, ',', 1) = top_5_town and tip_ponude = 'Prodaja') as 'Broj nekrentina za prodaju',
(select count(*) from nekretnina where substring_index(lokacija, ',', 1) = top_5_town and tip_ponude = 'Izdavanje') as 'Broj nekrentina za iznajmljivanje',
count(*) as 'Ukupno nekretnina' 
from nekretnina 
where substring_index(lokacija, ',', 1) in (
	 select town from (
     select substring_index(lokacija, ',', 1) as town
	 from psz_baza.nekretnina b
     group by town
     order by count(*) desc
	 limit 5
     ) as c
)
group by top_5_town
order by count(*) desc;


-- 2e)
select (CASE
    WHEN truncate(convert(replace(left(cena, char_length(cena)-4), ' ', ''), signed integer), 0) <= 49999 THEN '<= 49999€'
    WHEN truncate(convert(replace(left(cena, char_length(cena)-4), ' ', ''), signed integer), 0) <= 99999 THEN '50000€ - 99999€'
    WHEN truncate(convert(replace(left(cena, char_length(cena)-4), ' ', ''), signed integer), 0) <= 149999 THEN '100000 - 149999€'
    WHEN truncate(convert(replace(left(cena, char_length(cena)-4), ' ', ''), signed integer), 0) <= 199999 THEN '150000€ - 199999€'
    ELSE '>= 200000€'
END) as 'Cenovni rang', count(*) as 'Broj nekretnina ovog cenovnog ranga'
from nekretnina
where tip_ponude = 'Prodaja'
group by (CASE
    WHEN truncate(convert(replace(left(cena, char_length(cena)-4), ' ', ''), signed integer), 0) <= 49999 THEN '<= 49999€'
    WHEN truncate(convert(replace(left(cena, char_length(cena)-4), ' ', ''), signed integer), 0) <= 99999 THEN '50000€ - 99999€'
    WHEN truncate(convert(replace(left(cena, char_length(cena)-4), ' ', ''), signed integer), 0) <= 149999 THEN '100000 - 149999€'
    WHEN truncate(convert(replace(left(cena, char_length(cena)-4), ' ', ''), signed integer), 0) <= 199999 THEN '150000€ - 199999€'
    ELSE '>= 200000€'
END);


-- 2f)
select count(*) as 'Broj nekretnina koje se prodaju u Beogradu i imaju parking'
from nekretnina
where tip_ponude = 'Prodaja' and substring_index(lokacija, ',', 1) = 'Beograd' and parking = 'Da';

select count(*) as 'Broj nekretnina koje se prodaju u Beogradu i nemaju parking'
from nekretnina
where tip_ponude = 'Prodaja' and substring_index(lokacija, ',', 1) = 'Beograd' and parking = 'Ne';