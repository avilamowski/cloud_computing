// @ts-nocheck
import { fail, redirect } from '@sveltejs/kit';
import * as api from '$lib/api.js';

/** @param {Parameters<import('./$types').PageServerLoad>[0]} event */
export async function load({ locals }) {
	if (locals.user) redirect(307, '/');
}

/** */
export const actions = {
	default:/** @param {import('./$types').RequestEvent} event */  async ({ cookies, request }) => {
		const data = await request.formData();

		const body = await api.post('users/login', {
			user: {
				email: data.get('email'),
				password: data.get('password')
			}
		});

		if (body.errors) {
			return fail(401, body);
		}

		const value = btoa(JSON.stringify(body.user));
		cookies.set('jwt', value, { path: '/' });

		redirect(307, '/');
	}
};
