
import gettext
#import locale

#print str(locale.getdefaultlocale())
gettext.textdomain('hans')
lang = gettext.translation('hans')
_ = gettext.gettext

