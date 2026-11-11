const trimTrailingSlashes = (value) => value.replace(/\/+$/, "");

export const API_BASE_URL = trimTrailingSlashes(
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8080/api",
);

export const AI_CHAT_URL =
  import.meta.env.VITE_AI_CHAT_URL || "http://localhost:8000/chat";
