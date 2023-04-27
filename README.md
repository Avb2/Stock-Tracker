<h1>Stock Tracker</h1>

<div><b>Good afternoon, traders!</b><div><br>
<p id='intro'>Stock Tracker is a program that can help you on your day-to-day trading by allowing you to easily track & model stock prices so you can buy at the right time! The data gathered will be displayed to the user in a database table, and current information will be shown in the Tkinter widget. If the stock is lower than the set target price, a new table is created called 'watchlist' and the stocks data is added to it. This allows the user to quickly know which stocks have reached the target prices.</p>
</body>
<br>
  
<body>
<div>
  <h2>Instructions</h2>
  <ul>
    <li>Run 'main.py'</li>
    <li>Input the name or ticker of the stock or select it from the drop down menu</li>
    <li>Input a target price you would like the stock to reach</li>
    <li>Click the 'Enter' button or press the 'Enter' button on your keyboard</li>
    <h2>Output:</h2>
    <li>The current time, name of the stock, the price, and previous closing price will be displayed on the tkinter widget</li>
    <li>The stock information, date and time will be added to corresponding databases in new-data-stocks.db</li>
    <li>Models will be created and available to be viewed by clicking the name of the stock displayed in the stock information frame</li>
  </ul>
  </div>
  
  <br>
  
  <div>
  <h2>Using Auto Run feature </h2>
  <ul>
    <li>Input the name or ticker of the stock or select it from the drop down menu</li>
    <li> Input a target price you would like the stock to reach</li>
    <li>Press 'Auto Run' button</li>
    <li>Click the 'End' button to end the Auto Run thread</li>
    <h2>Output:</h2>
    <li>The stock you have inputted will be scraped every 10 minutes. If the price of the stock is less than the target price, an email will be sent to the specified Outlook email address.</li>
    <br>
    <h2>Auto Running all stocks</h2>
    <li>Input 'all' into the Stocks input field</li>
    <li>Click the 'Auto Run' button</li>
    <h2>Output:</h2>
    <li>All stocks in the AllStocks table in the new-data-stocks.db will be webscraped and the information will be added to the specified stocks table, as well as the AllStocks table</li>
    <br>
    <p><b>NOTE: You can still scrape other stocks while auto run is active</b></p>
    <br>
    <p><b>NOTE: You must use an outlook email to send the emails, gmail will not work</b></p>
   </ul>
   </div>
  
  <br>
  
  <div>
  <h2>Using Run All feature </h2>
  <ul>
    <li>Click 'Run All'</li>
    <h2>Output:</h2>
    <li>All stocks you have previously searched that are saved in your data-stocks.db file will be web scraped and displayed in the GUI.</li>
      <li>The prices will be added to the database</li>
    <br<br>
    <p><b>NOTE: Once you start the Run All feature, you cannot end it until it is complete</b></p>
  </ul>
  </div>
  
  <br>
  
  <div>
  <h2>Creating stock portfoilios</h2>
    <ul>
    <li>Click the 'settings' button</li>
    <li>Type the name you would like to name the stock group into the 'Group Name' entry widget</li>
    <li>Type the stock names that you would like to add to the group into the 'Stock Names' entry widget</li>
    <li>Press the 'Enter' button</li>
    <h2>Output:</h2>
      <li>A newly created stock group/portfolio table will be created containing the name of the group and the stocks within it. The table will be added to the new-stocks-data.db database file</li>
      </ul>
      
   <h2> Searching with stock portfolios</h2>
    <ul>
      <li>After creating a stock group/portfolio under the settings tab, search the name of the group in the 'Stocks' input field</li>
      <li>Press the 'Enter' button</li>
      <h2>Output:</h2>
      <li>The stock information for the stocks within the stock group will be displayed in the stock information frame</li>
      <li>The stock information will be added to the AllStocks and the specified stocks database table</li>
    </ul>
    </div>
  
  <br>
  
 <div>
  <h2>Searching with sectors</h2>
  <ul>
    <li>Type 's tech', 's real estate', or 's finance' into the stock input field</li>
    <li>Leave the target price input field empty</li>
    <li>Click the 'Enter' Button</li>
   </ul>
  </div>
  
  <br>
  
  <div>
  <h2>Viewing Graphs</h2>
  <ul>
  <li>After you have filled out the input fields and clicked the 'Enter' button, stock information will be displayed. Clicking the stock name will display a graph of price history pulled from the new-data-stocks database file. </li>
  <li>Normal plots on the graph will be displayed with the color blue, but the highest price will be displayed in pink</li>
  <li>Increases in stock price will have a green line connecting the plots, and decreases will be connected with a red line</li>
  <h2>Output:</h2>
  <li>A predefined list of popular stocks in the specified sector will be displayed to the user in the tkinter GUI</li>
  <li>The stock information will be added to that sectors database table</li>
  </ul>
    <br>
  <p><b>NOTE: Data displayed on the graph will only be data that has been collected when you run that specific stock. Unless you are using the Auto Run feature and letting the program run, stocks will have to be searched manually.</b></p>
  </div>
  
   <br>
  
   <div>
  <h2>Under the hood</h2>
  <ul>
    <li>Using Tkinter to create GUI</li>
    <li>Using requests & BeautifulSoup4 to webscrape stock information from 'google.com/finance'</li>
    <li>Using SQLite3 to create and manipulate databases</li>
    <li>Using matplotlib to create graphs displaying stock prices</li>
    <li>Using datetime package to collect date and time information</li>
    <li>Using threading package to create multiple threads to increase speed</li>
  </ul>
</div>
 </body>

  
 
