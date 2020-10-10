ls src | while read file; do
  python3 src/$file test;
  done