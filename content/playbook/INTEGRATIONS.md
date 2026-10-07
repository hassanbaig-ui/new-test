# Connecting FineCool's Channels

What each platform allows, what it gives the system, and what the media manager must provide. Tokens and keys go into the environment's **secrets**, never into chat or this repo.

| Platform | Official way in | What we get | What you provide |
|---|---|---|---|
| **YouTube** | YouTube Data API + YouTube Analytics API (Google Cloud) | All videos, views, likes, comments; your own watch time, retention, subscriber gains; reply to comments | Channel link · a Google Cloud project with both APIs enabled · an API key (public data) · OAuth access from the channel owner (own analytics + replies) |
| **Facebook Page** | Meta Graph API (Meta developer app) | Reels list and insights, comments, comment replies, Messenger | Admin access on the page · a Meta developer app · a long-lived Page access token |
| **Instagram** | Meta Graph API (same app) | Reels insights, comments, replies, DMs | Instagram switched to Business/Creator and linked to the Facebook page · same token |
| **TikTok** | TikTok Business account; API access is limited | Analytics through exports | TikTok handle · switch to Business account · weekly CSV export from TikTok Studio |
| **Facebook Group** | No API (removed by Facebook in 2024) | — | A human posts; Claude drafts (group-manager agent) |
| **WhatsApp Business** | WhatsApp Business app (free) | Greeting message, quick replies, labels | Set up on the shop phone using the reply bank |

## Fastest path (no code)

1. **Meta Business Suite** (free): set automated responses and saved replies for Facebook + Instagram using `REPLIES_AND_GROUP.md`. Instant replies work the same day.
2. **Zapier** (already connected to this account): connect Facebook Pages, Instagram and YouTube there; then new comments can be pulled in for the community-manager agent to draft replies, and new reels can be logged automatically.
3. **Weekly exports**: until the APIs are connected, download each platform's analytics export on Sunday and give it to the analytics-reporter agent.

## Environment settings needed for this cloud session

Allow these domains in the environment's Network access: `graph.facebook.com`, `www.googleapis.com`, `youtubeanalytics.googleapis.com`, `oauth2.googleapis.com`, and `huggingface.co` (for Urdu transcripts of reels). Then add the tokens as environment secrets.

## Limits we respect

- No bots posting in Facebook groups, no fake accounts, no buying followers: all break platform rules and can get the page banned.
- Replies are drafted by the system; a human approves before sending until the bank is proven.
- Cookie-based scraping logs out after heavy use (it happened on 6 Oct 2026). Official APIs are the long-term source.
