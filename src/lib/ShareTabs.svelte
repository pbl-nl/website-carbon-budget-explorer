<script lang="ts">
	import { clsx } from 'clsx';
	import { page } from '$app/stores';
</script>

<div class="tabs">
	<a
		href={`/global${$page.url.search}`}
		class={clsx(
			'tab-lifted tab tab-lg text-xl font-bold text-gray-700',
			$page.url.pathname === '/global' && 'tab-active'
		)}
		><svg class="mr-4" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
			><path
				fill="currentColor"
				d="m3.5 6.5l6 6.01l4-4L22 17.08l-1.41 1.41l-7.09-7.97l-4 4L2 7.01z"
			/></svg
		>
		Global budget</a
	>
	<a
		href={`/map${$page.url.search}`}
		class={clsx(
			'tab-lifted tab tab-lg text-xl font-bold text-gray-700',
			$page.url.pathname === '/map' && 'tab-active'
		)}
		><svg class="mr-4" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
			><g
				fill="none"
				stroke="currentColor"
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				><path d="M21 12a9 9 0 1 0-9 9M3.6 9h16.8M3.6 15h7.9" /><path
					d="M11.5 3a17 17 0 0 0 0 18m1-18a16.984 16.984 0 0 1 2.574 8.62M15 18a3 3 0 1 0 6 0a3 3 0 1 0-6 0m5.2 2.2L22 22"
				/></g
			></svg
		>World map with shares</a
	>
</div>
