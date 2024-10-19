import { error } from '@sveltejs/kit';
import { PUBLIC_BASE_PATH, PUBLIC_COGNITO_APP_CLIENT_ID, PUBLIC_COGNITO_URL, PUBLIC_REDIRECT_URL } from '$env/static/public';
import { isLoading } from '../routes/store';

// const base = 'https://api.realworld.io/api';
// const base = 'https://0lhje3xjl2.execute-api.us-east-1.amazonaws.com/default/';
const base = PUBLIC_BASE_PATH;
const cognitoAppClientId = PUBLIC_COGNITO_APP_CLIENT_ID;
const cognitoUrl = PUBLIC_COGNITO_URL;
const redirectUrl = PUBLIC_REDIRECT_URL;

async function send({ method, path, data}) {
  const opts = { method, headers: {} };

  if (data) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(data);
  }

  const token = localStorage.getItem("token");
  if (token) {
    opts.headers["Authorization"] = `Bearer ${token}`;
  }

  isLoading.set(true);
  let res;
  try {
    res = await fetch(`${base}/${path}`, opts);
  } catch (err) {
    throw err;
  } finally {
    isLoading.set(false);
  }

  if (res.ok || res.status === 422) {
    const text = await res.text();
    return text ? JSON.parse(text) : {};
  }

  error(res.status);
}
	
export function get(path) {
	return send({ method: 'GET', path});
}

export function del(path) {
	return send({ method: 'DELETE', path});
}

export function post(path, data) {
	return send({ method: 'POST', path, data});
}

export function put(path, data) {
	return send({ method: 'PUT', path, data});
}

export function getSignInUrl() {

	// The login api endpoint with the required parameters.
	const loginUrl = new URL("/login", cognitoUrl);
	loginUrl.searchParams.set("response_type", "code");
	loginUrl.searchParams.set("client_id", cognitoAppClientId);
	loginUrl.searchParams.set("redirect_uri", redirectUrl);
	loginUrl.searchParams.set("scope", "email openid");

	return loginUrl.toString();
}

export function getRegisterUrl() {

	// The login api endpoint with the required parameters.
	const loginUrl = new URL("/signup", cognitoUrl);
	loginUrl.searchParams.set("response_type", "code");
	loginUrl.searchParams.set("client_id", cognitoAppClientId);
	loginUrl.searchParams.set("redirect_uri", redirectUrl);
	loginUrl.searchParams.set("scope", "email openid");

	return loginUrl.toString();
}

export function getSignOutUrl() {

	const logoutUrl = new URL("/logout", cognitoUrl);
	logoutUrl.searchParams.set("response_type", "code");
	logoutUrl.searchParams.set("client_id", cognitoAppClientId);
	logoutUrl.searchParams.set("redirect_uri", redirectUrl);

	return logoutUrl.toString();
}
