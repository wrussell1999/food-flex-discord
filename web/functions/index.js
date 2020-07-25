const functions = require('firebase-functions');
const express = require('express');
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

app.get('/leaderboard', (req, res) => {

    
    res.sendFile('views/leaderboard.html', { root: __dirname });
});

app.get('/submissions', (req, res) => {

    res.sendFile('views/submissions.html', { root: __dirname });
});

exports.app = functions.https.onRequest(app);
