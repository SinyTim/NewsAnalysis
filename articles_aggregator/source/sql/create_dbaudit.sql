

drop database if exists dbaudit;
create database dbaudit;


--drop table if exists errors;
drop table if exists audit;


create table audit(
    id           bigserial    primary key,
    process_name varchar(256) not null,
    state_start  varchar(256) not null,
    state_stop   varchar(256) null,
    time_start   timestamptz  default now(),
    time_stop    timestamptz  null
);


--create table errors(
--    id           bigserial    primary key,
--    url_id       bigint       not null,
--    error        varchar(512) not null,
--    process_name varchar(256) not null,
--    time         timestamptz  default now()
--);
