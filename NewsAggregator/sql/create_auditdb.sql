

drop database if exists auditdb;
create database auditdb;


drop table if exists audit;
drop table if exists url_audit;
drop table if exists errors;
drop table if exists bad_urls;
drop table if exists urls;
drop table if exists url_generation;



create table url_generation(
   id           bigserial    primary key,
   source       varchar(256) not null,
   start_state  varchar(256) not null,
   stop_state   varchar(256) null,
   process_name varchar(256) not null,
   start_time   timestamptz  default now(),
   stop_time    timestamptz  null,
   n_urls       int          null
);


create table urls(
   id                bigserial    primary key,
   url               varchar(256) not null unique,
   url_generation_id bigint       not null,

   foreign key (url_generation_id) references url_generation(id)
);


create table bad_urls(
    id                bigserial    primary key,
    url               varchar(256) not null,
    url_generation_id bigint       not null,
    status_code       int          not null,
    url_response      varchar(256) not null,

    foreign key (url_generation_id) references url_generation(id)
);


create table errors(
    id           bigserial    primary key,
    url_id       bigint       not null,
    error        varchar(512) not null,
    process_name varchar(256) not null,
    time         timestamptz  default now(),

    foreign key (url_id) references urls(id)
);


create table url_audit(
    id           bigserial    primary key,
    url_id       bigint       not null,
    destination  varchar(256) not null,
    process_name varchar(256) not null,
    start_time   timestamptz  default now(),
    stop_time    timestamptz  null,

    foreign key (url_id) references urls(id)
);


create table audit(
    id           bigserial    primary key,
    source       varchar(256) not null,
    destination  varchar(256) not null,
    process_name varchar(256) not null,
    start_time   timestamptz  default now(),
    stop_time    timestamptz  null
);
