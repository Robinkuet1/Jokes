create database jokes;
use jokes;

create table category
(
    Id   int auto_increment
        primary key,
    Name varchar(64) null
);

create table country
(
    Id   int auto_increment
        primary key,
    Name varchar(128) null,
    CODE varchar(2)   null
);

create table user
(
    Id        int auto_increment
        primary key,
    Username  varchar(64)  not null,
    Password  varchar(128) not null,
    CountryId int          not null,
    NSFW      tinyint(1)   null,
    Token     varchar(64)  null,
    constraint user_country_Id_fk
        foreign key (CountryId) references country (Id)
);

create table joke
(
    Id         int auto_increment
        primary key,
    Text       varchar(512) null,
    CategoryId int          not null,
    UserId     int          not null,
    NSFW       tinyint(1)   null,
    constraint Joke_category_Id_fk
        foreign key (CategoryId) references category (Id),
    constraint Joke_user_Id_fk
        foreign key (UserId) references user (Id)
);

create table comment
(
    Id     int auto_increment
        primary key,
    Text   varchar(128) not null,
    JokeId int          not null,
    constraint Comment_joke_Id_fk
        foreign key (JokeId) references joke (Id)
);

create table vote
(
    UserId int        not null,
    JokeId int        not null,
    Up     tinyint(1) null,
    constraint JokeId
        foreign key (JokeId) references joke (Id),
    constraint UserId
        foreign key (UserId) references user (Id)
);

