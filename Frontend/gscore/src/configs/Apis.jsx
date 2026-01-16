import axios from "axios";

const BASE_URL = "https://g-score-t3np.onrender.com";


const CLIENT_ID = "R9f80lielipFDVbPnJ716chbBkYMSlQi2DlQcQDw";
const CLIENT_SECRET = "vV88G5317CITuPEetv6AFb32Q65iRvEf0qONIZbOCk2PrpN73UmFwXq4umF6lLWNNRrjc53B7ehf68E9MLMtyldcM5hEv6Wlq8og2t3xe4o8eyhEkTd6bU9Sn8Gg9GS4";

export const endpoints = {
    login: "/o/token/",
    register: "/users/",
    profile: "/secure/profile",
    result: "/student-exam-result/",
};

export const loginApi = axios.create({
    baseURL: BASE_URL,
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
    },
});

export const api = axios.create({
    baseURL: BASE_URL,
  });
