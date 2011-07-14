
import gettext

gettext.textdomain('hans')
lang = gettext.translation('hans')
_ = lang.gettext
