USE Book_management;

/* full names? */

SELECT CONCAT(author_fname, ' ', author_lname) as 'full names'
FROM books;

/*concat_ws with seperator between all specified columns*/

SELECT CONCAT_WS(' - ',author_fname, author_lname) as 'Seperate with - '
FROM books;

/*result: hell*/

SELECT SUBSTRING('Hello World'  FROM 1 FOR 4);

/*World*/

SELECT SUBSTRING('Hello World', 7);

/*rld*/

SELECT SUBSTRING('Hello World', -3);

/*SUBSTRING = SUBSTR*/

SELECT SUBSTR('Hello World', -3);

/*shorten book's title ...*/

SELECT CONCAT(SUBSTR(title, 1, 10), '...')
FROM books;

/*replace Hell with %$#@ 
Result => %$#@ World
*/

SELECT REPLACE('Hello World', 'Hell', '%$#@');

/*replace ' ' wit ' and '
Result => cheese and bread and coffee and milk*/

SELECT REPLACE('chesse bread coffe milk', ' ', ' and ');


/*Result => dlroW olleH*/

SELECT REVERSE('Hello World');

/*Result => 11*/

SELECT CHAR_LENGTH('Hello World');

/*HELLO WORLD*/

SELECT UPPER('Hello World');

/*hello world*/

SELECT LOWER('Hello World');

/* ---------------------------- */

/*Reverse and Uppercase the following sentence
"Why does my cat look at me with such hatred?"*/

SELECT UPPER(REVERSE('Why does my cat look at me with such hatred?'));

/*
'I-like-cats'
*/

SELECT REPLACE(CONCAT('I',' ', 'like',' ','cat'), ' ', '-');

/*Replace spaces in titles with '->'*/

SELECT REPLACE(title,' ', '->')
FROM books;

/*reverse author_lname*/

SELECT REVERSE(author_lname)
FROM books;

/*full name in caps*/

SELECT UPPER(CONCAT_WS(' ',author_fname, author_lname)) as 'Full name'
FROM books;



/*title + release year
+--------------------------------------------------------------------------+
| blurb                                                                    |
+--------------------------------------------------------------------------+
| The Namesake was released in 2003                                        |
----------------------------------------------------------------------------
*/

SELECT CONCAT(title, ' was released in ', released_year)
FROM books;


/*Print book titles and the length of each title
+-----------------------------------------------------+-----------------+
| title                                               | character count |
+-----------------------------------------------------+-----------------+
| The Namesake                                        |              12 |
-------------------------------------------------------------------------
*/

SELECT title, CHAR_LENGTH(title) as 'character count'
FROM books;


/*
+---------------+-------------+--------------+
| short title   | author      | quantity     |
+---------------+-------------+--------------+
| American G... | Gaiman,Neil | 12 in stock  |
| A Heartbre... | Eggers,Dave | 104 in stock |
+---------------+-------------+--------------+
*/

SELECT  CONCAT(SUBSTR(title,1 , 10), '...') as 'short title', 
		CONCAT(author_fname, ',', author_lname) as author,
        CONCAT(stock_quantity, ' in stock') as quantity
FROM books
ORDER BY 1;