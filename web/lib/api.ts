import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export type SensorLogEntry = {
  id: string;
  device_id: string;
  sensor_type: string;
  value: number;
  timestamp: string;
};

export type GasAlertEntry = {
  id: string;
  deviceId: string;
  sensorValue: number;
  alertStart: string;
  alertEnd: string | null;
};

export type RfidScanEntry = {
  id: string;
  deviceId: string;
  cardId: string;
  authorisedCardId: string | null;
  accessResult: "granted" | "denied";
  username: string | null;
  timestamp: string;
};

export const getMotionData = async (
  hours: number = 1
): Promise<SensorLogEntry[]> => {
  try {
    const response = await axios.get(
      `${API_URL}/api/sensors/motion?hours=${hours}`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching motion data:", error);
    throw error;
  }
};

export const getGasData = async (
  hours: number = 24
): Promise<GasAlertEntry[]> => {
  try {
    const response = await axios.get(
      `${API_URL}/api/sensors/gas?hours=${hours}`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching gas data:", error);
    throw error;
  }
};

export const getRfidScans = async (
  filter: "all" | "success" | "failed"
): Promise<RfidScanEntry[]> => {
  try {
    const response = await axios.get(
      `${API_URL}/api/RfidScans?filter=${filter}`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching RFID scans:", error);
    throw error;
  }
};

export type AuthorisedCardEntry = {
  id: string;
  cardId: string;
  userId: string | null;
  username: string | null;
  isActive: boolean;
  createdAt: string;
};

export const getAuthorisedCards = async (
  cardId: string
): Promise<AuthorisedCardEntry[]> => {
  try {
    const response = await axios.get(`${API_URL}/api/AuthorisedCard/${cardId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching authorised cards:", error);
    throw error;
  }
};
