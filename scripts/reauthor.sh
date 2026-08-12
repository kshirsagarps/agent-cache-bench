#!/usr/bin/env bash
set -e

git config user.name "kshirsagarps"
git config user.email "pratyush.kshirsagar@gmail.com"

# Reset git author on head
GIT_COMMITTER_NAME="kshirsagarps" GIT_COMMITTER_EMAIL="pratyush.kshirsagar@gmail.com" git commit --amend --author="kshirsagarps <pratyush.kshirsagar@gmail.com>" --no-edit

echo "SUCCESS_AMEND_AUTHOR"
