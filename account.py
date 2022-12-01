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
        try:
            needToUnfollow = set(self.ShowFollowers().keys()) - set(self.ShowSubscribers().keys())
            for userId in needToUnfollow:
                self.cl.user_unfollow(userId)
            return True
        except:
            return False

    def FollowOnSubs(self):
        try:
            needToFollow = set(self.ShowSubscribers().keys()) - set(self.ShowFollowers().keys())
            for userId in needToFollow:
                self.cl.user_follow(userId)
            return True
        except:
            return False
    # who follows you
    def ShowFollowers(self):
        return self.cl.user_followers(str(self.cl.user_id))

    # you follow
    def ShowSubscriptions(self):
        return self.cl.user_following(str(self.cl.user_id))

