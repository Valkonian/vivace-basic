# Basic Command Syntax for Vivace

## Data requests

#### Get Data

All get commands will start with **"get"**.<br>
Then, the **target data** will be entered.<br>
_If it applies to a certain object_, like an **artist**, **song**, or **album**, the object name will follow first.<br>
Then, the **target data type** will be added, if required.<br>
Finally, the **extra information** (if applicable).<br>
_Spaces_ in names will be replaced with a dash (-).<br>
The _order_ goes like this:<br>

> artist
> album
> song

_If not_, simply the **command instructions** will follow.<br>

##### e.g.

Say I want to get the **kworb.net link** for _Billie Eilish_'s song .<br>

> ##### get Billie-Eilish link kworb streams songs

> - get = **get command word**
> - Billie-Eilish = **target object**, _artist comes first_
> - link = **target data**, _comes before target data type_
> - kworb = **target data type**
> - streams, songs = **extra information**, _there are more than 1 pages for Billie Eilish's stats_

This, once fully implemented, will return:<br>

> https://kworb.net/spotify/artist/6qqNVTkY8uBg9cP3Jd7DAH_songs.html
