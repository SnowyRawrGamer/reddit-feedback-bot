import praw
import time
import os
from datetime import datetime

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="weekly_feedback_bot",
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD")
)

sub = reddit.subreddit("feedback4feedback")  # CHANGE if needed

now = time.time()

recent_posts = []
for post in sub.new(limit=200):
    age = now - post.created_utc
    
    if 86400 < age < 10 * 86400:
        recent_posts.append(post)

lowest = sorted(recent_posts, key=lambda x: x.num_comments)[:5]

zero = [
    p for p in recent_posts
    if p.num_comments == 0 and (now - p.created_utc < 7 * 86400)
]

text = "🎮 5 Games You Might Have Missed This Week\n\n"
text += "These posts didn’t get much attention — go show them some love!\n\n"

for p in lowest:
    text += f"- [{p.title}]({p.url}) — {p.num_comments} comments\n"

text += "\n---\n\n💬 No Feedback Yet:\n\n"

for p in zero:
    text += f"- [{p.title}]({p.url})\n"

text += f"\n\n_Post generated on {datetime.utcnow().strftime('%Y-%m-%d')}_"

sub.submit("5 Games You Might Have Missed This Week", selftext=text)
