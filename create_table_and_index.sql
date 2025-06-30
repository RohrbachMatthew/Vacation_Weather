############ Create the table ############

/*
create table vacation_weather_data (
id int auto_increment primary key,
day varchar(10),
date date,
time time,
temperature varchar(10),
conditions varchar(50),
humidity varchar(10),
wind_speed_direction varchar(50),
uv_index int,
tide_height float,
rip_tide_warning varchar(10)
);
*/

#################### Create index for table #####################

/*
create index idx_date on vacation_weather_data(date);
*/

/*
create index idx_time on vacation_weather_data(time);
*/
select * from vacation_weather_data