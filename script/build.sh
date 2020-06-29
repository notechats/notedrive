#!/usr/bin/env bash

name=notedrive
echo $name

if [ "$1" = "build" ]; then
  echo build
  # 编译
  python setup.py build
  # 生成 tar.gz
  python setup.py sdist
  # 生成 egg 包
  python setup.py bdist_egg
  # 生成 wheel 包
  python setup.py bdist_wheel

  #twine register dist/*
  # 发布包
  twine upload dist/*

  rm -rf $name.egg-info
  rm -rf dist
  rm -rf build
fi

if [ "$1" = "install" ]; then
  echo install
  pip uninstall $name -y
  python setup.py install

  rm -rf $name.egg-info
  rm -rf dist
  rm -rf build
fi

if [ "push" = "push" ]; then
  echo push
  git pull
  git add -A
  git commit -a -m "add"
  git push
fi

if [ "$1" = "clear_history" ]; then
  echo clear_history
  #1.Checkout
  git checkout --orphan latest_branch
  #2. Add all the files
  git add -A
  #3. Commit the changes
  git commit -am "clear history"
  #4. Delete the branch
  git branch -D master
  #5.Rename the current branch to master
  git branch -m master
  #6.Finally, force update your repository
  git push -f origin master
fi
