#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import mysql.connector

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return mysql.connector.connect(user='root',password='CxP@0529',database='tournament',use_unicode=True)

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('delete from match_record')
    conn.commit()
    cursor.close()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('delete from player')
    conn.commit()
    cursor.close()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('select count(*) from player')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('insert into player (name) values (%s)', (name,))
    conn.commit()
    cursor.close()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('select player.id, player.name, ifnull(wins,0), ifnull(m,0) from (player left join Wins on player.id = Wins.winner) left join Matches on player.id = Matches.id')
    result = cursor.fetchall()
    print result
    cursor.close()
    conn.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('insert into match_record (playerA, playerB, winner) values (%s, %s, %s)', (winner,loser,winner))
    conn.commit()
    cursor.close()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    result = []
    record = playerStandings()
    counter = 0
    while counter < len(record):
        playerA = record[counter]
        playerB = record[counter+1]
        result.append([playerA[0], playerA[1], playerB[0], playerB[1]])
        counter += 2
    return result
