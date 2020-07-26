const functions = require('firebase-functions');
const express = require('express');
const fs = require('fs');
const parse = require('node-html-parser').parse;

const app = express();
const firebase = require("firebase");
require("firebase/firestore");
firebase.initializeApp({
    apiKey: functions.config().creds.api_key,
    authDomain: functions.config().creds.auth_domain,
    databaseURL: functions.config().creds.database_url,
    projectId: functions.config().creds.project_id,
    storageBucket: functions.config().creds.storage_bucket,
    messagingSenderId: functions.config().creds.messaging_sender_id,
    appId: functions.config().creds.app_id,
    measurementId: functions.config().creds.measurement_id
});

var db = firebase.firestore();


app.get('/leaderboard', async (req, res) => {
    const leaderboardIdRef = db.collection("leaderboard").doc("current-leaderboard");
    const idDoc = await leaderboardIdRef.get();
    const leaderboardRef = db.collection("leaderboard").doc(idDoc.data().id);
    const leaderboard = await leaderboardRef.get();
    const data = leaderboard.data();

    fs.readFile('views/leaderboard.html', 'utf8', (err, html) => {
        if (err) {
            throw err;
        }

        var sort_array = [];
        for (var key in data) {
            sort_array.push({ key: key, score: data[key].score, nick: data[key].nick });
        }
        sort_array.sort(function (x, y) { return y.score - x.score });
        
        const root = parse(html);
        const tbody = root.querySelector('tbody');
        for (var i = 0; i < sort_array.length; i++) {
            var item = data[sort_array[i].key];
            const table = `
            <tr>
                <th scope="row">${i + 1}</th>
                <td>${item.nick}</td>
                <td>${item.score}</td>
            </tr>
            </tbody>`
            tbody.appendChild(table);
        }        
        // add term date
        res.status(200).send(root.toString());
    });
});

app.get('/submissions', async (req, res) => {
    const weekRef = db.collection("weekly-data").doc("current-week");
    const weekId = await weekRef.get();
    const currentWeekRef = db.collection("weekly-data").doc(weekId.data().id);
    const currentWeek = await currentWeekRef.get();
    res.sendFile('views/submissions.html', { root: __dirname });
});

exports.app = functions.https.onRequest(app);
