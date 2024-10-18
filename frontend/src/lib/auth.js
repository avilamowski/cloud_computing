import { PUBLIC_COGNITO_APP_CLIENT_ID, PUBLIC_COGNITO_URL, PUBLIC_REDIRECT_URL } from '$env/static/public';
import { getTokens } from "../server/helpers";
import { error, redirect } from "@sveltejs/kit";

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