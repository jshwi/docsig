#=======================================================================
#
#          File:  audit.sh
#
#         Usage:  bash audit.sh
#
#   Description:  Execute audit on all commits between HEAD and origin.
#
#       Options:  NA
#  Requirements:  git>=2.39.0
#                 poetry>=1.2.1
#                 pyaud>=4.0.2
#          Bugs:  None known
#         Notes:  Before commencing stash all changes.
#                 On exit cleanup by aborting the rebase and popping
#                 the stash.
#        AUTHOR:  Stephen Whitlock (jshwi), stephen@jshwisolutions.com
#  ORGANIZATION:  Jshwi Solutions
#       Created:  01/01/2023 12:32:33
#      Revision:  0.1.0
#=======================================================================
set -o nounset


#---  FUNCTION  --------------------------------------------------------
#          NAME:  rebase-abort
#   DESCRIPTION:  Attempt to abort rebase, while silencing output, but
#                 do not error if not in a rebase.
#    PARAMETERS:  None
#       RETURNS:  0
#-----------------------------------------------------------------------
rebase-abort () {
    git rebase --abort > /dev/null 2>&1 || return 0
}


#---  FUNCTION  --------------------------------------------------------
#          NAME:  stash-pop
#   DESCRIPTION:  Attempt to pop stash, while silencing output, but
#                 do not error if no changes stashed.
#    PARAMETERS:  None
#       RETURNS:  0
#-----------------------------------------------------------------------
stash-pop () {
    git stash pop > /dev/null 2>&1 || return 0
}


#---  FUNCTION  --------------------------------------------------------
#          NAME:  cleanup
#   DESCRIPTION:  Run on exit, regardless of the result.
#                 Abort stash if in a stash, and pop stash if there is
#                 one.
#    PARAMETERS:  None
#       RETURNS:  0
#-----------------------------------------------------------------------
cleanup () {
    rebase-abort
    stash-pop
}


#---  FUNCTION  --------------------------------------------------------
#          NAME:  revision
#   DESCRIPTION:  Get current revision.
#    PARAMETERS:  None
#       RETURNS:  0
#-----------------------------------------------------------------------
revision () {
  git rev-parse --short HEAD
}


#---  FUNCTION  --------------------------------------------------------
#          NAME:  failure-msg
#   DESCRIPTION:  Announce failure and the commit that failed.
#    PARAMETERS:  None
#       RETURNS:  0
#-----------------------------------------------------------------------
failure-msg () {
    echo -e "\033[0;31mfailed on $(revision)"
    echo -e "please fix this commit before pushing\033[0m"

}


trap cleanup EXIT
git stash > /dev/null 2>&1
git rebase origin/master -x 'poetry run pyaud audit' || (failure-msg && exit 1)
