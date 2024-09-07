// @ts-nocheck
import { get_articles } from '../get_articles';

/** @param {Parameters<import('./$types').PageServerLoad>[0]} event */
export async function load(event) {
	const { articles, page } = await get_articles(event, 'favorited');
	return { articles, page };
}
