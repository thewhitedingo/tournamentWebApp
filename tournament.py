#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

#     DB = connect()
#     c = DB.cursor()
#     c.execute("")
#     DB.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches;")
    DB.commit()
    DB.close()



def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) AS num from players;")
    results = c.fetchall()
    DB.close()
    results = results[0][0]
    return results


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    #register a player to the database
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players(name) values(%s)", (name,))
    DB.commit()
    DB.close()

  # #sets the cursor to look through the database
  # c = DB.cursor()
  # #execute SQL code to fetch results
  # c.execute("SELECT time, content FROM posts ORDER BY time DESC")
  # #format to what the code expects to do with them
  # posts = ({'content': str(bleach.clean((row[1]), strip=True).strip()), 'time': str(row[0])}
  #     for row in c.fetchall())
  # DB.close
  # return posts


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
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT players.id, players.name, "
      "count((SELECT matches.winner from matches where matches.winner = players.id)) as wins, "
      "count(matches.winner) as matches "
      "from players left join matches "
      "on players.id = matches.winner or players.id = matches.loser group by players.id, players.name;")
    results = c.fetchall()
    DB.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches(winner, loser) values(%s, %s)", (winner, loser,))
    DB.commit()
    DB.close()

 
 
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

    DB = connect()
    c = DB.cursor()
    c.execute("CREATE OR REPLACE VIEW standings as " 
      "SELECT players.id, players.name, "
      "count((SELECT matches.winner from matches where matches.winner = players.id)) as wins, "
      "count(matches.winner) as matches "
      "from players left join matches "
      "on players.id = matches.winner or players.id = matches.loser group by players.id, players.name;")
    DB.commit()
    c.execute("SELECT standingsA.id, standingsA.name, standingsA.wins, standingsB.id, standingsB.name, standingsB.wins " 
      "from standings as standingsA, standings as standingsB "
      "where standingsA.wins = standingsB.wins and and standingsA.id > standingsB.id;")
    results = c.fetchall()
    DB.close
    return results



