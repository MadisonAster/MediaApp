#===============================================================================
# @License: 
#    This example file is public domain. See ADDENDUM section in LICENSE.
#    You may do the following things with this file without restrictions or conditions:
#        1. Modify it.
#        2. Remove or modify this section to your liking.
#        3. Redistribute it under any licensing terms that you wish.
#        4. Make copyright claims to derivative works of this file.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#===============================================================================

import os
if __name__ == '__main__':
    if os.path.abspath(__file__).split(os.sep)[-2] == 'MediaApp':
        import __init__ as MediaApp
        MediaApp.run()
    else:
        ##### Rename MyApp to your App's name here #####
        import __init__ as MyApp
        MyApp.run()
