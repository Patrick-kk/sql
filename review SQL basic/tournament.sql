-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table player
(
    id serial primary key,
    name varchar(20)
);

create table match_record
(
    id serial primary key,
        playerA int(20) references player(id),
        playerB int(20) references player(id),
        winner int(20) references player(id)
);

create view Wins as
(
    select winner, count(*)  as wins
    from match_record
    group by winner
);

create view Matches as
(
    select player.id, count(*) as m
    from player, match_record
    where (player.id = match_record.playerA) or (player.id = match_record.playerB)
    group by player.id
);
