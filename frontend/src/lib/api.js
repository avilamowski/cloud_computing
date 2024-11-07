import { error } from '@sveltejs/kit';
import { PUBLIC_BASE_PATH } from '$env/static/public';
import { isLoading } from '../routes/store';
import { fetchAuthSession } from "aws-amplify/auth";

// const base = 'https://api.realworld.io/api';
// const base = 'https://0lhje3xjl2.execute-api.us-east-1.amazonaws.com/default/';
const base = PUBLIC_BASE_PATH;

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


export async function isAdmin() {
  const { tokens } = await fetchAuthSession();
  if (tokens && ("cognito:groups" in tokens?.accessToken?.payload ?? {})) {
    console.log(tokens.accessToken.payload["cognito:groups"]);
    return tokens.accessToken.payload["cognito:groups"].includes("admin-group");
  }
  return false;
}
