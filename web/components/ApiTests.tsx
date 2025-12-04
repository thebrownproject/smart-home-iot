"use client";
import {
  getMotionData,
  getGasData,
  getRfidScans,
  getAuthorisedCards,
  getAuthorisedCardEntry,
  SensorLogEntry,
  GasAlertEntry,
  RfidScanEntry,
} from "../lib/api";
import { useState, useEffect } from "react";

export default function ApiTests() {
  const [motionData, setMotionData] = useState<SensorLogEntry[]>([]);
  const [gasData, setGasData] = useState<GasAlertEntry[]>([]);
  const [rfidScans, setRfidScans] = useState<RfidScanEntry[]>([]);
  const [authorisedCards, setAuthorisedCards] = useState<
    getAuthorisedCardEntry[]
  >([]);

  useEffect(() => {
    getMotionData().then(setMotionData);
    getGasData().then(setGasData);
    getRfidScans("all").then(setRfidScans);
    getAuthorisedCards("11bfd903-4a2a-4027-9451-2585814b0fba").then(
      setAuthorisedCards
    );
  }, []);

  return (
    <div>
      <h1>API Tests</h1>
      <h2>Motion Data</h2>
      <pre>{JSON.stringify(motionData, null, 2)}</pre>
      <h2>Gas Data</h2>
      <pre>{JSON.stringify(gasData, null, 2)}</pre>
      <h2>RFID Scans</h2>
      <pre>{JSON.stringify(rfidScans, null, 2)}</pre>
      <h2>Authorised Cards</h2>
      <pre>{JSON.stringify(authorisedCards, null, 2)}</pre>
    </div>
  );
}
