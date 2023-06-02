import { APITokenType } from "../types";
import axios from "../utils/axios";

async function getAPIToken(): Promise<APITokenType> {
  const { data } = await axios.get<APITokenType>("/api/v1/accounts/token/");
  return data;
}

async function regenerateAPIToken(): Promise<APITokenType> {
  const { data } = await axios.put<APITokenType>("/api/v1/accounts/token/");
  return data;
}

async function deleteAPIToken(): Promise<void> {
  await axios.delete("/api/v1/accounts/token");
}

const tokenApi = {
  getAPIToken,
  regenerateAPIToken,
  deleteAPIToken,
};

export default tokenApi;
