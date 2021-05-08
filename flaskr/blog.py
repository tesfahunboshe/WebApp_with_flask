from flask import Blueprint
from flask import flash
from flask import g
from flask import session
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)

@bp.route("/")
def home():

    user_id = session.get("user_id")    
    return render_template("blog/home.html",user_id = user_id)


@bp.route("/applications")
@login_required
def applications():
    user_id = g.user["id"]    
    db = get_db()
    Applications = db.execute(
        "SELECT Ap.applicantID,Ap.firstname, Ap.lastname, Ap.email,Ap.phone,Ad.city,Ad.country,Ad.zipCode,Ad.streetname,Pr.programName,Pr.status,Do.document,Do.passport,Do.docDescription,Do.passDescription"
        " FROM Applicant Ap"
        " INNER JOIN Address Ad ON Ap.applicantID = Ad.AddressID"
        " INNER JOIN OtherInformation Oi ON Ap.applicantID = Oi.InfoID" 
        " INNER JOIN Program Pr ON Oi.InfoID = Pr.programID"
        " INNER JOIN Documents Do ON Do.documentID = Pr.programID"
        " WHERE Ap.applicantID = ?",[user_id]       
    ).fetchall()
    # if isinstance(Applications, list):
    #     return str(len(Applications)) 
    # else:
    return render_template("blog/applications.html", Applications=Applications)


def get_post(id, check_author=True):
    user_id = g.user["id"]
    db = get_db()
    Applications = db.execute(
        "SELECT Ap.applicantID, Ap.firstname, Ap.lastname, Ap.email,Ap.phone,Ad.city,Ad.country,Ad.zipCode,Ad.streetname,Pr.programName,Pr.status,Do.document,Do.passport,Do.docDescription,Do.passDescription"
        " FROM Applicant Ap"
        " INNER JOIN Address Ad ON Ap.applicantID = Ad.AddressID"
        " INNER JOIN OtherInformation Oi ON Ap.applicantID = Oi.InfoID" 
        " INNER JOIN Program Pr ON Oi.InfoID = Pr.programID"
        " INNER JOIN Documents Do ON Do.documentID = Pr.programID"
        " WHERE Ap.applicantID = ?",(user_id,),       
    ).fetchall()

    if Applications is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and Applications[0]["applicantID"] != g.user["id"]:
        abort(403)

    return Applications


@bp.route("/applynow", methods=("GET", "POST"))
@login_required
def applynow():
    """Create a new post for the current user."""
    if request.method == "POST":
        # title = request.form["title"]
        # body = request.form["body"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        phone = request.form["phone"]
        program = request.form["program"]
        citizenship = request.form["citizenship"]
        status = request.form["status"]
        zipcode = request.form["zipcode"]
        streetname = request.form["streetname"]
        country = request.form["country"]
        city = request.form["city"]
        docDescription = request.form["description1"]
        document = request.form["file"]
        passDescription = request.form["description2"]
        passport = request.form["file2"]
        error = None

        Data = [firstname,lastname,email,phone]
        if Data is None:
            return "No data submitted"
        

        user_id = g.user["id"]

        if not email:
            error = "Email is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO Applicant (firstname, lastname, email,phone,zipcode,applicantID) VALUES (?, ?, ?,?, ?, ?)",
                (firstname, lastname,email, phone,zipcode, user_id),
            )
            db.execute(
                "INSERT INTO OtherInformation (InfoID, applicantID, documentID, programID) VALUES (?,?, ?, ?)",
                (user_id, user_id, user_id,user_id),
            )
            db.execute(
                "INSERT INTO Address (zipCode, streetname,city,country) VALUES (?, ?, ?, ?)",
                (zipcode, streetname,city,country),
            )
            db.execute(
                "INSERT INTO Documents (documentID, docDescription, document, passDescription, passport) VALUES (?, ?,?, ?, ?)",
                (user_id, docDescription, document, passDescription, passport),
            )
            db.execute(
                "INSERT INTO Program (programID, programName,status) VALUES (?, ?,?)",
                (user_id, program, status),
            )
            db.commit()
            return redirect(url_for("blog.applications"))

    return render_template("blog/applynow.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    # post = get_post(id)
    Applications = get_post(id)
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        phone = request.form["phone"]
        program = request.form["program"]
        citizenship = request.form["citizenship"]
        status = request.form["status"]
        zipcode = request.form["zipcode"]
        streetname = request.form["streetname"]
        country = request.form["country"]
        city = request.form["city"]
        docDescription = request.form["description1"]
        document = request.form["file"]
        passDescription = request.form["description2"]
        passport = request.form["file2"]
        error = None

        if not email:
            error = "Email is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE Applicant SET firstname = ?, lastname = ?, email = ?, phone = ?, zipcode = ? WHERE applicantID = ?", (firstname, lastname, email,phone,zipcode,id)
            )
            db.execute(
                "UPDATE Address SET zipCode = ?, streetname = ?, city = ?, country = ? WHERE zipCode = ?", (zipcode, streetname,city,country,zipcode)
            )
            db.execute(
                "UPDATE Documents SET docDescription = ?, document = ?, passDescription = ?, passport = ? WHERE documentID = ?", (docDescription, document, passDescription, passport,id)
            )
            db.execute(
                "UPDATE OtherInformation SET applicantID = ?, documentID = ? WHERE InfoID = ?", (id, id, id)
            )
            db.execute(
                "UPDATE Program SET programName = ?, status = ? WHERE programID = ?", (program,status,id)
            )
            db.commit()
            return redirect(url_for("blog.applications"))

    return render_template("blog/update.html",Applications=Applications)


@bp.route("/table")
@login_required
def table():

    db = get_db()
    # posts = db.execute(
    #     "SELECT p.id, title, body, created, author_id, username"
    #     " FROM post p JOIN user u ON p.author_id = u.id"
    #     " ORDER BY created DESC"
    # ).fetchall()
    db.execute(
        "DROP VIEW IF EXISTS Data;"          
    ).fetchall()
    db.execute(
        "DROP VIEW IF EXISTS dataTable; "     
    ).fetchall()
    
    dataTable = db.execute(
        "SELECT firstname, lastname, email,country,programName"
        " FROM Applicant"
        " INNER JOIN Address ON applicantID = AddressID" 
        " INNER JOIN Program ON applicantID = programID"       
    ).fetchall()
    CountryData = db.execute(
        "SELECT country, count(*) as N_applicants, max(score) as maximumScore, min(score) as minimumScore"
        " FROM Address"
        " INNER JOIN OtherInformation ON AddressID = applicantID"
        " GROUP BY country" 
    ).fetchall()

    if  not dataTable:
        return render_template("blog/home.html")
    return render_template("blog/table.html",dataTable = dataTable,CountryData=CountryData)

@bp.route("/<int:id>/profile", methods=("GET", "POST"))
@bp.route("/profile")
@login_required
def profile(id):
    db = get_db()
    Profile = db.execute(
        "SELECT firstname, lastname, email,phone,decision,score"
        " FROM Applicant a JOIN OtherInformation o ON a.applicantID = o.InfoID"
        " WHERE O.InfoID = ?",
            (id,),               
    ).fetchall()
    if  not Profile:
        return render_template("blog/home.html")   
    return render_template("blog/profile.html",Profile = Profile)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.
    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM Applicant WHERE applicantID = ?", (id,))
    db.execute("DELETE FROM Address WHERE AddressID = ?", (id,))
    db.execute("DELETE FROM Documents WHERE documentID = ?", (id,))
    db.execute("DELETE FROM OtherInformation WHERE InfoID = ?", (id,))
    db.execute("DELETE FROM Program WHERE programID = ?", (id,))
    db.commit()
    return redirect(url_for("blog.applications"))



@bp.route("/admin", methods=("GET", "POST"))
@login_required
def admin():
    #admin is able to see and grade the applications. 
    db = get_db()        
    dataAdmin = db.execute(
        "SELECT Ap.applicantID,Ap.firstname, Ap.lastname, score, decision,Ap.email,Ap.phone,Ad.city,Ad.country,Ad.zipCode,Ad.streetname,Pr.programName,Pr.status,Do.document,Do.passport,Do.docDescription,Do.passDescription"
        " FROM Applicant Ap"
        " INNER JOIN Address Ad ON Ap.applicantID = Ad.AddressID"
        " INNER JOIN OtherInformation Oi ON Ap.applicantID = Oi.InfoID" 
        " INNER JOIN Program Pr ON Oi.InfoID = Pr.programID"
        " INNER JOIN Documents Do ON Do.documentID = Pr.programID"
    ).fetchall()    
    if  not dataAdmin:
        return redirect(url_for("blog.home"))
    return render_template("blog/admin.html", dataAdmin = dataAdmin)


