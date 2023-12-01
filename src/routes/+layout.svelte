<script lang="js">
	import '../app.css';
	import { page } from '$app/stores';
	import logo from '$lib/logo.svg';
	import clsx from 'clsx';
</script>

<svelte:head>
	<script type="text/javascript">
		(function (window, document, dataLayerName, id) {
			(window[dataLayerName] = window[dataLayerName] || []),
				window[dataLayerName].push({ start: new Date().getTime(), event: 'stg.start' });
			var scripts = document.getElementsByTagName('script')[0],
				tags = document.createElement('script');
			function stgCreateCookie(a, b, c) {
				var d = '';
				if (c) {
					var e = new Date();
					e.setTime(e.getTime() + 24 * c * 60 * 60 * 1e3), (d = '; expires=' + e.toUTCString());
				}
				document.cookie = a + '=' + b + d + '; path=/';
			}
			var isStgDebug =
				(window.location.href.match('stg_debug') || document.cookie.match('stg_debug')) &&
				!window.location.href.match('stg_disable_debug');
			stgCreateCookie('stg_debug', isStgDebug ? 1 : '', isStgDebug ? 14 : -1);
			var qP = [];
			dataLayerName !== 'dataLayer' && qP.push('data_layer_name=' + dataLayerName),
				isStgDebug && qP.push('stg_debug');
			var qPString = qP.length > 0 ? '?' + qP.join('&') : '';
			(tags.async = !0),
				(tags.src = '//statistiek.rijksoverheid.nl/containers/' + id + '.js' + qPString),
				scripts.parentNode.insertBefore(tags, scripts);
			!(function (a, n, i) {
				a[n] = a[n] || {};
				for (var c = 0; c < i.length; c++)
					!(function (i) {
						(a[n][i] = a[n][i] || {}),
							(a[n][i].api =
								a[n][i].api ||
								function () {
									var a = [].slice.call(arguments, 0);
									'string' == typeof a[0] &&
										window[dataLayerName].push({
											event: n + '.' + i + ':' + a[0],
											parameters: [].slice.call(arguments, 1)
										});
								});
					})(i[c]);
			})(window, 'ppms', ['tm', 'cm']);
		})(window, document, 'dataLayer', '5f6027e9-9dd3-45b2-afbf-2b54ceee73d2');
	</script><noscript
		><iframe
			title="pbl traffic monitor"
			src="//statistiek.rijksoverheid.nl/containers/5f6027e9-9dd3-45b2-afbf-2b54ceee73d2/noscript.html"
			height="0"
			width="0"
			style="display:none;visibility:hidden"
		/></noscript
	>
</svelte:head>

<div class=" flex h-screen flex-col overflow-auto" data-theme="mytheme">
	<div class="navbar bg-primary text-neutral-content">
		<div class="flex-1">
			<a href={`/${$page.url.search}`} class="btn-ghost btn text-xl normal-case"
				><img
					style="filter: invert(1);"
					src={logo}
					class="h-full text-current"
					alt="Logo for Carbon Budget Explorer"
				/> Carbon Budget Explorer</a
			>
		</div>
		<div class="alert" style="width: 50%">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				class="h-6 w-6 shrink-0 stroke-current"
				><path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
				/></svg
			>
			<span
				>This website is currently in beta and is subject to frequent updates. Please see the About
				page for more information</span
			>
		</div>
		<div class="flex-none">
			<a href="/about" class="btn-ghost btn-square btn px-10">About</a>
		</div>
	</div>
	<div class={clsx($page.url.pathname === '/', 'flex-1 bg-base-100 p-4')}>
		<slot />
	</div>
</div>
