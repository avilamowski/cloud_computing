import * as api from '$lib/api.js';
import { error, redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, params, url }) {
	const tab = url.searchParams.get('tab') || 'all';
	const tag = url.searchParams.get('tag');
	const page = +(url.searchParams.get('page') ?? '1');
	// const [{ article }, { comments }] = await Promise.all([
	// 	api.get(`articles/${params.slug}`, locals.user?.token),
	// 	api.get(`articles/${params.slug}/comments`, locals.user?.token)
	// ]);

	// const dirty = marked(article.body);
	// article.body = sanitizeHtml(dirty);

	const qPub = new URLSearchParams();
	qPub.set('publication_id', params.slug);
	const { publication } = await api.get(`get_publications?${qPub}`);
	
	const qCom = new URLSearchParams();
	qCom.set('publication_id', params.slug);
	qCom.set('page', page);
	const comments = await api.get(`get_comments?${qCom}`);

	return { publication, comments, tab, tag, page };
}

/** @type {import('./$types').Actions} */
export const actions = {
	createComment: async ({ locals, params, request }) => {
		// if (!locals.user) error(401);

		const data = await request.formData();
		
		try {
			const response = await api.post(`create_comment`,
				{
					username: data.get('username'),
					email: data.get('email'),
					content: data.get('content'),
					publication_id: params.slug
				},
				// locals.user.token			
			);
			return {success: "Comment was created successfully"};
		} catch (e) {
			return {error: "Username or email are already in use"};
		}
	},

	// deleteComment: async ({ locals, params, url }) => {
	// 	if (!locals.user) error(401);

	// 	const id = url.searchParams.get('id');
	// 	const result = await api.del(`articles/${params.slug}/comments/${id}`, locals.user.token);

	// 	if (result.error) error(result.status, result.error);
	// },

	// deleteArticle: async ({ locals, params }) => {
	// 	if (!locals.user) error(401);

	// 	await api.del(`articles/${params.slug}`, locals.user.token);
	// 	redirect(307, '/');
	// },

	// toggleFavorite: async ({ locals, params, request }) => {
	// 	if (!locals.user) error(401);

	// 	const data = await request.formData();
	// 	const favorited = data.get('favorited') !== 'on';

	// 	if (favorited) {
	// 		api.post(`articles/${params.slug}/favorite`, null, locals.user.token);
	// 	} else {
	// 		api.del(`articles/${params.slug}/favorite`, locals.user.token);
	// 	}

	// 	redirect(307, request.headers.get('referer') ?? `/article/${params.slug}`);
	// }
};
