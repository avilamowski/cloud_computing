import { error } from '@sveltejs/kit';
import { BASE_PATH, STATE } from '$env/static/private';
// const base = 'https://api.realworld.io/api';
// const base = 'https://0lhje3xjl2.execute-api.us-east-1.amazonaws.com/default/';
const base = BASE_PATH;
async function send({ method, path, data, token }) {
	const opts = { method, headers: {} };
	
	if (data) {
		opts.headers['Content-Type'] = 'application/json';
		opts.body = JSON.stringify(data);
	}
	
	// if (token) {
		// 	opts.headers['Authorization'] = `Token ${token}`;
		// }
		
		const res = await fetch(`${base}/${path}`, opts);
		if (res.ok || res.status === 422) {
			const text = await res.text();
			return text ? JSON.parse(text) : {};
		}
		
		error(res.status);
	}
	
export function get(path, token) {
	console.log(STATE);
	return send({ method: 'GET', path, token });
}

export function del(path, token) {
	return send({ method: 'DELETE', path, token });
}

export function post(path, data, token) {
	return send({ method: 'POST', path, data, token });
}

export function put(path, data, token) {
	return send({ method: 'PUT', path, data, token });
}
