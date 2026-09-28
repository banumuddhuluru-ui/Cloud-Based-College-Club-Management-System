// =====================================================
// FIREBASE CONFIGURATION
// =====================================================

import { initializeApp }
from "https://www.gstatic.com/firebasejs/12.19.0/firebase-app.js";

import { getAnalytics }
from "https://www.gstatic.com/firebasejs/12.19.0/firebase-analytics.js";

import {
    getDatabase,
    ref,
    push,
    set,
    onValue,
    remove
}
from "https://www.gstatic.com/firebasejs/12.19.0/firebase-database.js";


// =====================================================
// YOUR FIREBASE CONFIGURATION
// =====================================================

const firebaseConfig = {

    apiKey:
        "AIzaSyD5EM5GF91uD6xRQF0k1IU7IcfI5WmhN0Q",

    authDomain:
        "club-management-system-2ad1e.firebaseapp.com",

    databaseURL:
        "https://club-management-system-2ad1e-default-rtdb.asia-southeast1.firebasedatabase.app",

    projectId:
        "club-management-system-2ad1e",

    storageBucket:
        "club-management-system-2ad1e.firebasestorage.app",

    messagingSenderId:
        "517384101314",

    appId:
        "1:517384101314:web:44633fcbc1d932db664a5b",

    measurementId:
        "G-1Q99FX9J16"
};


// =====================================================
// INITIALIZE FIREBASE
// =====================================================

const app = initializeApp(firebaseConfig);


// Firebase Analytics

const analytics = getAnalytics(app);


// Firebase Realtime Database

const db = getDatabase(app);


console.log("Firebase connected successfully!");


// =====================================================
// DATA
// =====================================================

let clubs = [];

let members = [];

let events = [];

let registrations = [];


// =====================================================
// PAGE NAVIGATION
// =====================================================

window.showPage = function(pageId) {

    const pages =
        document.querySelectorAll(".page");

    pages.forEach(function(page) {

        page.classList.add("hidden");

    });

    document
        .getElementById(pageId)
        .classList.remove("hidden");

    updateDashboard();

};


// =====================================================
// ADD CLUB
// =====================================================

window.addClub = async function() {

    const name =
        document
            .getElementById("clubName")
            .value
            .trim();

    const category =
        document
            .getElementById("clubCategory")
            .value
            .trim();

    const coordinator =
        document
            .getElementById("clubCoordinator")
            .value
            .trim();

    const description =
        document
            .getElementById("clubDescription")
            .value
            .trim();


    if (name === "") {

        alert("Please enter club name.");

        return;

    }


    try {

        const clubRef =
            push(ref(db, "clubs"));


        await set(clubRef, {

            name: name,

            category: category,

            coordinator: coordinator,

            description: description

        });


        document.getElementById(
            "clubName"
        ).value = "";

        document.getElementById(
            "clubCategory"
        ).value = "";

        document.getElementById(
            "clubCoordinator"
        ).value = "";

        document.getElementById(
            "clubDescription"
        ).value = "";


        alert("Club added successfully!");

    }

    catch (error) {

        console.error(error);

        alert(
            "Error adding club: " +
            error.message
        );

    }

};


// =====================================================
// LOAD CLUBS
// =====================================================

onValue(
    ref(db, "clubs"),
    function(snapshot) {

        clubs = [];

        const data = snapshot.val();


        if (data) {

            Object.keys(data).forEach(
                function(id) {

                    clubs.push({

                        id: id,

                        name:
                            data[id].name,

                        category:
                            data[id].category,

                        coordinator:
                            data[id].coordinator,

                        description:
                            data[id].description

                    });

                }
            );

        }


        displayClubs();

        updateClubDropdowns();

        updateDashboard();

    }
);


// =====================================================
// DISPLAY CLUBS
// =====================================================

function displayClubs() {

    const list =
        document.getElementById("clubList");


    list.innerHTML = "";


    clubs.forEach(function(club) {

        list.innerHTML += `

            <div class="item">

                <h2>
                    ${club.name}
                </h2>

                <p>
                    <b>Category:</b>
                    ${club.category || "-"}
                </p>

                <p>
                    <b>Coordinator:</b>
                    ${club.coordinator || "-"}
                </p>

                <p>
                    ${club.description || "No description"}
                </p>

                <button
                    class="delete"
                    onclick="deleteClub('${club.id}')">

                    Delete

                </button>

            </div>

        `;

    });

}


// =====================================================
// DELETE CLUB
// =====================================================

window.deleteClub = async function(id) {

    try {

        await remove(
            ref(db, "clubs/" + id)
        );

        alert("Club deleted successfully!");

    }

    catch (error) {

        console.error(error);

        alert(
            "Error deleting club: " +
            error.message
        );

    }

};


// =====================================================
// UPDATE CLUB DROPDOWNS
// =====================================================

function updateClubDropdowns() {

    const memberClub =
        document.getElementById("memberClub");

    const eventClub =
        document.getElementById("eventClub");


    memberClub.innerHTML =
        `<option value="">
            Select Club
        </option>`;


    eventClub.innerHTML =
        `<option value="">
            Select Club
        </option>`;


    clubs.forEach(function(club) {

        memberClub.innerHTML += `

            <option value="${club.id}">
                ${club.name}
            </option>

        `;


        eventClub.innerHTML += `

            <option value="${club.id}">
                ${club.name}
            </option>

        `;

    });

}


// =====================================================
// ADD MEMBER
// =====================================================

window.addMember = async function() {

    const name =
        document
            .getElementById("memberName")
            .value
            .trim();

    const registerNumber =
        document
            .getElementById("registerNumber")
            .value
            .trim();

    const department =
        document
            .getElementById("department")
            .value
            .trim();

    const email =
        document
            .getElementById("email")
            .value
            .trim();

    const clubId =
        document
            .getElementById("memberClub")
            .value;


    if (
        name === "" ||
        registerNumber === "" ||
        clubId === ""
    ) {

        alert(
            "Please fill the required details."
        );

        return;

    }


    try {

        const memberRef =
            push(ref(db, "members"));


        await set(memberRef, {

            name: name,

            registerNumber:
                registerNumber,

            department:
                department,

            email:
                email,

            clubId:
                clubId

        });


        document.getElementById(
            "memberName"
        ).value = "";

        document.getElementById(
            "registerNumber"
        ).value = "";

        document.getElementById(
            "department"
        ).value = "";

        document.getElementById(
            "email"
        ).value = "";

        document.getElementById(
            "memberClub"
        ).value = "";


        alert(
            "Member registered successfully!"
        );

    }

    catch (error) {

        console.error(error);

        alert(
            "Error registering member: " +
            error.message
        );

    }

};


// =====================================================
// LOAD MEMBERS
// =====================================================

onValue(
    ref(db, "members"),
    function(snapshot) {

        members = [];

        const data = snapshot.val();


        if (data) {

            Object.keys(data).forEach(
                function(id) {

                    members.push({

                        id: id,

                        name:
                            data[id].name,

                        registerNumber:
                            data[id].registerNumber,

                        department:
                            data[id].department,

                        email:
                            data[id].email,

                        clubId:
                            data[id].clubId

                    });

                }
            );

        }


        displayMembers();

        updateDashboard();

    }
);


// =====================================================
// DISPLAY MEMBERS
// =====================================================

function displayMembers() {

    const list =
        document.getElementById("memberList");


    list.innerHTML = "";


    members.forEach(function(member) {

        const club =
            clubs.find(function(c) {

                return String(c.id) ===
                    String(member.clubId);

            });


        list.innerHTML += `

            <div class="item">

                <h2>
                    ${member.name}
                </h2>

                <p>
                    <b>Register Number:</b>
                    ${member.registerNumber}
                </p>

                <p>
                    <b>Department:</b>
                    ${member.department || "-"}
                </p>

                <p>
                    <b>Email:</b>
                    ${member.email || "-"}
                </p>

                <p>
                    <b>Club:</b>
                    ${club ? club.name : "-"}
                </p>

                <button
                    class="delete"
                    onclick="deleteMember('${member.id}')">

                    Delete

                </button>

            </div>

        `;

    });

}


// =====================================================
// DELETE MEMBER
// =====================================================

window.deleteMember = async function(id) {

    try {

        await remove(
            ref(db, "members/" + id)
        );

        alert(
            "Member deleted successfully!"
        );

    }

    catch (error) {

        console.error(error);

        alert(
            "Error deleting member: " +
            error.message
        );

    }

};


// =====================================================
// ADD EVENT
// =====================================================

window.addEvent = async function() {

    const name =
        document
            .getElementById("eventName")
            .value
            .trim();

    const date =
        document
            .getElementById("eventDate")
            .value;

    const venue =
        document
            .getElementById("eventVenue")
            .value
            .trim();

    const clubId =
        document
            .getElementById("eventClub")
            .value;

    const description =
        document
            .getElementById("eventDescription")
            .value
            .trim();


    if (
        name === "" ||
        date === "" ||
        clubId === ""
    ) {

        alert(
            "Please enter event name, date and club."
        );

        return;

    }


    try {

        const eventRef =
            push(ref(db, "events"));


        await set(eventRef, {

            name: name,

            date: date,

            venue: venue,

            clubId: clubId,

            description: description

        });


        document.getElementById(
            "eventName"
        ).value = "";

        document.getElementById(
            "eventDate"
        ).value = "";

        document.getElementById(
            "eventVenue"
        ).value = "";

        document.getElementById(
            "eventClub"
        ).value = "";

        document.getElementById(
            "eventDescription"
        ).value = "";


        alert(
            "Event created successfully!"
        );

    }

    catch (error) {

        console.error(error);

        alert(
            "Error creating event: " +
            error.message
        );

    }

};


// =====================================================
// LOAD EVENTS
// =====================================================

onValue(
    ref(db, "events"),
    function(snapshot) {

        events = [];

        const data = snapshot.val();


        if (data) {

            Object.keys(data).forEach(
                function(id) {

                    events.push({

                        id: id,

                        name:
                            data[id].name,

                        date:
                            data[id].date,

                        venue:
                            data[id].venue,

                        clubId:
                            data[id].clubId,

                        description:
                            data[id].description

                    });

                }
            );

        }


        displayEvents();

        updateEventDropdown();

        updateDashboard();

    }
);


// =====================================================
// DISPLAY EVENTS
// =====================================================

function displayEvents() {

    const list =
        document.getElementById("eventList");


    list.innerHTML = "";


    events.forEach(function(event) {

        const club =
            clubs.find(function(c) {

                return String(c.id) ===
                    String(event.clubId);

            });


        list.innerHTML += `

            <div class="item">

                <h2>
                    ${event.name}
                </h2>

                <p>
                    <b>Club:</b>
                    ${club ? club.name : "-"}
                </p>

                <p>
                    <b>Date:</b>
                    ${event.date}
                </p>

                <p>
                    <b>Venue:</b>
                    ${event.venue || "-"}
                </p>

                <p>
                    ${event.description || "No description"}
                </p>

                <button
                    class="delete"
                    onclick="deleteEvent('${event.id}')">

                    Delete

                </button>

            </div>

        `;

    });

}


// =====================================================
// DELETE EVENT
// =====================================================

window.deleteEvent = async function(id) {

    try {

        await remove(
            ref(db, "events/" + id)
        );

        alert(
            "Event deleted successfully!"
        );

    }

    catch (error) {

        console.error(error);

        alert(
            "Error deleting event: " +
            error.message
        );

    }

};


// =====================================================
// UPDATE EVENT DROPDOWN
// =====================================================

function updateEventDropdown() {

    const select =
        document.getElementById(
            "registrationEvent"
        );


    select.innerHTML =
        `<option value="">
            Select Event
        </option>`;


    events.forEach(function(event) {

        select.innerHTML += `

            <option value="${event.id}">

                ${event.name} - ${event.date}

            </option>

        `;

    });

}


// =====================================================
// REGISTER FOR EVENT
// =====================================================

window.registerEvent = async function() {

    const name =
        document
            .getElementById("registrationName")
            .value
            .trim();

    const registerNumber =
        document
            .getElementById("registrationNumber")
            .value
            .trim();

    const eventId =
        document
            .getElementById("registrationEvent")
            .value;


    if (
        name === "" ||
        registerNumber === "" ||
        eventId === ""
    ) {

        alert(
            "Please fill all details."
        );

        return;

    }


    try {

        const registrationRef =
            push(
                ref(
                    db,
                    "registrations"
                )
            );


        await set(
            registrationRef,
            {

                studentName:
                    name,

                registerNumber:
                    registerNumber,

                eventId:
                    eventId

            }
        );


        document.getElementById(
            "registrationName"
        ).value = "";

        document.getElementById(
            "registrationNumber"
        ).value = "";

        document.getElementById(
            "registrationEvent"
        ).value = "";


        alert(
            "Event registration successful!"
        );

    }

    catch (error) {

        console.error(error);

        alert(
            "Error registering for event: " +
            error.message
        );

    }

};


// =====================================================
// LOAD REGISTRATIONS
// =====================================================

onValue(
    ref(db, "registrations"),
    function(snapshot) {

        registrations = [];

        const data = snapshot.val();


        if (data) {

            Object.keys(data).forEach(
                function(id) {

                    registrations.push({

                        id: id,

                        studentName:
                            data[id].studentName,

                        registerNumber:
                            data[id].registerNumber,

                        eventId:
                            data[id].eventId

                    });

                }
            );

        }


        displayRegistrations();

        updateDashboard();

    }
);


// =====================================================
// DISPLAY REGISTRATIONS
// =====================================================

function displayRegistrations() {

    const list =
        document.getElementById(
            "registrationList"
        );


    list.innerHTML = "";


    registrations.forEach(
        function(registration) {

            const event =
                events.find(function(e) {

                    return String(e.id) ===
                        String(
                            registration.eventId
                        );

                });


            list.innerHTML += `

                <div class="item">

                    <h2>
                        ${registration.studentName}
                    </h2>

                    <p>

                        <b>
                            Register Number:
                        </b>

                        ${registration.registerNumber}

                    </p>

                    <p>

                        <b>
                            Event:
                        </b>

                        ${
                            event
                            ? event.name
                            : "-"
                        }

                    </p>

                </div>

            `;

        }
    );

}


// =====================================================
// DASHBOARD
// =====================================================

function updateDashboard() {

    document.getElementById(
        "clubCount"
    ).innerText =
        clubs.length;


    document.getElementById(
        "memberCount"
    ).innerText =
        members.length;


    document.getElementById(
        "eventCount"
    ).innerText =
        events.length;


    document.getElementById(
        "registrationCount"
    ).innerText =
        registrations.length;

}


// =====================================================
// START
// =====================================================

updateDashboard();

updateClubDropdowns();

updateEventDropdown();


console.log(
    "Cloud-Based College Club Management System started!"
);