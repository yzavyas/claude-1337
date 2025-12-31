<script>
	import { base } from '$app/paths';
</script>

<h2>explore</h2>

<p class="intro">
	Standing on the shoulders of giants. What master craftsmen actually use in production — not catalogs of options, but THE answer for each use case. Evidence over opinion.
</p>

<div class="sections">
	<div class="section">
		<h3><a href="{base}/explore/reference/">reference</a></h3>
		<p>Plugin catalog and research findings. Browse what's available, see the data behind decisions.</p>
	</div>

	<div class="section">
		<h3><a href="{base}/explore/tutorials/">tutorials</a></h3>
		<p>Step-by-step learning. Build your first skill, create a custom plugin.</p>
	</div>

	<div class="section">
		<h3><a href="{base}/explore/how-to/">how-to</a></h3>
		<p>Task-oriented guides. Specific problems, specific solutions.</p>
	</div>

	<div class="section">
		<h3><a href="{base}/explore/explanation/">explanation</a></h3>
		<p>Concepts and architecture. How the system works, why it's built this way.</p>
	</div>
</div>

<style>
	.intro {
		color: var(--fg-dim);
		font-size: 1rem;
		line-height: 1.7;
		margin-bottom: 2.5rem;
		max-width: 60ch;
	}

	.sections {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.section {
		padding-bottom: 1.5rem;
		border-bottom: 1px solid var(--bg-alt);
	}

	.section:last-child {
		border-bottom: none;
	}

	.section h3 {
		margin: 0 0 0.5rem 0;
	}

	.section h3::before {
		content: none;
	}

	.section h3 a {
		color: var(--green);
	}

	.section p {
		margin: 0;
		color: var(--fg-dim);
		font-size: 0.9rem;
	}
</style>
