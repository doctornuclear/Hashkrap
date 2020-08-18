import json
from instabot import Bot

bot = Bot()
bot.login(username="username", password="password",
          is_threaded=True)
def purpose_of_hashtag(engagement, avg_likes_of_hashtag):
    probability = engagement/avg_likes_of_hashtag
    if 1 <= probability <= 1.5:
        purpose = "Ranking"
        probability_ranking = "High"
    elif 1 > probability >= 0.6:
        purpose = "Ranking"
        probability_ranking = "Medium"
    elif 0.6 > probability > 0.3:
        purpose = "Exposure"
        probability_ranking = "Low"
    elif probability <= 0.3:
        purpose = "Exposure"
        probability_ranking = "Very Low"
    else:
        purpose = "Ranking"
        probability_ranking = "Very High"
    probability = "%.3f" % probability
    return probability_ranking, purpose, probability

def profile_engagements(username, bot=bot):
    sum_likes = 0
    user_id = bot.get_user_id_from_username(username)
    try:
        if "not found" in bot.api.last_json["message"]:
            return "not found"
    except:
        pass
    bot.get_user_medias(user_id=user_id, filtration=False)
    posts = bot.api.last_json["items"]
    for post in posts:
        likes = post["like_count"]
        sum_likes += likes
    if len(posts) < 1:
        return 0
    return sum_likes/len(posts)
    # return 60