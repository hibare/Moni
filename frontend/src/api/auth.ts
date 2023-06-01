import axios from "../utils/axios";
import { AccountType, JWTLoginResponseType, PasswordType } from "../types";

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

async function patchAccount(account: AccountType): Promise<AccountType> {
  const { data } = await axios.patch<AccountType>("/api/v1/accounts/", account);
  return data;
}

async function changePassword(password: PasswordType): Promise<void> {
  await axios.put("/api/v1/accounts/password/", password);
}

const authApi = {
  login,
  jwtVerify,
  patchAccount,
  changePassword,
};

export default authApi;
