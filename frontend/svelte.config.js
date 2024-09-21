//import adapter from '@sveltejs/adapter-vercel';
import adapter from '@sveltejs/adapter-node';


/** @type {import('@sveltejs/kit').Config} */
export default {
	kit: {
		// adapter: adapter({ runtime: 'edge' })
		adapter: adapter()
	}
};
