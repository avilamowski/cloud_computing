export { matchers } from './matchers.js';

export const nodes = [
	() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9'),
	() => import('./nodes/10'),
	() => import('./nodes/11'),
	() => import('./nodes/12')
];

export const server_loads = [0,2];

export const dictionary = {
		"/": [~3],
		"/article/[slug]": [~4],
		"/editor": [~5],
		"/editor/[slug]": [~6],
		"/login": [~7],
		"/profile": [8],
		"/profile/@[user]": [~9,[2]],
		"/profile/@[user]/favorites": [~10,[2]],
		"/register": [~11],
		"/settings": [~12]
	};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),

	reroute: (() => {})
};

export { default as root } from '../root.svelte';