"""
Connects to the Reddit API to get rising submissions details and posts
them to a Discord webhook.
"""

import os
import requests


WEBHOOK_URL = os.environ["WEBHOOK"]


def main():
    """Start the script."""

    print("Connecting to Reddit...")
    message, image_url = get_rising_submissions("pics")

    print("Data received. Sending webhook...")
    post_message(message, image_url)


def get_rising_submissions(subreddit):
    """Connects to the Reddit API and queries the top rising submission
    from the specified subreddit.

    Parameters
    ----------
    subreddit : str
        The name of the subreddit without forward slashes.

    Returns
    -------
    tuple
        A tuple containing a formatted message and an image url.

    """

    url = f"https://www.reddit.com/r/{subreddit}/rising.json?limit=1"
    headers = {"User-Agent": "Reddit Rising Checker v1.0"}

    with requests.get(url, headers=headers) as response:

        data = response.json()["data"]["children"]

        # Iterate over all the children.
        for item in data:

            item_data = item["data"]

            # We will collect only the fields we are interested in.
            title = item_data["title"]
            permalink = "https://reddit.com" + item_data["permalink"]
            author = item_data["author"]
            score = item_data["score"]
            image_url = item_data["url"]

            # Compose a Markdown message using string formatting.
            message = f"[{title}]({permalink})\nby **{author}**\n**{score:,}** points"

            return (message, image_url)


def post_message(message, image_url):
    """Sends the formatted message to a Discord server.

    Parameters
    ----------
    message : str
        The formatted message to post.

    image_url : str
        The URL used as the thumbnail.

    """

    payload = {
        "username": "Rising Posts",
        "embeds": [
            {
                "title": "Top Rising Post",
                "color": 102204,
                "description": message,
                "thumbnail": {"url": image_url},
                "footer": {"text": "Powered by Elf Magic™"}
            }
        ]
    }

    with requests.post(WEBHOOK_URL, json=payload) as response:
        print(response.status_code)


if __name__ == "__main__":

    main()
