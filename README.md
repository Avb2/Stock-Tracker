<h1>Stock Tracker</h1>

<div><b>Good afternoon, traders!</b><div><br>
<p>Stock Tracker is a program that can help you on your day-to-day trading by allowing you to easily track & model stock prices so you can buy at the right time! The data gathered will be displayed to the user in a database table, and current information will be shown in the Tkinter widget. If the stock is lower than the set target price, a new table is created called 'watchlist' and the stocks data is added to it. This allows the user to quickly know which stocks have reached the target prices.
</body></p>

<body>
  <h2>Instructions</h2>
  <ul>
    <li>Run 'main.py'</li>
    <li>Input the name or ticker of the stock or select it from the drop down menu</li>
    <li>Input a target price you would like the stock to reach</li>
    <li>Click the 'enter' button</li>
    <h2>Output:</h2>
    <li>The current time, name of the stock, the price, and previous closing price will be displayed on the tkinter widget</li>
    <li>The stock information, date and time will be added to corresponding databases in new-data-stocks.db</li>
    <li>Models will be created and available to be viewed by clicking the 'Graph' button</li>
  </ul>
  
  <h2>Using Auto Run feature </h2>
  <ul>
    <li>Input the name or ticker of the stock or select it from the drop down menu</li>
    <li> Input a target price you would like the stock to reach</li>
    <li>Press 'Auto Run' button</li>
    <br><p>The stock you have inputted will be scraped every 10 minutes. If the price of the stock is less than the target price, an email will be sent to you.</p>
    <li>Click the 'End' button to end the Auto Run thread</li>
    <br><p>NOTE: You can still scrape other stocks while auto run is active</p>
    <br><p>NOTE: You must use an outlook email to send the emails, gmail will not work</p>
   </ul>
  
  <h2>Using Run All feature </h2>
  <ul>
    <li>Click 'Run All'</li>
    <p>All stocks you have previously searched that are saved in your data-stocks.db file will be web scraped and the prices will be added to the db</p>
    <br><p>NOTE: Once you start the Run All feature, you cannot end it until it is complete</p>
   
  <h2>Under the hood</h2>
  <ul>
    <li>Using Tkinter to create GUI</li>
    <li>Using requests & BeautifulSoup4 to webscrape stock information from 'google.com/finance'</li>
    <li>Using SQLite3 to create and manipulate databases</li>
    <li>Using matplotlib to create graphs displaying stock prices</li>
  </ul>
 </body>

  
 
