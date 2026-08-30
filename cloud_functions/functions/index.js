// index.js - Firebase Cloud Functions for MIoT Secure Project

const functions = require("firebase-functions");
const admin = require("firebase-admin");
const crypto = require("crypto");
const express = require("express");
const cors = require("cors");

// Init Firebase
admin.initializeApp();
const db = admin.database();

// Express app
const app = express();
app.use(cors({ origin: true }));
app.use(express.json());

// Load secret from Firebase runtime config
const HMAC_SECRET = functions.config().hmac.secret;

// In-memory nonce tracker (demo only — better use Redis/Firestore)
let usedNonces = new Set();

// Helper: verify HMAC
function verifySignature(payload, sig) {
  const { deviceId, ts, nonce, tempC, hr, spo2 } = payload;
  const canonical = `${deviceId}|${ts}|${nonce}|${tempC}|${hr}|${spo2}`;
  const expected = crypto.createHmac("sha256", HMAC_SECRET)
                         .update(canonical)
                         .digest("hex");
  return sig === expected;
}

// Ingest endpoint
app.post("/ingestReading", async (req, res) => {
  const { deviceId, ts, nonce, tempC, hr, spo2, sig } = req.body;

  if (!deviceId || !ts || !nonce || !sig) {
    return res.status(400).send("Missing fields");
  }

  // Timestamp freshness (±120s)
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - ts) > 120) {
    await db.ref("alerts").push({ deviceId, reason: "timestamp_skew", ts, receivedAt: now });
    return res.status(400).send("Invalid timestamp");
  }

  // Replay protection
  if (usedNonces.has(nonce)) {
    await db.ref("alerts").push({ deviceId, reason: "nonce_replay", nonce, receivedAt: now });
    return res.status(400).send("Replay detected");
  }
  usedNonces.add(nonce);

  // Verify signature
  if (!verifySignature({ deviceId, ts, nonce, tempC, hr, spo2 }, sig)) {
    await db.ref("alerts").push({ deviceId, reason: "bad_signature", ts, receivedAt: now });
    return res.status(401).send("Invalid signature");
  }

  // Store valid reading
  const path = `readings/${deviceId}/${ts}`;
  await db.ref(path).set({ deviceId, ts, nonce, tempC, hr, spo2, receivedAt: now });

  // Basic rule-based anomaly checks
  if (hr < 40 || hr > 160 || tempC < 35 || tempC > 39) {
    await db.ref("alerts").push({ deviceId, reason: "out_of_range", hr, tempC, ts, receivedAt: now });
  }

  return res.status(200).send("OK");
});

// Export as HTTPS Cloud Function
exports.ingestReading = functions.https.onRequest(app);
