from instagrapi import Client


class Account:
    def __init__(self, login, password, verifyCode=''):
        self.cl = Client()
        try:
            self.cl.login(login, password, verification_code=verifyCode)
            print("success auth")
        except:
            try:
                self.cl.login(login, password, verification_code=verifyCode)
                print("success auth")
            except:
                raise Exception("Please make sure of correctness your login or password or verification_code")

    def RemoveSubsNotFollowingYou(self):
        try:
            needToUnfollow = set(self.ShowSubscriptions().keys()) - set(self.ShowFollowers().keys())
            Subs = self.ShowSubscriptions().values()
            subs_nickname = set()
            for nick in Subs:
                subs_nickname.add(nick.username)
            Follows = self.ShowFollowers().values()
            fols_nickname = set()
            for nick in Follows:
                fols_nickname.add(nick.username)
            usernames = subs_nickname - fols_nickname
            for userId in needToUnfollow:
                self.cl.user_unfollow(userId)
            return usernames
        except:
            return False

    def GetUserId(self):
        return self.cl.user_id

    def FollowOnSubs(self):
        print("follow subs")
        try:
            needToFollow = set(self.ShowFollowers().keys()) - set(self.ShowSubscriptions().keys())
            print(needToFollow)
            Subs = self.ShowSubscriptions().values()
            subs_nickname = set()
            for nick in Subs:
                subs_nickname.add(nick.username)
            Follows = self.ShowFollowers().values()
            fols_nickname = set()
            for nick in Follows:
                fols_nickname.add(nick.username)
            usernames = fols_nickname - subs_nickname
            for userId in needToFollow:
                self.cl.user_follow(userId)
            return usernames
        except:
            return False

    # who follows you
    def ShowFollowers(self):
        self.cl._users_followers.clear()
        return self.cl.user_followers(str(self.cl.user_id))

    # you follow
    def ShowSubscriptions(self):
        self.cl._users_following.clear()
        return self.cl.user_following(str(self.cl.user_id))

    def ShowUsersWhoNotFollowYouSawStory(self, story_pk):
        story_viewers = self.cl.story_viewers(story_pk)
        print(story_viewers)
        user_view = set()
        for usershort in story_viewers:
            user_view.add(usershort.username)
        followers = self.ShowFollowers().values()
        print(followers)
        followers_set = set()
        for usershort in followers:
           followers_set.add(usershort.username)
        users = user_view - followers_set
        print(users)
        return users

    def ShowStoriesInfo(self):
        stories = self.cl.user_stories(self.cl.user_id)
        ans = []
        for i in stories:
            users = self.ShowUsersWhoNotFollowYouSawStory(i.pk)
            ans.append([i.thumbnail_url, users])
        print(ans)
        print(stories)
        return ans



