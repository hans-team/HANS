
import gettext

gettext.textdomain('hans')

try:
    lang = gettext.translation('hans')
    _ = lang.gettext

except:
    _ = gettext.gettext
