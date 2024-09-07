// @ts-nocheck
import * as api from '$lib/api.js';
import { error, fail } from '@sveltejs/kit';
import { get_articles } from './get_articles';

/** @param {Parameters<import('./$types').PageServerLoad>[0]} event */
export async function load(event) {
	const { articles, page } = await get_articles(event, 'author');
	return { articles, page };
}

/** */
export const actions = {
	toggleFollow:/** @param {import('./$types').RequestEvent} event */  async ({ locals, params, request }) => {
		if (!locals.user) error(401);

		const data = await request.formData();
		const following = data.get('following') !== 'on';

		const result = following
			? await api.post(`profiles/${params.user}/follow`, null, locals.user.token)
			: await api.del(`profiles/${params.user}/follow`, locals.user.token);

		if (result.errors) {
			return fail(422, result);
		}
	}
};
