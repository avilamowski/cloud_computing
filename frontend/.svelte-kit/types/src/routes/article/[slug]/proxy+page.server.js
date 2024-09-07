// @ts-nocheck
import * as api from '$lib/api.js';
import { error, redirect } from '@sveltejs/kit';
import { marked } from 'marked';
import sanitizeHtml from 'sanitize-html';

/** @param {Parameters<import('./$types').PageServerLoad>[0]} event */
export async function load({ locals, params }) {
	const [{ article }, { comments }] = await Promise.all([
		api.get(`articles/${params.slug}`, locals.user?.token),
		api.get(`articles/${params.slug}/comments`, locals.user?.token)
	]);

	const dirty = marked(article.body);
	article.body = sanitizeHtml(dirty);

	return { article, comments };
}

/** */
export const actions = {
	createComment:/** @param {import('./$types').RequestEvent} event */  async ({ locals, params, request }) => {
		if (!locals.user) error(401);

		const data = await request.formData();

		await api.post(
			`articles/${params.slug}/comments`,
			{
				comment: {
					body: data.get('comment')
				}
			},
			locals.user.token
		);
	},

	deleteComment:/** @param {import('./$types').RequestEvent} event */  async ({ locals, params, url }) => {
		if (!locals.user) error(401);

		const id = url.searchParams.get('id');
		const result = await api.del(`articles/${params.slug}/comments/${id}`, locals.user.token);

		if (result.error) error(result.status, result.error);
	},

	deleteArticle:/** @param {import('./$types').RequestEvent} event */  async ({ locals, params }) => {
		if (!locals.user) error(401);

		await api.del(`articles/${params.slug}`, locals.user.token);
		redirect(307, '/');
	},

	toggleFavorite:/** @param {import('./$types').RequestEvent} event */  async ({ locals, params, request }) => {
		if (!locals.user) error(401);

		const data = await request.formData();
		const favorited = data.get('favorited') !== 'on';

		if (favorited) {
			api.post(`articles/${params.slug}/favorite`, null, locals.user.token);
		} else {
			api.del(`articles/${params.slug}/favorite`, locals.user.token);
		}

		redirect(307, request.headers.get('referer') ?? `/article/${params.slug}`);
	}
};
