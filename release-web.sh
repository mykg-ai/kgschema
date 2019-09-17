cd web
npm run build
cd dist
git init
git remote add origin git@github.com:mykg-ai/kgs.git
git add .
git commit -m 'init'
git push --force -u origin master
cd ../..

sh release.sh
