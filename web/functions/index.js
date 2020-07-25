const functions = require('firebase-functions');
const express = require('express');
const app = express();
const firebase = require("firebase");
require("firebase/firestore");
require('dotenv').config();

firebase.initializeApp({
    apiKey: process.env['API_KEY'],
    authDomain: process.env['AUTH_DOMAIN'],
    databaseURL: process.env['DATABASE_URL'],
    projectId: process.env['PROJECT_ID'],
    storageBucket: process.env['STORAGE_BUCKET'],
    messagingSenderId: process.env['MESSAGING_SENDER_ID'],
    appId: process.env['APP_ID'],
    measurementId: process.env['MEASUREMENT_ID']
});

var db = firebase.firestore();

app.get('/leaderboard', (req, res) => {
    res.sendFile('views/leaderboard.html', { root: __dirname });
});

app.get('/submissions', (req, res) => {

    res.sendFile('views/submissions.html', { root: __dirname });
});

exports.app = functions.https.onRequest(app);
