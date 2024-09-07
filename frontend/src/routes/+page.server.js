import * as api from '$lib/api';
import { page_size } from '$lib/constants';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, url }) {
	const tab = url.searchParams.get('tab') || 'all';
	const tag = url.searchParams.get('tag');
	const page = +(url.searchParams.get('page') ?? '1');

	// const endpoint = tab === 'feed' ? 'articles/feed' : 'articles';

	const q = new URLSearchParams();

	q.set('limit', page_size);
	q.set('offset', (page - 1) * page_size);
	if (tag) q.set('tag', tag);

	// const [{ articles, articlesCount }] = await Promise.all([
		// api.get(`${endpoint}?${q}`, locals.user?.token),
		// api.get('tags')
	// ]);

	const publications = await api.get(`publications`);
	console.log(publications);
	const tags = [];

	return {
		publications,
		pages: Math.ceil(publications.length / page_size),
		tags
	};
}
