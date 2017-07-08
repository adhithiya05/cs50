from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    
    portfolio = db.execute("SELECT shares, symbol FROM portfolio WHERE id = :id",
    id = session["user_id"])    
    
    total = 0
    
    for portfolios in portfolio:
        symbol = portfolios["symbol"]
        shares = portfolios["shares"]
        stock = lookup(symbol)
        totalcash = shares * stock["price"]
        total += totalcash
        db.execute("UPDATE portfolio SET price = :price, total = :total WHERE id = :id AND \
        symbol = :symbol", price = usd(stock["price"]), total = usd(totalcash)
        , id = session["user_id"], symbol = symbol)
    
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
    
    total += cash[0]["cash"]
    
    newportfolio = db.execute("SELECT * FROM portfolio WHERE id = :id", id = session["user_id"])
    
    return render_template("index.html", stocks = newportfolio, cash = usd(cash[0]["cash"]),
    total = usd(total))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        
        if not request.form.get("symbol"):
            return apology("Symbol missing")
            
        elif not request.form.get("share"):
            return apology("Share no missing")
            
        symbol = lookup(request.form.get("symbol"))
        
        if symbol is None:
            return apology("Invalid symbol")
            
        sh = int((request.form.get("share")))
        sh1 = float((request.form.get("share")))
        
        if sh < 1:
            return apology("Enter valid no")
            
        name = symbol["name"]
        price = symbol["price"]
        symbol = symbol["symbol"]
        
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        amount = cash[0]["cash"]
        amt = float(amount)
        
        if not (price * sh1) < amt:
            return apology("Not enough cash") 
            
        new_cash = amt - (price * sh1)
        
        purchase = db.execute("INSERT INTO purchase (id,stocksymbol,price,shares) \
        VALUES(:id, :stocksymbol, :price, :shares)",
        id = session["user_id"], stocksymbol = symbol ,price = usd(price), 
        shares = (request.form.get("share")))
        
        update = db.execute("UPDATE users SET cash = :newcash WHERE id = :id" ,
        newcash = new_cash,  id = session["user_id"])
        
        
        usershares = db.execute("SELECT shares FROM portfolio WHERE id = :id and\
        symbol = :symbol",id = session["user_id"], symbol = symbol)
        
        if not usershares:
            db.execute("INSERT into portfolio (name,shares,price,total,symbol,id) \
            VALUES(:name,:shares,:price,:total,:symbol,:id)", name = name, 
            shares = (request.form.get("share")), price = usd(price),
            total = usd((price * sh1)), symbol = symbol, id = session["user_id"])
            
        else:
            totalshares = (usershares[0]["shares"] + int(request.form.get("share")))
            
            
            db.execute("UPDATE portfolio SET shares = :newshare WHERE id = :id\
            and symbol = :symbol",newshare = totalshares, id = session["user_id"], symbol = symbol)
            
        return redirect(url_for("index"))
    
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    #Get information from purchase table
    purchase = db.execute("SELECT * FROM purchase WHERE id = :id", id = session["user_id"])
    
    #Pass the information to the html template
    return render_template("history.html", histories = purchase)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", 
        username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        
        if not request.form.get("quote"):
            return apology("Quote missing")
        
        quote = lookup(request.form.get("quote"))
        
        if quote is None:
            return apology("Quote invalid")
        
        name = quote["name"]    
        price = quote["price"]
        symbol = quote["symbol"]
        
        return render_template("quoted.html", name = name, price = usd(price), sym = symbol)
    
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Missing username !")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")
            
        elif not request.form.get("repassword"):
            return apology("Must re-enter password")
    
        elif  request.form.get("password") != request.form.get("repassword"):
            return apology("Passwords do not match")
            
        
        hash = pwd_context.encrypt(request.form.get("password"))
        
        result = db.execute("INSERT INTO users (username,hash) VALUES(:username, :hash)",
        username = request.form.get("username"), hash = hash)
        
        if not result:
            return apology("Username already exists")
        
        
        session["user_id"] = result
       
        return redirect(url_for("index"))
            
    else:    
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    if request.method == "POST":
        
        if not request.form.get("symbol"):
            return apology("Symbol missing")
        if not request.form.get("share_no"):
            return apology("Share missing")
            
        stock = lookup(request.form.get("symbol"))
        
        if not stock:
            return apology("Invalid symbol")
            
        name = stock["name"]
        price = stock["price"]
        symbol = stock["symbol"]
            
        
        shares = int(request.form.get("share_no"))
        if shares < 0:
            return apology("Enter positive number")
        
            
        sym = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol = :symbol",
        id = session["user_id"], symbol = symbol)
        
        if sym is None:
            return apology("Share not bought")
            
        shareno = int(sym[0]["shares"])
        givenshare = int(request.form.get("share_no"))
        updateshare = -givenshare
        
        if shareno < givenshare: 
            return apology("Not enough shares")
        
        db.execute("INSERT INTO purchase (id,stocksymbol,price,shares) \
        VALUES(:id, :stocksymbol, :price, :shares)",
        id = session["user_id"], stocksymbol = symbol ,price = usd(price), 
        shares = updateshare)
        
        db.execute("UPDATE users SET cash = cash + :purchase WHERE id = :id",
        id = session["user_id"], purchase = price * float(givenshare))
        
        shares_total = sym[0]["shares"] - givenshare
        
        if shares_total == 0:
            db.execute("DELETE FROM portfolio WHERE id = :id AND symbol = :symbol",
            id = session["user_id"], symbol = symbol)
        else:
            db.execute("UPDATE portfolio SET shares = :shares WHERE id = :id AND symbol = :symbol",
            shares = shares_total, id = session["user_id"], symbol = symbol)
        
        
        return redirect(url_for("index"))
            
    else:
        return render_template("sell.html")



@app.route("/cash", methods=["GET" , "POST"])
@login_required
def cash():
    """ Add cash """
    
    if request.method == "POST":
        
        
        try: 
            cash = int(request.form.get("cash")) 
            if cash < 1:
                return apology("Enter valid cash")
            elif cash > 1000000:
                return apology("Can only add upto 1,000,000$ per try")
        except:
            return apology("Enter cash") 
        
        newcash = float(request.form.get("cash"))
        
        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :id",
        cash = newcash, id = session["user_id"])
        
        return redirect(url_for("index"))
        
        
    else:
        return render_template("cash.html")
        
        
