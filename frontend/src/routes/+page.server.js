import * as api from '$lib/api';
import { page_size } from '$lib/constants';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, url }) {
	// const tab = url.searchParams.get('tab') || 'all';
	// const tag = url.searchParams.get('tag');
	const page = +(url.searchParams.get('page') ?? '1');
	const searchTerm = url.searchParams.get('search');

	// const endpoint = tab === 'feed' ? 'articles/feed' : 'articles';

	const q = new URLSearchParams();

	q.set('page', page);
	if (searchTerm) q.set('search_term', searchTerm);
	// q.set('offset', (page - 1) * page_size);
	// if (tag) q.set('tag', tag);

	// const [{ articles, articlesCount }] = await Promise.all([
		// api.get(`${endpoint}?${q}`, locals.user?.token),
		// api.get('tags')
	// ]);

	const {publications, total_pages, total_publications } = await api.get(`get_publications?${q}`);
	const tags = [];

	return {
		publications,
		pages: total_pages,
		tags
	};
}

/** @type {import('./$types').Actions} */
export const actions = {
	createPublication: async ({ locals, params, request }) => {
		// if (!locals.user) error(401);

		const data = await request.formData();

		try {
			const response = await api.post(`create_publication`,
				{
						title: data.get('title'),
						content: data.get('content'),
						username: data.get('username'),
						email: data.get('email'),
						// tagList: data.get('tagList').split(' ')

				},
				// locals.user.token			
			);
			return {success: "Publication was created successfully"};
		} catch (e) {
			return {error: "Username or email are in use"}
		}
	},
}