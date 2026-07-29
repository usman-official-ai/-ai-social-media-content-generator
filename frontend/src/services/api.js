import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const client = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 45000,
});

function unwrapError(error) {
  const detail = error?.response?.data?.detail;
  return new Error(
    typeof detail === "string"
      ? detail
      : "Something went wrong talking to the API. Is the backend running?"
  );
}

export async function generateContent(businessInfo) {
  try {
    // FIXED: Changed from /generate-content to /content/generate
    const { data } = await client.post("/content/generate", businessInfo);
    return data;
  } catch (error) {
    throw unwrapError(error);
  }
}

export async function generateHashtags(businessInfo) {
  try {
    const { data } = await client.post("/hashtags/generate", {
      industry: businessInfo.industry,
      business_name: businessInfo.business_name,
      target_audience: businessInfo.target_audience,
    });
    return data;
  } catch (error) {
    throw unwrapError(error);
  }
}

export async function generateCalendar(businessInfo, days) {
  try {
    const { data } = await client.post("/calendar/generate", {
      days: days,
    });
    return data;
  } catch (error) {
    throw unwrapError(error);
  }
}

export async function generateKeywords(businessInfo) {
  try {
    const { data } = await client.post("/extras/seo-keywords", {
      business_name: businessInfo.business_name,
      industry: businessInfo.industry,
      product_service: businessInfo.product_service,
    });
    return data;
  } catch (error) {
    throw unwrapError(error);
  }
}

export async function bestPostingTime(platform) {
  try {
    const { data } = await client.post("/extras/posting-time", { 
      platform: platform 
    });
    return data;
  } catch (error) {
    throw unwrapError(error);
  }
}

export default client;