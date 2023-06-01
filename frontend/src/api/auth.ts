import axios from "../utils/axios";
import { JWTLoginResponseType } from "../types";

async function login(
  username: string,
  password: string
): Promise<JWTLoginResponseType> {
  const { data } = await axios.post<JWTLoginResponseType>(
    "/api/v1/accounts/jwt/",
    {
      username: username,
      password: password,
    }
  );

  return data;
}

async function jwtVerify(token: string): Promise<boolean> {
  const { status } = await axios.post("/api/v1/accounts/jwt/verify/", {
    token: token,
  });

  return status === 200 ? true : false;
}

const authApi = {
  login,
  jwtVerify,
};

export default authApi;
