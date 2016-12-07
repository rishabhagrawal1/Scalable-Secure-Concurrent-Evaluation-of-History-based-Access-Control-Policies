import sys

##Object of attribute versions to be used in latestVersion and latestVersionBefore
class Version:

  def __init__(self, wts, rts, val):
    ##init new version object with pre specified values
    self.wts = wts
    self.rts = rts
    self.val = val 
    self.pendingMightRead = set()

