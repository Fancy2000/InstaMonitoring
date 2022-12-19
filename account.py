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
            for userId in needToUnfollow:
                self.cl.user_unfollow(userId)
            return True
        except:
            return False

    def GetUserId(self):
        return self.cl.user_id

    def FollowOnSubs(self):
        print("follow subs")
        try:
            needToFollow = set(self.ShowFollowers().keys()) - set(self.ShowSubscriptions().keys())
            print(needToFollow)
            for userId in needToFollow:
                self.cl.user_follow(userId)
            return True
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
        users = set(self.cl.story_viewers(story_pk).keys()) - set(self.ShowFollowers().keys())
        print(users)
        return users

    def ShowStoriesInfo(self):
        stories = self.cl.user_stories(self.cl.user_id)
        print(stories)
        return stories


