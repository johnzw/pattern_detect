#the directory of all the pdf files
DIR=$1
echo "the directory you type in: "$DIR
cd $DIR

for file in `ls *.pdf`;do
	echo $file
	pdftoppm -rx 200 -ry 200 -jpeg $file ${file:0:(-4)} -singlefile
done