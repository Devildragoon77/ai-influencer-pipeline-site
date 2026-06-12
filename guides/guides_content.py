# Guide content for the site. Bodies are HTML fragments.

KIT = '<a href="https://lionheart886.gumroad.com/l/ai-influencer-pipeline-kit">AI Influencer Pipeline Kit</a>'
DNA = '<a href="https://lionheart886.gumroad.com/l/reel-dna-extractor">Reel DNA Extractor</a>'

GUIDES = {

"how-to-create-an-ai-influencer": {
"title": "How to Create an AI Influencer in 2026 (Working Architecture, Real Costs)",
"desc": "The full architecture of a working automated AI influencer: persona design, n8n pipeline, official Instagram API, quality control, and what it really costs per month.",
"h1": "How to Create an AI Influencer in 2026",
"cta": f"Skip the 6 months of engineering — the exact production system described here is packaged as the {KIT}.",
"body": """
<p>Most "create an AI influencer" tutorials end at generating a pretty face. This guide covers the part that actually determines success: the production system that posts every day without you, while keeping quality high enough that the account grows.</p>

<h2>The architecture that works</h2>
<p>A sustainable AI influencer is a pipeline with five stages:</p>
<ol>
<li><strong>Research</strong> — scrape benchmark accounts in your niche and extract what makes their top posts work: pose, framing, lighting, color grade. We call this "Visual DNA". Generating from a blank prompt produces generic content; regenerating proven formats produces content that fits what the niche already rewards.</li>
<li><strong>Generation</strong> — an image model with a locked face reference. The single most important asset is one clean, neutral-lit portrait of your persona: every future image is conditioned on it. Identity drift is the #1 quality killer.</li>
<li><strong>Quality control</strong> — an AI gate (we use Claude) judging each generation PASS/FAIL against the spec, with the failure reason fed back into the next attempt. Cap it at 3 attempts. Without this, your feed fills with six-fingered hands.</li>
<li><strong>Human approval</strong> — every item lands in Telegram with approve/reject buttons. This is ~5 minutes a day and it is not optional: unreviewed AI content is how accounts drift into spam patterns and policy trouble.</li>
<li><strong>Publishing</strong> — the official Instagram Graph API with your own Meta developer app. Own-account automation needs no app review. Browser bots get accounts banned; the API does not.</li>
</ol>

<h2>Persona design decisions that matter</h2>
<ul>
<li><strong>Disclose that the persona is AI.</strong> It's Instagram policy, and undisclosed personas lose every brand deal at the due-diligence step. Disclosure costs you nothing with Gen-Z audiences in 2026.</li>
<li><strong>Lock identity to features, not expressions.</strong> Your identity block should describe hair, eyes, skin, build — and let pose, gaze, and expression come from each benchmark photo. Hard-coding an expression makes every post look the same.</li>
<li><strong>Pick a niche with visual formats you can replicate</strong> — fashion, fitness, and lifestyle work because their content is about a person in a scene. Tutorial or talking-head niches don't fit this pipeline.</li>
</ul>

<h2>What it costs (verified June 2026)</h2>
<table>
<tr><th>Item</th><th>Monthly</th></tr>
<tr><td>n8n (self-hosted, the automation engine)</td><td>$0</td></tr>
<tr><td>VPS to run it 24/7 (optional)</td><td>~$6</td></tr>
<tr><td>Claude API (captions, Visual DNA, QC)</td><td>$3–10</td></tr>
<tr><td>Apify (benchmark scraping)</td><td>~$5</td></tr>
<tr><td>Image/video generation credits</td><td>$0–30 depending on cadence and provider</td></tr>
</table>
<p>Total: roughly $15–50/month for a daily-posting account. The expensive part is video (reels) — see our <a href="kling-motion-control-guide.html">Kling motion control guide</a> for those numbers.</p>

<h2>Timeline expectations</h2>
<p>Setup: a weekend if you're technical. Growth: months — automation solves production, not audience. The accounts that win treat the pipeline as a consistency machine: it never misses a posting day, never burns out, and frees your human hours for the things automation can't do (niche choices, collabs, brand outreach).</p>
"""},

"instagram-graph-api-auto-posting": {
"title": "Auto-Posting to Instagram with the Official Graph API and n8n (2026)",
"desc": "How to publish posts, stories, and reels to Instagram automatically using the official Graph API and n8n — token setup, the two-step publish flow, and the gotchas.",
"h1": "Auto-Posting to Instagram with the Graph API + n8n",
"cta": f"All of this is prebuilt in the {KIT} — 13 import-ready n8n workflows including publishers for posts, stories, and reels.",
"body": """
<p>You do not need a third-party scheduling tool or a sketchy browser bot to auto-post to Instagram. The official Graph API handles posts, stories, and reels — free, allowed, and reliable. Here's the working setup.</p>

<h2>Prerequisites</h2>
<ul>
<li>An Instagram <strong>professional</strong> account (creator or business) linked to a Facebook Page</li>
<li>A Meta developer app with the Instagram-Login flavor and the "Manage messaging & content" use case</li>
<li>A long-lived access token with <code>instagram_business_basic</code> and <code>instagram_business_content_publish</code></li>
</ul>
<p>Two facts that save hours: tokens of this app flavor call <code>graph.instagram.com</code> (not graph.facebook.com), and own-account automation works with standard access — <strong>no Meta app review needed</strong>.</p>

<h2>The two-step publish flow</h2>
<p>Publishing is always: create a media container, then publish it.</p>
<pre><code>POST https://graph.instagram.com/v23.0/{ig-user-id}/media
     ?image_url={public-url}&caption={caption}&access_token={token}
# returns {"id": "container-id"}

POST https://graph.instagram.com/v23.0/{ig-user-id}/media_publish
     ?creation_id={container-id}&access_token={token}</code></pre>
<p>In n8n these are two HTTP Request nodes with a short Wait between (containers need a few seconds to process; videos need longer — poll the container's <code>status_code</code> until <code>FINISHED</code> for reels).</p>
<ul>
<li><strong>Stories:</strong> same flow with <code>media_type=STORIES</code></li>
<li><strong>Reels:</strong> <code>media_type=REELS</code> + <code>video_url</code> (must be a publicly fetchable .mp4)</li>
<li><strong>Image hosting:</strong> the API fetches your media by URL, so generated images must live somewhere public first — a free Cloudinary account works.</li>
</ul>

<h2>Gotchas from production</h2>
<ul>
<li><strong>n8n's default timezone is America/New_York.</strong> If your instance isn't configured, your "8 PM" cron fires at New York time. Set <code>GENERIC_TIMEZONE</code> or per-workflow <code>settings.timezone</code>.</li>
<li><strong>Page tokens expire (~60 days).</strong> Calendar the rotation or build a refresh workflow; silent token death is the most common "it stopped working".</li>
<li><strong>Use a content queue, not direct posting.</strong> A Google Sheet with <code>id | status | image_url | caption | scheduled_time</code> lets you approve items before a separate publisher workflow picks up <code>approved</code> rows. Decoupling generation from publishing is what makes the system safe to leave unattended.</li>
<li><strong>Story link stickers can't be placed via API</strong> — links in stories remain a manual action. Highlights have no public API either.</li>
</ul>
"""},

"kling-motion-control-guide": {
"title": "Kling Motion Control: Transfer Real Reel Performances onto an AI Character (2026)",
"desc": "How Kling V3 Omni motion control works, what it costs, and how to use a reference video to drive an AI character's performance for Instagram reels.",
"h1": "Kling Motion Control: Real Performances on AI Characters",
"cta": f"The {DNA} turns any reel into a ready-to-use motion blueprint — including the Kling motion prompt.",
"body": """
<p>Text-prompted AI video has a ceiling: you can describe choreography, but the model invents the performance, and identity tends to drift with every second. Motion control flips this — you provide a <em>reference video</em> and the model transfers the performer's actual motion onto your character.</p>

<h2>What Kling V3 Omni motion control does</h2>
<p>You supply two inputs: a <strong>start frame image</strong> (your character — identity, outfit, scene) and a <strong>reference video</strong> (3–30 seconds of a real performance). The output keeps your character's identity while reproducing the reference's body motion, gesture timing, and energy. In our production tests, identity holds dramatically better than with text choreography.</p>

<h2>Cost reality (June 2026)</h2>
<table>
<tr><th>Mode</th><th>Cost</th><th>Notes</th></tr>
<tr><td>Plain image-to-video (text choreography)</td><td>~13 credits/sec</td><td>5s ≈ 65 credits</td></tr>
<tr><td>V3 Omni motion control</td><td>15 credits/sec</td><td>5s = 75, 10s = 150</td></tr>
</table>
<p>Cost scales with output length, not complexity. Start with 5-second clips: length is rarely why a reel underperforms, and it halves your iteration cost.</p>

<h2>The workflow that produces convincing reels</h2>
<ol>
<li><strong>Pick a benchmark reel</strong> with a human subject and few cuts (≤4). Cuts are the enemy: driving motion across a cut boundary makes the character "teleport" between poses.</li>
<li><strong>Replicate the first frame</strong> with your character: same pose, framing, scene, and lighting, your character's identity. Generate it at 9:16 (1080×1920) — Kling preserves the source image's aspect ratio, so a square-ish source produces a square-ish video.</li>
<li><strong>Run motion control</strong> with that image + the benchmark video, prompting it to preserve identity and transfer motion from the first N seconds.</li>
<li><strong>Keep a human approval step</strong> before publishing. Motion transfer is good, not perfect — hands and rapid turns still fail sometimes.</li>
</ol>

<h2>Practical warnings</h2>
<ul>
<li>Generation continues server-side even if your client times out waiting — poll for the result instead of retrying (retrying = paying twice).</li>
<li>Long reference reels: split at cut boundaries, generate per-segment clips, and concatenate with ffmpeg, rather than driving across cuts.</li>
<li>Ethics/policy: transfer <em>motion styles</em>, disclose AI content, and don't recreate identifiable people. The motion is the technique; the identity must be yours.</li>
</ul>
"""},

"ai-content-quality-control": {
"title": "AI Quality Control for Generated Content: the PASS/FAIL Gate Pattern",
"desc": "How to stop bad AI generations from reaching your audience: a Claude-judged PASS/FAIL gate with feedback loops, retry caps, and the design rules that make it reliable.",
"h1": "The AI Quality Gate: Stop Bad Generations Before They Post",
"cta": f"This exact QC chain ships preconfigured in the {KIT}.",
"body": """
<p>Anyone can automate content generation. The difference between an account that grows and one that looks like a bot farm is what happens <em>between</em> generation and publishing. The pattern that works in production is a strict AI judge with a feedback loop.</p>

<h2>The contract</h2>
<p>After each generation, a vision-capable model (we use Claude) receives the image and the original spec, and must reply with exactly one line:</p>
<pre><code>PASS
— or —
FAIL: &lt;specific reason — e.g. "left hand has six fingers", "lighting is flat frontal, spec requires hard side light"&gt;</code></pre>
<p>Three design rules make this reliable:</p>
<ol>
<li><strong>Single-line contract, checked mechanically.</strong> The workflow checks <code>startsWith("PASS")</code> — no parsing essays, no ambiguity.</li>
<li><strong>Failure reasons feed the next attempt.</strong> The FAIL text is injected into the regeneration prompt ("previous attempt failed because…"). This converts retries from coin flips into corrections.</li>
<li><strong>Cap attempts at 3.</strong> Past three, you're burning credits on a prompt that needs human eyes. The item goes to a rejected queue instead.</li>
</ol>

<h2>Order of operations matters</h2>
<p>Upload the image to public hosting <em>before</em> QC, not after. Judge models fetch images server-side, and most generation providers' artifact URLs aren't publicly fetchable. Uploading first also means the approved URL is the exact one you publish — no second upload, no mismatch.</p>

<h2>What to put in the judge's rubric</h2>
<ul>
<li>Anatomy (hands, teeth, eyes — still the top AI tells in 2026)</li>
<li>Identity match against the persona's locked reference</li>
<li>Spec compliance: pose, framing, lighting, camera finish</li>
<li>Artifacts: extra limbs/objects, melted text, warped backgrounds, accidental grain or vignette the spec didn't ask for</li>
</ul>

<h2>The economics</h2>
<p>A QC call costs a fraction of a cent of API time; a failed generation costs real credits and a bad post costs audience trust. In production, roughly 30–50% of generations fail the first attempt — the gate plus feedback loop converts most of those into clean second attempts. Add a human approval tap (Telegram buttons work well) as the final layer: AI QC catches defects, humans catch "technically fine but off-brand".</p>
"""},

"telegram-approval-workflow-n8n": {
"title": "Human-in-the-Loop Automation: Telegram Approve/Reject Buttons in n8n",
"desc": "Build a Telegram approval gate for any n8n automation: inline buttons, callback handling, queue states, and auto-regeneration of rejected items.",
"h1": "Telegram Approval Gates for n8n Automations",
"cta": f"The full approval loop — request, callback, regeneration — is included in the {KIT} as importable workflows.",
"body": """
<p>Full automation without review is how automated accounts die. The pattern below adds a one-tap human gate to any n8n pipeline, using Telegram because its bot API is free, instant, and runs on the phone you already check.</p>

<h2>The state machine</h2>
<p>Drive everything from a queue (Google Sheets is fine) with a status column:</p>
<pre><code>pending → awaiting_approval → approved | rejected → posted
                       rejected → regenerating → replaced</code></pre>
<p>Each state transition is owned by exactly one workflow. That single rule prevents the classic bug where two workflows fight over a row.</p>

<h2>Workflow 1: the proposer</h2>
<p>On a schedule, pick the oldest <code>pending</code> row, send the content to your chat with inline buttons, and mark it <code>awaiting_approval</code>:</p>
<pre><code>// Telegram sendPhoto/sendVideo with reply_markup:
{ "inline_keyboard": [[
  { "text": "✅ Approve", "callback_data": "approve:{{rowId}}" },
  { "text": "❌ Reject",  "callback_data": "reject:{{rowId}}" }
]]}</code></pre>

<h2>Workflow 2: the callback handler</h2>
<p>A webhook receives Telegram's <code>callback_query</code>. Parse <code>action:rowId</code>, validate both, update the row, and answer the callback so the user gets instant button feedback. Validate strictly — ignore anything that isn't exactly <code>approve</code> or <code>reject</code> with a known row id.</p>

<h2>Workflow 3 (optional): the regenerator</h2>
<p>A scheduled workflow picks the oldest <code>rejected</code> row, marks it <code>regenerating</code> <em>first</em> (this prevents retry storms if generation fails), reruns the generation chain, and appends a replacement row as <code>pending</code>. Rejection becomes self-healing: you tap ❌ and a better candidate shows up in the next proposal cycle.</p>

<h2>Hard-won details</h2>
<ul>
<li>Claim rows by writing the new state <em>before</em> starting slow work, so a second scheduler tick can't grab the same row.</li>
<li>Send media by public URL, not file upload — you want the exact asset that will be published.</li>
<li>One chat per project. Mixing projects in one approval chat guarantees a mis-tap eventually.</li>
<li>Put a daily error digest in the same chat: approvals and failures in one place means you actually see both.</li>
</ul>
"""},

"viral-reel-structure-analysis": {
"title": "Why Reels Go Viral: Analyzing Structure, Motion, and Camera Language as Data",
"desc": "A method for decoding viral reels into reusable structure: cut timelines, motion energy, camera language, lighting — and how to apply the blueprint to your own content.",
"h1": "Decoding Viral Reels into Reusable Blueprints",
"cta": f"The {DNA} automates this entire analysis — any reel URL in, structured JSON blueprint out, Kling motion prompt included.",
"body": """
<p>"Study what works in your niche" is advice everyone gives and nobody operationalizes. Here's how to turn a high-performing reel into structured data you can actually reuse — what we call its DNA.</p>

<h2>The five layers worth extracting</h2>
<ol>
<li><strong>Cut timeline.</strong> How many shots, how long each holds, where the rhythm changes. Most viral short-form sits between 1 and 4 cuts — and the first cut's timing is the retention hook.</li>
<li><strong>Subject motion.</strong> What the performer physically does, beat by beat, and the energy curve: where motion is sharp, where it settles. This is the layer that text prompts describe worst and that matters most.</li>
<li><strong>Camera language.</strong> Distance (close/medium/full), angle, and movement (locked, handheld drift, push-in). "Phone-shot handheld at chest height" reads completely differently from "locked tripod full-body".</li>
<li><strong>Lighting and grade.</strong> Source direction, hardness, color temperature, and the finish: clean vs grain, lifted blacks vs crushed. Aesthetic consistency across posts comes from copying this layer precisely.</li>
<li><strong>Format skeleton.</strong> Hook (first 1.5s), development, payoff. Strip the specific subject and the skeleton transfers across niches.</li>
</ol>

<h2>The practical method</h2>
<p>Extract 6–10 evenly spaced frames from the reel plus the audio-stripped clip, and have a vision model describe each layer in structured JSON. The critical prompt-engineering detail: ask for <em>observable facts</em> (shot lengths in seconds, light direction) rather than interpretations ("energetic vibe") — facts are reusable, vibes are not.</p>

<h2>Using a blueprint</h2>
<ul>
<li><strong>For AI generation:</strong> recreate the first frame with your character (pose, framing, lighting from the blueprint), then drive motion with the blueprint's motion description — or with the original video via motion control. See the <a href="kling-motion-control-guide.html">Kling guide</a>.</li>
<li><strong>For human creators:</strong> the blueprint is a shot list. Same cuts, same camera positions, your subject.</li>
<li><strong>For strategy:</strong> blueprint your niche's top 50 reels and patterns jump out — recurring skeletons, dominant lighting, the 2–3 formats that actually carry the niche. Make those before inventing new ones.</li>
</ul>

<p>One ethical line: blueprints describe structure; they don't copy content. Recreate <em>formats</em> with your own subject and styling — don't reproduce someone's actual footage or identity.</p>
"""},

"n8n-vs-zapier-make-social-automation": {
"title": "n8n vs Zapier vs Make for Social Media Automation (2026, Honest Comparison)",
"desc": "Why self-hosted n8n wins for AI content pipelines: cost at volume, code nodes, loops and retries — and when Zapier or Make is actually the better pick.",
"h1": "n8n vs Zapier vs Make for AI Content Pipelines",
"cta": f"If you choose n8n, the {KIT} is 13 production workflows you don't have to build.",
"body": """
<p>Short answer: for an AI content pipeline that runs hundreds of operations a day, self-hosted n8n is the only economically sane option. Longer answer below, including where the others win.</p>

<h2>The cost math that decides it</h2>
<p>A daily AI-influencer pipeline (generation, QC retries, approvals, publishing, replies, metrics) executes 200–600 operations per day. Zapier and Make price per operation/task; at this volume you're in their upper tiers — real money every month, forever. Self-hosted n8n is free software on a ~$6 VPS, unlimited executions. The pipeline's economics only work because the orchestration layer costs nothing.</p>

<h2>Capability differences that matter for AI pipelines</h2>
<table>
<tr><th></th><th>n8n (self-hosted)</th><th>Zapier</th><th>Make</th></tr>
<tr><td>Cost at 10k+ ops/month</td><td>$0 + VPS</td><td>$$$</td><td>$$</td></tr>
<tr><td>Real code nodes (JS)</td><td>Yes, first-class</td><td>Limited</td><td>Limited</td></tr>
<tr><td>Loops / retry with feedback</td><td>Native</td><td>Awkward</td><td>Possible, fiddly</td></tr>
<tr><td>Call any API (raw HTTP)</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Webhooks in</td><td>Free, unlimited</td><td>Plan-gated</td><td>Plan-gated</td></tr>
<tr><td>Data stays on your server</td><td>Yes</td><td>No</td><td>No</td></tr>
<tr><td>Setup effort</td><td>Hours (Docker/npx)</td><td>Minutes</td><td>Minutes</td></tr>
</table>
<p>The killer features for AI work are the code nodes and loop control: a quality-control gate with "max 3 attempts, feed the failure reason back into the prompt" is a few nodes in n8n and a contortion act elsewhere.</p>

<h2>When NOT to use n8n</h2>
<ul>
<li>You run 5 simple zaps a month — Zapier's polish wins, cost is irrelevant at that volume.</li>
<li>Nobody on the team can maintain a server. Self-hosting means you own updates and backups (an hour a month, but a real hour).</li>
<li>You need certified enterprise connectors with SLAs.</li>
</ul>

<h2>n8n gotchas to know going in</h2>
<ul>
<li>Default timezone is America/New_York — set <code>GENERIC_TIMEZONE</code> before trusting any cron.</li>
<li>Workflow imports arrive deactivated and credentials don't travel with JSON exports — re-link after import.</li>
<li>In single-item flows after an HTTP Request node, use <code>.first().json</code> rather than <code>.item.json</code> — paired-item tracking breaks through HTTP nodes.</li>
</ul>
"""},

"ai-influencer-monetization": {
"title": "How AI Influencers Actually Make Money in 2026 (Ranked by Realism)",
"desc": "The real monetization paths for AI personas — brand deals, affiliate, UGC ads, subscriptions — with honest follower thresholds and which to attempt first.",
"h1": "How AI Influencers Actually Make Money",
"cta": f"The production side is solvable today — the {KIT} is the full posting/reels/replies machine, so your hours go into the deals.",
"body": """
<p>The uncomfortable truth: an AI influencer is a media business, and media businesses monetize audiences, which take months to build. Here are the paths that actually pay, ranked by realism for a small account, with the thresholds nobody includes in the hype threads.</p>

<h2>1. UGC-style ads for brands (works from ~0 followers)</h2>
<p>Brands need ad creative more than they need your audience. An AI persona that can "wear" products and perform in reels is an ad-production capability — $50–300 per video on UGC marketplaces and via direct outreach. This is the only path that pays before you have an audience, because you're selling production, not reach.</p>

<h2>2. Affiliate links (works from ~100 followers, scales with trust)</h2>
<p>Marketplace affiliate programs (Amazon in the US; Shopee/Tokopedia/TikTok Shop in Southeast Asia — the latter approve near-instantly) pay commission per sale from your link-in-bio. Expect pennies until your audience trusts recommendations; the real value early is the <em>conversion data</em> — which products your audience clicks tells you what to sell later.</p>

<h2>3. Brand deals / sponsored posts (realistic from ~1,000 engaged followers)</h2>
<p>Below 1,000 followers with real engagement, outreach burns contacts — wait for the threshold. Two non-negotiables for AI personas: disclose AI status up front in the media kit (surprise discovery kills deals and risks the account), and bring engagement stats, not follower counts. Local/small brands in your persona's niche close far more often than global names.</p>

<h2>4. Subscriptions and paid DMs (realistic from ~10k)</h2>
<p>Platform subscriptions, exclusive content, and paid-DM products only convert from large warm audiences. Measured reality: the difference between $1k/month and $5k+/month AI persona accounts is usually 4+ simultaneous revenue streams — but each stream switched on only after the audience supported it.</p>

<h2>5. Selling the machinery (works immediately, isn't influencer revenue)</h2>
<p>The skills that build an AI influencer — automation, generation pipelines, quality control — sell to other creators and businesses as products and services regardless of your follower count. Many "AI influencer" operations quietly earn more from this than from the persona itself.</p>

<h2>The honest sequencing</h2>
<p>Production-capability income first (UGC, machinery), affiliate as data collection second, brand deals at 1k, subscriptions at 10k. Anyone selling you a path that starts with brand deals at 200 followers is selling the dream, not the math.</p>
"""},

}
