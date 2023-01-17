#!/usr/bin/env bash

# set -Ceu

TAG=$1
FILENAME="portable_swiftlint"

REPO_ROOT_DIR=$(
    cd $(dirname $0)/..
    pwd
)

cd "$REPO_ROOT_DIR"

echo $TAG


curl -sLJO "https://github.com/realm/SwiftLint/releases/download/${TAG}/$FILENAME.zip"

unzip -o -d "$FILENAME" "$FILENAME.zip"

if [ $? = 0 ]; then
    echo "unzipped"
else
    echo "unzip failed"
    rm -f $FILENAME.zip
    exit 0
fi

opt_in=$(
    $FILENAME/swiftlint rules | awk '$4=="yes"{print"  - " $2}'
)

not_opt_in=$(
    $FILENAME/swiftlint rules | awk '$4=="no"{print"  # - " $2}'
)

echo "opt_in_rules:" >| swiftlint_base.yml
echo -e "$opt_in" >> swiftlint_base.yml
echo -e "\n" >> swiftlint_base.yml

echo "disabled_rules:" >> swiftlint_base.yml
echo -e "$not_opt_in" >> swiftlint_base.yml

if [[ `git status --porcelain |grep swiftlint_base.yml ` ]]; then
    echo "modified"
    git add swiftlint_base.yml
    git commit -m "swiftlint base rule for \"$TAG\""
fi

echo "add tag: $TAG"
git tag $TAG

rm -rf $FILENAME
rm -f $FILENAME.zip
