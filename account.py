from instagrapi import Client


class Account:
    def __init__(self, login, password, verifyCode=''):
        self.cl = Client()
        try:
            self.cl.login(login, password, verification_code=verifyCode)
        except:
            try:
                self.cl.login(login, password, verification_code=verifyCode)
            except:
                raise Exception("Please make sure of correctness your login or password or verification_code")

    def RemoveSubsNotFollowingYou(self):
        needToUnfollow = set(self.ShowFollowers().keys()) - set(self.ShowSubscribers().keys())
        for userId in needToUnfollow:
            self.cl.user_unfollow(userId)

    def FollowOnSubs(self):
        needToFollow = set(self.ShowSubscribers().keys()) - set(self.ShowFollowers().keys())
        for userId in needToFollow:
            self.cl.user_follow(userId)

    # who follows you
    def ShowSubscribers(self):
        return self.cl.user_followers(str(self.cl.user_id))

    # you follow
    def ShowFollowers(self):
        return self.cl.user_following(str(self.cl.user_id))

