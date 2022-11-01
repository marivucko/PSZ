use psz_baza;

select * from nekretnina;
select count(*) from nekretnina;

-- 2a) 
select count(*) as 'Broj nekretnina za prodaju'
from nekretnina
where tip_ponude = 'Prodaja';
select count(*) as 'Broj nekretnina za izdavanje'
from nekretnina 
where tip_ponude = 'Izdavanje';

-- 2b)
select substring_index(lokacija, ',', 1) as 'Grad', count(*) as 'Broj nekretnina koje se prodaju u ovom gradu'
from nekretnina
where tip_ponude = 'Prodaja'
group by substring_index(lokacija, ',', 1)
order by substring_index(lokacija, ',', 1);

-- 2c)
select count(*) as 'Broj uknjiženih kuća'
from nekretnina
where tip_nekretnine = 'Kuća' and uknjizenost='Da';
select count(*) as 'Broj neuknjiženih kuća'
from nekretnina
where tip_nekretnine = 'Kuća' and uknjizenost='Ne';
select count(*) as 'Broj uknjiženih stanova'
from nekretnina
where tip_nekretnine = 'Stan' and uknjizenost='Da';
select count(*) as 'Broj neuknjiženih stanova'
from nekretnina
where tip_nekretnine = 'Stan' and uknjizenost='Ne';

-- 2d)
select * 
from nekretnina
where tip_nekretnine = 'Kuća' and tip_ponude = 'Prodaja' and replace(left(cena, char_length(cena)-4), ' ', '') REGEXP '^[0-9]+$'
order by convert(replace(left(cena, char_length(cena)-4), ' ', ''), unsigned integer) desc
limit 30;

select * 
from nekretnina
where tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja' and replace(left(cena, char_length(cena)-4), ' ', '') REGEXP '^[0-9]+$'
order by convert(replace(left(cena, char_length(cena)-4), ' ', ''), unsigned integer) desc
limit 30; 


-- 2e)
select * 
from nekretnina
where tip_nekretnine = 'Kuća' and left(kvadratura, char_length(kvadratura)-3) REGEXP '^[0-9]+$'
order by convert(left(kvadratura, char_length(kvadratura)-3), signed integer) desc
limit 100;

select * 
from nekretnina
where tip_nekretnine = 'Stan' and left(kvadratura, char_length(kvadratura)-3) REGEXP '^[0-9]+$'
order by convert(left(kvadratura, char_length(kvadratura)-3), signed integer) desc
limit 100;


-- 2f)
select * 
from nekretnina
where godina_izgradnje='2020' and replace(left(cena, char_length(cena)-4), ' ', '') REGEXP '^[0-9]+$'
order by convert(replace(left(cena, char_length(cena)-4), ' ', ''), unsigned integer) desc;


-- 2g)
select * 
from nekretnina
WHERE broj_soba REGEXP '^-?[0-9]+$' 
order by broj_soba desc
limit 30;

select * 
from nekretnina
where tip_nekretnine = 'Stan' and left(kvadratura, char_length(kvadratura)-3) REGEXP '^[0-9]+$' 
order by convert(left(kvadratura, char_length(kvadratura)-3), signed integer) desc
limit 30;

select *
from nekretnina
where tip_nekretnine = 'Kuća' and left(povrsina_zemljista, char_length(povrsina_zemljista)-3) REGEXP '^[0-9]+$' 
order by (CASE
    WHEN right(povrsina_zemljista, 2) = 'ar' THEN convert(left(povrsina_zemljista, char_length(povrsina_zemljista)-3), signed integer)*100
    WHEN right(povrsina_zemljista, 2) = 'm²' THEN convert(left(povrsina_zemljista, char_length(povrsina_zemljista)-3), signed integer)
    ELSE 0
END) desc
limit 30;





