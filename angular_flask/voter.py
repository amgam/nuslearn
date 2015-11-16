from dbase import DBase

class Voter:

    def __init__(self):
        self.db = DBase()

    def upvote(self, vid_link):
    #  retrieveQuery = "UPDATE GlobalTagTable SET Age = 18 WHERE Age = 17"
        self.db.connect()
        print "upvoting ", vid_link

        updateGlobalQuery = "update GlobalVideoTable set votes = votes + 1 where vid_link=?"
        self.db.update(updateGlobalQuery, (vid_link,))

        updateTagQuery = "update GlobalTagTable set votes = votes + 1 where vid_link=?"
        self.db.update(updateTagQuery, (vid_link,))
        self.db.save()

        lst = self.db.retrieve("select * from GlobalVideoTable where vid_link=?", (vid_link,))
        print lst
        self.db.close()

        return True

    def downvote(self, vid_link):
    #  retrieveQuery = "UPDATE GlobalTagTable SET Age = 18 WHERE Age = 17"
        print "downvoting ", vid_link
        self.db.connect()

        updateGlobalQuery = "update GlobalVideoTable set votes = votes - 1 where vid_link=?"
        self.db.update(updateGlobalQuery, (vid_link,))

        updateTagQuery = "update GlobalTagTable set votes = votes - 1 where vid_link=?"
        self.db.update(updateTagQuery, (vid_link,))
        self.db.save()

        lst = self.db.retrieve("select * from GlobalVideoTable where vid_link=?", (vid_link,))
        self.db.close()

        print lst
        return True
