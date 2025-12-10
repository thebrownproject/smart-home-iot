import axios, { AxiosError } from "axios";

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
  device_id: string;
  card_id: string;
  authorised_card_id: string;
  access_result: "granted" | "denied";
  timestamp: string;
};

export type getAuthorisedCardEntry = {
  id: string;
  card_id: string;
  user_id: string;
  is_active: boolean;
  created_at: string;
};

export const getMotionData = async (
  hours: number = 1
): Promise<SensorLogEntry[]> => {
  try {
    const response = await axios.get(
      `${API_URL}/api/sensors/motion?hours=${hours}`
    );
    console.log("Motion data:", response.data);
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

export const getAuthorisedCards = async (
  id: string
): Promise<getAuthorisedCardEntry[]> => {
  try {
    const response = await axios.get(`${API_URL}/AuthorisedCard/${id}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching authorised cards:", error);
    throw error;
  }
};
