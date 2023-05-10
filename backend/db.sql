create database jokes;
use jokes;
create table category
(
    Id   int auto_increment
        primary key,
    Name varchar(64) null
);

create table user
(
    Id       int auto_increment
        primary key,
    Username varchar(64)  not null,
    Password varchar(128) not null
);

create table joke
(
    Id         int auto_increment
        primary key,
    Text       varchar(512) null,
    CategoryId int          not null,
    UserId     int          not null,
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

create table rating
(
    Id     int auto_increment
        primary key,
    Rating int not null,
    JokeId int not null,
    constraint rating_joke_Id_fk
        foreign key (JokeId) references joke (Id)
);
