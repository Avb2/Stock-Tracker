<h1>Stock Tracker<h1>

<h2>Good afternoon, traders!<h2>
<p>Stock Tracker is a program that can help you on your day-to-day trading by allowing you to easily track stock prices so that you can buy at the right time!</p>

<body>
Start by running 'main.py'. This program begins by asking the user for the name of the stock they are searching for, and the target price in which they hope the stock reaches. It then displays the current date, time, name of the stock, and the price of the stock in a database file called 'data-stocks.db' using SQLite3, BeautifulSoup4, and requests to collect the data from 'google.com/finance'. This data will then be displayed to the user in a table, so they can track the change in price over time. If the stock reaches the set target price, a new table is created called 'watchlist' and the stocks data is added to it. This allows the user to quickly know which stocks have reached the target price.
</body>

  
  
<ul>
<h2>NEED TO INSTALL:</h2>
<li>datetime<li>
<li>sqlite3</li>
<li>requests</li>
<li>bs4</li>
</ul>
