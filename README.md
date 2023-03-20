<h1>Stock Tracker</h1>

<div><b>Good afternoon, traders!</b><div><br>
<p>Stock Tracker is a program that can help you on your day-to-day trading by allowing you to easily track & model stock prices so you can buy at the right time! The data gathered will be displayed to the user in a database table, and current information will be shown in the Tkinter widget. If the stock is lower than the set target price, a new table is created called 'watchlist' and the stocks data is added to it. This allows the user to quickly know which stocks have reached the target prices.
</body></p>

<body>
  <h2>Instructions</h2>
  <ul>
    <li>Run 'main.py'</li>
    <li>Input the name or ticker of the stock</li>
    <li>Input a target price you would like the stock to reach</li>
    <li>Click the 'enter' button</li>
    <li>Click the 'show' button</li>
    <h2>Output:</h2>
    <li>The current time, name of the stock, and the price will be displayed on the tkinter widget</li>
    <li>The stock information, date and time will be added to corresponding databases in data-stocks.db</li>
    <li>Models will be created and available to be viewed in your IDE, if using PyCharm, under the SciView tab</li>
  </ul>
  
  <h2>Under the hood</h2>
  <ul>
    <li>Using Tkinter to create GUI</li>
    <li>Using requests & BeautifulSoup4 to webscrape stock information from 'google.com/finance'</li>
    <li>Using SQLite3 to create and manipulate databases</li>
    <li>Using matplotlib to create graphs displaying stock prices</li>
  </ul>
 </body>

  
 
