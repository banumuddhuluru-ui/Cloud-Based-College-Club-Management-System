from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

app = Flask(__name__)

DATABASE = "college_club.db"


# ================= DATABASE =================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clubs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            coordinator TEXT,
            category TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            register_no TEXT NOT NULL,
            department TEXT,
            email TEXT,
            club_id INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT,
            venue TEXT,
            description TEXT,
            club_id INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            register_no TEXT NOT NULL,
            event_id INTEGER
        )
    """)

    conn.commit()
    conn.close()


# Initialize database when app starts
init_db()


# ================= COMMON HTML =================

HTML_START = """
<!DOCTYPE html>
<html>
<head>
    <title>College Club Management System</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f6f9;
            color: #222;
        }

        nav {
            background: #243447;
            padding: 15px;
            text-align: center;
        }

        nav a {
            color: white;
            text-decoration: none;
            margin: 0 12px;
            font-weight: bold;
        }

        nav a:hover {
            color: #61dafb;
        }

        .container {
            width: 90%;
            max-width: 1100px;
            margin: 30px auto;
        }

        h1, h2 {
            color: #243447;
        }

        .hero {
            background: white;
            padding: 35px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        .hero h1 {
            margin-top: 0;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        .card h2 {
            font-size: 35px;
            margin: 5px;
        }

        .form-box {
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        }

        input, textarea, select {
            width: 100%;
            padding: 12px;
            margin: 8px 0 15px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 15px;
        }

        textarea {
            height: 100px;
            resize: vertical;
        }

        button, .btn {
            background: #243447;
            color: white;
            border: none;
            padding: 11px 18px;
            border-radius: 6px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }

        button:hover, .btn:hover {
            background: #16232f;
        }

        .delete {
            background: #d9534f;
        }

        .delete:hover {
            background: #b52b27;
        }

        .club {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .event {
            background: white;
            padding: 20px;
            border-left: 5px solid #243447;
            margin-bottom: 15px;
            border-radius: 8px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            margin-top: 15px;
        }

        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }

        th {
            background: #243447;
            color: white;
        }

        .search {
            margin-bottom: 20px;
        }

        footer {
            margin-top: 40px;
            padding: 20px;
            text-align: center;
            background: #243447;
            color: white;
        }

        @media(max-width: 600px) {
            nav a {
                display: block;
                margin: 8px;
            }

            .container {
                width: 94%;
            }
        }
    </style>
</head>

<body>

<nav>
    <a href="/">Dashboard</a>
    <a href="/clubs">Clubs</a>
    <a href="/members">Members</a>
    <a href="/events">Events</a>
    <a href="/registrations">Registrations</a>
</nav>

<div class="container">
"""


HTML_END = """
</div>

<footer>
    Cloud-Based College Club Management System
</footer>

</body>
</html>
"""


# ================= DASHBOARD =================

@app.route("/")
def home():

    conn = get_db()

    clubs = conn.execute(
        "SELECT COUNT(*) FROM clubs"
    ).fetchone()[0]

    members = conn.execute(
        "SELECT COUNT(*) FROM members"
    ).fetchone()[0]

    events = conn.execute(
        "SELECT COUNT(*) FROM events"
    ).fetchone()[0]

    registrations = conn.execute(
        "SELECT COUNT(*) FROM event_registrations"
    ).fetchone()[0]

    conn.close()

    html = HTML_START + f"""
        <div class="hero">

            <h1>🎓 College Club Management System</h1>

            <p>
                Manage college clubs, members, events and registrations
                in one place.
            </p>

        </div>

        <div class="cards">

            <div class="card">
                <h2>{clubs}</h2>
                <p>Total Clubs</p>
            </div>

            <div class="card">
                <h2>{members}</h2>
                <p>Total Members</p>
            </div>

            <div class="card">
                <h2>{events}</h2>
                <p>Total Events</p>
            </div>

            <div class="card">
                <h2>{registrations}</h2>
                <p>Event Registrations</p>
            </div>

        </div>
    """ + HTML_END

    return render_template_string(html)


# ================= CLUBS =================

@app.route("/clubs")
def clubs():

    search = request.args.get("search", "")

    conn = get_db()

    if search:
        club_list = conn.execute(
            """
            SELECT * FROM clubs
            WHERE name LIKE ?
            OR category LIKE ?
            """,
            ("%" + search + "%", "%" + search + "%")
        ).fetchall()
    else:
        club_list = conn.execute(
            "SELECT * FROM clubs ORDER BY id DESC"
        ).fetchall()

    conn.close()

    html = HTML_START + """

        <h1>🏫 College Clubs</h1>

        <div class="form-box">

            <h2>Add New Club</h2>

            <form method="POST" action="/add-club">

                <label>Club Name</label>
                <input type="text" name="name" required>

                <label>Category</label>
                <input type="text" name="category"
                       placeholder="Coding / Cultural / Sports">

                <label>Coordinator</label>
                <input type="text" name="coordinator">

                <label>Description</label>
                <textarea name="description"></textarea>

                <button type="submit">Add Club</button>

            </form>

        </div>

        <form class="search" method="GET">

            <input type="text"
                   name="search"
                   placeholder="Search clubs..."
                   value=\"""" + search + """\">

            <button type="submit">Search</button>

        </form>
    """

    for club in club_list:

        html += f"""
        <div class="club">

            <h2>{club['name']}</h2>

            <p><b>Category:</b> {club['category'] or 'Not specified'}</p>

            <p><b>Coordinator:</b>
            {club['coordinator'] or 'Not specified'}</p>

            <p>{club['description'] or 'No description available.'}</p>

            <a class="btn delete"
               href="/delete-club/{club['id']}"
               onclick="return confirm('Delete this club?')">
               Delete
            </a>

        </div>
        """

    html += HTML_END

    return render_template_string(html)


@app.route("/add-club", methods=["POST"])
def add_club():

    name = request.form["name"]
    category = request.form["category"]
    coordinator = request.form["coordinator"]
    description = request.form["description"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO clubs
        (name, category, coordinator, description)
        VALUES (?, ?, ?, ?)
        """,
        (name, category, coordinator, description)
    )

    conn.commit()
    conn.close()

    return redirect("/clubs")


@app.route("/delete-club/<int:id>")
def delete_club(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM clubs WHERE id = ?",
        (id,)
    )

    conn.execute(
        "DELETE FROM members WHERE club_id = ?",
        (id,)
    )

    conn.execute(
        "DELETE FROM events WHERE club_id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/clubs")


# ================= MEMBERS =================

@app.route("/members")
def members():

    conn = get_db()

    member_list = conn.execute("""
        SELECT members.*, clubs.name AS club_name
        FROM members
        LEFT JOIN clubs
        ON members.club_id = clubs.id
        ORDER BY members.id DESC
    """).fetchall()

    club_list = conn.execute(
        "SELECT * FROM clubs"
    ).fetchall()

    conn.close()

    html = HTML_START + """

        <h1>👩‍🎓 Student Members</h1>

        <div class="form-box">

            <h2>Register as Club Member</h2>

            <form method="POST" action="/add-member">

                <label>Student Name</label>
                <input type="text" name="name" required>

                <label>Register Number</label>
                <input type="text" name="register_no" required>

                <label>Department</label>
                <input type="text" name="department">

                <label>Email</label>
                <input type="email" name="email">

                <label>Select Club</label>

                <select name="club_id" required>

                    <option value="">Select Club</option>
    """

    for club in club_list:
        html += f"""
                    <option value="{club['id']}">
                        {club['name']}
                    </option>
        """

    html += """
                </select>

                <button type="submit">
                    Register Member
                </button>

            </form>

        </div>

        <h2>Registered Members</h2>

        <table>

            <tr>
                <th>Name</th>
                <th>Register No</th>
                <th>Department</th>
                <th>Email</th>
                <th>Club</th>
                <th>Action</th>
            </tr>
    """

    for member in member_list:

        html += f"""
            <tr>

                <td>{member['name']}</td>

                <td>{member['register_no']}</td>

                <td>{member['department'] or '-'}</td>

                <td>{member['email'] or '-'}</td>

                <td>{member['club_name'] or '-'}</td>

                <td>
                    <a class="btn delete"
                       href="/delete-member/{member['id']}"
                       onclick="return confirm('Delete member?')">
                       Delete
                    </a>
                </td>

            </tr>
        """

    html += "</table>" + HTML_END

    return render_template_string(html)


@app.route("/add-member", methods=["POST"])
def add_member():

    name = request.form["name"]
    register_no = request.form["register_no"]
    department = request.form["department"]
    email = request.form["email"]
    club_id = request.form["club_id"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO members
        (name, register_no, department, email, club_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, register_no, department, email, club_id)
    )

    conn.commit()
    conn.close()

    return redirect("/members")


@app.route("/delete-member/<int:id>")
def delete_member(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM members WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/members")


# ================= EVENTS =================

@app.route("/events")
def events():

    conn = get_db()

    event_list = conn.execute("""
        SELECT events.*, clubs.name AS club_name
        FROM events
        LEFT JOIN clubs
        ON events.club_id = clubs.id
        ORDER BY events.date ASC
    """).fetchall()

    club_list = conn.execute(
        "SELECT * FROM clubs"
    ).fetchall()

    conn.close()

    html = HTML_START + """

        <h1>📅 Club Events</h1>

        <div class="form-box">

            <h2>Create New Event</h2>

            <form method="POST" action="/add-event">

                <label>Event Name</label>
                <input type="text" name="name" required>

                <label>Date</label>
                <input type="date" name="date" required>

                <label>Venue</label>
                <input type="text" name="venue">

                <label>Select Club</label>

                <select name="club_id" required>

                    <option value="">Select Club</option>
    """

    for club in club_list:
        html += f"""
                    <option value="{club['id']}">
                        {club['name']}
                    </option>
        """

    html += """

                </select>

                <label>Description</label>

                <textarea name="description"></textarea>

                <button type="submit">
                    Create Event
                </button>

            </form>

        </div>

        <h2>Upcoming Events</h2>
    """

    for event in event_list:

        html += f"""

        <div class="event">

            <h2>{event['name']}</h2>

            <p>
                <b>Club:</b>
                {event['club_name'] or '-'}
            </p>

            <p>
                <b>Date:</b>
                {event['date'] or '-'}
            </p>

            <p>
                <b>Venue:</b>
                {event['venue'] or '-'}
            </p>

            <p>
                {event['description'] or 'No description'}
            </p>

            <a class="btn delete"
               href="/delete-event/{event['id']}"
               onclick="return confirm('Delete event?')">
               Delete
            </a>

        </div>

        """

    html += HTML_END

    return render_template_string(html)


@app.route("/add-event", methods=["POST"])
def add_event():

    name = request.form["name"]
    date = request.form["date"]
    venue = request.form["venue"]
    description = request.form["description"]
    club_id = request.form["club_id"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO events
        (name, date, venue, description, club_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, date, venue, description, club_id)
    )

    conn.commit()
    conn.close()

    return redirect("/events")


@app.route("/delete-event/<int:id>")
def delete_event(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM events WHERE id = ?",
        (id,)
    )

    conn.execute(
        "DELETE FROM event_registrations WHERE event_id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/events")


# ================= EVENT REGISTRATION =================

@app.route("/registrations")
def registrations():

    conn = get_db()

    events_list = conn.execute(
        "SELECT * FROM events ORDER BY date"
    ).fetchall()

    registrations_list = conn.execute("""
        SELECT event_registrations.*,
               events.name AS event_name
        FROM event_registrations
        LEFT JOIN events
        ON event_registrations.event_id = events.id
        ORDER BY event_registrations.id DESC
    """).fetchall()

    conn.close()

    html = HTML_START + """

        <h1>🎟️ Event Registration</h1>

        <div class="form-box">

            <h2>Register for an Event</h2>

            <form method="POST"
                  action="/register-event">

                <label>Student Name</label>

                <input type="text"
                       name="student_name"
                       required>

                <label>Register Number</label>

                <input type="text"
                       name="register_no"
                       required>

                <label>Select Event</label>

                <select name="event_id" required>

                    <option value="">
                        Select Event
                    </option>
    """

    for event in events_list:

        html += f"""
                    <option value="{event['id']}">
                        {event['name']} - {event['date']}
                    </option>
        """

    html += """

                </select>

                <button type="submit">
                    Register
                </button>

            </form>

        </div>

        <h2>Registered Students</h2>

        <table>

            <tr>
                <th>Student Name</th>
                <th>Register Number</th>
                <th>Event</th>
            </tr>
    """

    for registration in registrations_list:

        html += f"""

            <tr>

                <td>
                    {registration['student_name']}
                </td>

                <td>
                    {registration['register_no']}
                </td>

                <td>
                    {registration['event_name'] or '-'}
                </td>

            </tr>
        """

    html += "</table>" + HTML_END

    return render_template_string(html)


@app.route("/register-event", methods=["POST"])
def register_event():

    student_name = request.form["student_name"]
    register_no = request.form["register_no"]
    event_id = request.form["event_id"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO event_registrations
        (student_name, register_no, event_id)
        VALUES (?, ?, ?)
        """,
        (student_name, register_no, event_id)
    )

    conn.commit()
    conn.close()

    return redirect("/registrations")


# ================= RUN APPLICATION =================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )