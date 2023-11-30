# Basic Command Syntax for Vivace

There will be a **py command handler**, and a **js command handler**, for **back-end** and **front-end** respectively.<br>
This is so that the 2 languages can _interact with eachother_ with a **standardised set of commands in a standardised format**.<br>

## Data requests

### Get Data

All _get_ commands will start with **"get"**.<br>
Then, the **target data** will be entered.<br>
_If it applies to a certain object_, like an **artist**, **song**, or **album**, the object name will follow first.<br>
Then, the **target data type** will be added, if required.<br>
If we are searching a database, a **target data key** will be required.<br>
Finally, the **extra information** (if applicable).<br>
_Spaces_ in names will be replaced with a dash (-).<br>
The _order_ goes like this:<br>

- artist
- album
- song

_If not_, simply the **command instructions** will follow.<br>

#### e.g.

Say I want to **get the kworb.net link** for _Billie Eilish_'s songs.<br>

> #### get data Billie-Eilish link kworb streams songs

> - get = **get command word**
> - data = **keyword**, _tells program it's a piece of data_
> - Billie-Eilish = **target object**, _artist comes first_
> - link = **target data**, _comes before target data type_
> - kworb = **target data type**
> - streams, songs = **extra information**, _there are more than 1 pages for Billie Eilish's stats_

This, once fully implemented, will return:<br>

> <https://kworb.net/spotify/artist/6qqNVTkY8uBg9cP3Jd7DAH_songs.html>

Say I want to **get the link** to _Billie Eilish's stats_ **from the webpage https://kworb.net/spotify/listeners.html**. <br>

> #### get data Billie-Eilish stats with link https://kworb.net/spotify/listeners.html

> - get = **get command word**
> - data = **keyword**, _tells program it's a piece of data_
> - Billie-Eilish = **target object**, _artist comes first_
> - stats = **target data**, _comes before target data type (if applicable)_
> - with = **keyword**, _mostly there for readability_
> - link = **target data type** , _tells program what type the following data is_
> - \[kworb link] = **data**, _gives program the data to use_

Say I wanted to **get all information** **from the database main**, **the table monthlyListeners**, using the **primary key Billie-Eilish** <br>

> #### get all from database main table artists with key name Billie-Eilish

> - get = **get command word**
> - all = **target data**, _in this case all fields from table_
> - from database main = **keyword/target data location**, _get data from the database 'main', 'database' considered keyword_
> - table artists = **target data location (cont)**, _get data from the table artists_
> - with key Billie-Eilish = **target data key**, _using the key_

### Send Data

All _send_ commands will start with **"send"**.<br>
If applicable, a **file location** will be sent, and then a **file name**. This will _always_ be _preceded_ by the keyword **file**.<br>
If not, a piece of data, be it a _string_, an _integer_, etc, will be entered, _after_ the keyword **data**.<br>
A **command word** will then follow. For instance, if I wanted to _store something in a database_, the command word would be **store**.<br>
If required, **more context** will be added to the **command word**. For instance, if I wanted to _store something in a database named artists_, the command word & context would be **store in database artists**.<br>

#### e.g.

Say I want to **store a file** _(already formatted)_ **called "Billie-Eilish.txt"** in a **database called main**, in a **table called artists** located in a **subfolder called transfer**.<br>

> #### send file transfer/ Billie-Eilish.txt store in database main table artists

> - send = **send command word**
> - file = **keyword**, _tells program it's a file and not a piece of data_
> - transfer/ = **file location**, _tells program that the target file is in a subfolder with the path transfer/_
> - Billie-Eilish.txt = **file name**
> - store = **command word**, _tells program what to do_
> - in database main = **extra information**, _tells program to store in a database called main_
> - in table artists = **extra information**, _tells program to store in a table called artists_
