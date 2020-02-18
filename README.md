Project Background:
Self Help groups are a poverty alleviation tool used across South Asia. They are groups of 10-15 women women who use collective action and positive peer effect to save, borrow and invest towards a brighter future. The program is implemented by lower government functionaries and field workers who are hamstrung by lack of technological tools. Having worked on such a project in the state of Haryana in India, I decided to create a web application that could solve a good chunk of the problems faced by these officials. 

Approach:
To create the web application Flask microframework was used along with SQLlite for data storage and Jinja2 for the web template engine. The focus was on the backend logic and hence only basic html code was written. However, the web interface is helpful in navigating and understanding the logic of the app. The project was developed entirely on a Windows 10 Machine. Testing was done with some unit tests but mostly through web interface.

Installation:
1. Install all the packages as listed under requirements.txt
2. Activate venv using 'venv\Scripts\activate' for Windows.  
2. Run 'python shg_app.py' on the command line and open the localhost as shown (http://127.0.0.1:5000/).

Navigation:
1. Login using email: nixon@gmail.com and password: nixon123
2. Add a SHG from the top right corner. 
3. View SHGs on Home Page.
4. Click on a SHG to view the SHG page.
5. Add members to SHG from the SHG page. 
6. View members from the SHG page
7. Add member meeting details from the SHG or Member page. 
8. Evaluate SHG from the SHG page
9. Evaluate Member from the Member page

References:
1. Miguel Grinbergs blog series on Flask
2. Corey Shafer's YouTube tutorials on Flask

PS: Heroku link (currently down): https://shg-app1.herokuapp.com/